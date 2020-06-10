import sys

import numpy as np
import pandas as pd
import xgboost as xgb
from numba import jit
from numba import prange
from sklearn.model_selection import RandomizedSearchCV

from bld.project_paths import project_paths_join as ppj


def list_generator(keyword):
    """Function for getting the variable names from txt file
    and converting into a list.

    Args:
        keyword (str): the name of txt file

    Returns:
        the list of variable names
    """

    with open(ppj("IN_SPECS", keyword + ".txt"), "r") as f:
        var_read = f.read()
    return list(var_read.split("\n"))


def rule_func(var_list, dataset, rule):
    """Function for applying data management rule on dataset with given variable names.
    Variable names should match with dataset's column names.

    Defined rules are exclusion, conversion and length generation.

    Exclusion(exclude) rule excludes variable from the dataset.

    Conversion(convert) rule converts "f" and "t" values into 0 and 1 respectively.
    Thus variable should have values either "f" or "t".

    Length generator(lengthen) rule gets the string lenght,
    adds "_len" to variable name and exclude variable from dataset.

    Args:
        | var_list (list): list of variables to apply
        | dataset (pd.Dataframe): dataset to implement the rule
        | rule (str): can take values 'exclude', 'convert' or 'lengthen'

    Returns:
        the altered dataset (pd.Dataframe)
    """

    if rule == "exclude":
        dataset = dataset.drop(var_list, axis=1)

    elif rule == "convert":
        for c in var_list:
            dataset[c] = dataset[c].replace({"f": 0, "t": 1})

    elif rule == "lengthen":
        for l in var_list:
            dataset[l + "_len"] = dataset[l].str.len()
            dataset = dataset.drop(l, axis=1)

    else:
        raise ValueError("Rule is not defined")

    return dataset


@jit(nopython=True)
def distance_calc(house, venue):
    """Function for calculating the distance between
    a house and a venue while taking world's shape into consideration.

    Args:
        | house (list): list including latitude and longitude of a house
        | venue (list): list including latitude and longitude of a venue

    Returns:
        the approximate distance (float)

    """

    # approximate radius of earth in km
    R = 6373.0

    house_lat = np.deg2rad(house[0])
    house_lng = np.deg2rad(house[1])
    venue_lat = np.deg2rad(venue[0])
    venue_lng = np.deg2rad(venue[1])

    dist = (
        np.sin((venue_lat - house_lat) / 2) ** 2
        + np.cos(house_lat)
        * np.cos(venue_lat)
        * np.sin((venue_lng - house_lng) / 2) ** 2
    )

    return 2 * R * np.arcsin(np.sqrt(dist))


def score_func(house_data, venue_data):
    """Function for calculating location-based score of a house.

    Function gets a house and venues within 1 km radius of that house,
    calculates each venue's influential score on that house with dividing
    venue's check-in count with the distance.
    With that division, score is adjusted to popularity and distance.
    In the end, that house's score is the mean of relevant venues' influential scores.

    Args:
        | house_data (pd.Dataframe): airbnb dataset including house features
            especially latitude, longitude
        | venue_data (pd.Dataframe): dataset with venues' latitude, longitude
            and check_in_counts

    Returns:
        house_data with additional column called location_score (pd.Dataframe)
    """

    # coordinates should be tuples for geopy.distance function
    venue_data_list = np.array(
        list(zip(venue_data.latitude, venue_data.longitude, venue_data.check_in_counts))
    )
    house_data_coordinate = np.array(
        list(zip(house_data.latitude, house_data.longitude))
    )
    location_score_list = np.empty([len(house_data), 1])

    def numba_func(venue_data_list, house_data_coordinate):
        """Inside function for numba application.
        """

        for house in prange(len(house_data_coordinate)):
            # Preliminary elimination based on coordinates
            red_venue_list = np.array(
                list(
                    filter(
                        lambda x: (
                            x[0] - house_data_coordinate[0][0] < 0.01
                        )  # latitude
                        & (x[1] - house_data_coordinate[0][1] < 0.01),  # longitude
                        venue_data_list,
                    )
                )
            )

            score_list = np.array(0)
            for ven in prange(len(red_venue_list)):
                cal_dist = distance_calc(
                    house_data_coordinate[house], red_venue_list[ven][0:2]
                )
                if cal_dist < 1:  # venues closer than 1 km
                    np.append(score_list, red_venue_list[ven][2] / cal_dist)
            np.append(location_score_list, np.mean(score_list))
        return location_score_list

    location_score_list = numba_func(venue_data_list,house_data_coordinate)
    house_data["location_score"] = location_score_list

    return house_data


def dummy_func(data, column_list):
    """Function for creating dummy variable columns out of defined columns.

    Created dummy columns have the name of source column as prefix and "_".
    Function drops the source column from the dataset.

    Args:
        | data (pd.Dataframe): dataset of interest contaning columns with categorical data
        | column_list (list): list of columns to get dummy variables

    Returns:
        the altered dataset with dummy variable columns (pd.Dataframe)

    """

    for column in column_list:
        temp_data = pd.get_dummies(data[column]).add_prefix(str(column + "_"))
        data = data.drop(column, axis=1)
        data = pd.concat([data, temp_data], axis=1)

    return data


