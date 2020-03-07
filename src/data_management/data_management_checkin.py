import pandas as pd

from bld.project_paths import project_paths_join as ppj


def venue_istanbul(venue_data):
    """Function for finding venues in istanbul

    Function eliminates venues not in Turkey, categorized as "Home (private)" and
    not within certain area.

    In the elimination process, two line equations are calculated and
    venue coordinates should lie between those lines to be in Istanbul's borders.

    Args:
        | venue_data (pd.Dataframe): venue information dataset with columns
            venue_id, latitude, longitude, category and country

    Returns:
        the reduced venue dataset including only non-eliminated venues
    """

    # Country of interest is Turkey
    venue_data = venue_data[venue_data.country == "TR"]
    # Exclude private housing
    exclude_list = [
        "Home (private)",
        "Residential Building (Apartment / Condo)",
        "Housing Development",
    ]
    for exc in exclude_list:
        venue_data = venue_data[venue_data.category != exc]
    # Elimination using coordinates
    venue_data = venue_data.drop(
        venue_data[
            (venue_data["latitude"] < 40.803)  # southest point
            | (venue_data["latitude"] > 41.617)  # northest point
            | (  # line equation for eastern boundary
                venue_data["latitude"]
                < (venue_data["longitude"] * 0.43931624 + 27.913231)
            )
            | (  # line equation for western boundary
                venue_data["latitude"]
                > (venue_data["longitude"] * 2.51362773 - 29.14609)
            )
        ].index
    )

    return venue_data


if __name__ == "__main__":

    # Load data
    with open(
        ppj("IN_DATA", "Foursquare_data/dataset_TIST2015_Checkins.txt"), "rb"
    ) as c:
        check_in = pd.read_csv(
            c,
            sep="\t",
            header=None,
            names=["user_id", "venue_id", "utc_time", "timezone_offset"],
        )

    with open(ppj("IN_DATA", "Foursquare_data/dataset_TIST2015_POIs.txt"), "rb") as p:
        venue_data = pd.read_csv(
            p,
            sep="\t",
            header=None,
            names=["venue_id", "latitude", "longitude", "category", "country"],
        )

    # Only include venues in Istanbul
    adj_venue_data = venue_istanbul(venue_data)

    # Count the check-in of each venue
    check_in_counts = check_in.venue_id.value_counts().rename("check_in_counts")
    adj_venue_data = adj_venue_data.join(check_in_counts, on="venue_id", how="left")

    # Venues with at least 1 check-in per day (data is 18 months long)
    reduced_venue = adj_venue_data[adj_venue_data.check_in_counts > 18 * 30].drop(
        "category", axis=1
    )

    # Out data
    with open(ppj("OUT_DATA", "reduced_check_in_dataset.csv"), "w") as out_file:
        reduced_venue.to_csv(out_file)