def data_management(date, venue_data, g_data):
    """Function for data management.
    It loads the airbnb dataset and rearranges both airbnb and generated
    dataset for prediction.

    A certain amount of house features  are excluded, the list can be found
    in src/specs/var_exclude.txt.
    In addition, for some features only the length is considered,
    similarly listed in src/specs/var_len.txt.

    Args:
        | date (str): a part of airbnb dataset's name also indicating scraping date
        | venue_data (pd.Dataframe): the dataset including venues' information
        | g_data (pd.Dataframe): randomly generated house features for prediction

    Returns:
        | data (pd.Dataframe): the cleared, ready-for-modelling, dataset
        | g_data (pd.Dataframe): the altered generated data
    """

    with open(ppj("IN_DATA", "Airbnb_data/" + date + "_listings.csv"), "rb") as d:
        data = pd.read_csv(d, low_memory=False)

    # Data clearing process
    rule_list = ["exclude", "convert", "lengthen"]
    for rule in rule_list:
        var_list = list_generator(keyword="var_" + rule)
        data = rule_func(var_list=var_list, dataset=data, rule=rule)

    # Only include apartments and exclude Shared rooms for simplicity
    data = (
        data.loc[
            (data["room_type"] != "Shared room")
            & (data["property_type"] == "Apartment"),
        ]
        .copy()
        .reset_index()
    )

    # Calculate the location score of each house
    data = score_func(house_data=data, venue_data=venue_data)

    # Preparing data for modelling
    data = dummy_func(
        data=data, column_list=["room_type", "bed_type", "cancellation_policy"]
    )
    g_data = dummy_func(
        data=g_data, column_list=["room_type", "bed_type", "cancellation_policy"]
    )

    # Drop remaining unnecessary columns in case of differences in airbnb datasets
    col_list = list(g_data.columns)
    col_list.append("price")
    data = data.filter(col_list, axis=1)

    nan_fill_list = [
        "host_is_superhost",
        "host_listings_count",
        "host_has_profile_pic",
        "host_identity_verified",
        "location_score",
    ]
    for item in nan_fill_list:
        data[item] = data[item].fillna(0)

    currency_list = ["price", "security_deposit", "cleaning_fee", "extra_people"]
    for item in currency_list:
        data[item] = data[item].fillna("$0.00")
        data[item] = data[item].str.replace(",", "").str.extract(r"(\d+)").astype(int)

    return data, g_data


def prediction_func(data, g_data, grid_search, param_list):
    """Function for using dataset to train a model and
    predicting prices for a generated data.

    Parameter search is done using RandomizedSearchCV since it is computationally
    more efficientcompared to GridSearchCV.

    In param_list, learning_rate, subsample and max_depth,
    min_child_weight, gamma and colsample_bytree can be included.

    Args:
        | data (pd.Dataframe): the dataset including house features and prices
        | g_data (pd.Dataframe): randomly generated house features for prediction purposes
        | grid_search (bool): indicates whether model is trained with parameter
		    search(True) or use default values(False)
        | param_list (list): the list of parameters to be included in parameter search

    Returns:
        the predicted prices for houses in g_data (np.array)
    """

    # Base Model
    xgb_reg = xgb.XGBRegressor(n_treads=-1)

    if grid_search:
        # Search for best parameters in model
        params = {
            "learning_rate": [i / 20 for i in range(1, 11)],
            "min_child_weight": [i for i in range(3, 12)],
            "gamma": [i / 10.0 for i in range(3, 8)],
            "subsample": [i / 10.0 for i in range(7, 11)],
            "colsample_bytree": [i / 10.0 for i in range(6, 11)],
            "max_depth": [i for i in range(3, 8)],
        }

        # Only includes selected parameters
        params = {key: params[key] for key in param_list}

        xgb_reg = RandomizedSearchCV(
            estimator=xgb_reg,
            param_distributions=params,
            n_iter=5,
            cv=3,
            random_state=23,
            iid=False,
        )

    xgb_reg.fit(data.drop("price", axis=1), data.price)

    return xgb_reg.predict(g_data)


if __name__ == "__main__":

    # Load data
    with open(ppj("OUT_DATA", "reduced_check_in_dataset.csv"), "rb") as c:
        reduced_venue = pd.read_csv(c)

    with open(ppj("OUT_DATA", "generated_house_data.csv"), "rb") as g:
        generated_data = pd.read_csv(g)

    date = sys.argv[1]

    data, generated_data = data_management(
        date=date, venue_data=reduced_venue, g_data=generated_data
    )
    prediction = prediction_func(
        data=data,
        g_data=generated_data,
        grid_search=True,
        param_list=["learning_rate", "subsample", "max_depth"],
    )
    predicted_df = pd.DataFrame(prediction, columns=[date])

    # Out data
    with open(ppj("OUT_PREDICTION", f"{date}_prediction.csv"), "w") as p:
        predicted_df.to_csv(p, index=False)
