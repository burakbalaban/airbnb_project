import re
import sys

import matplotlib.pyplot as plt
import pandas as pd

from bld.project_paths import project_paths_join as ppj


def data_prep(data):
    """Function calculating yearly and monthly change

    Args:
        data (pd.Dataframe): dataset with predicted values

    Returns:
        | monthly_change (pd.Dataframe): includes monthly change in mean prices
        | yearly_change (pd.Dataframe): includes change in mean prices compared
            to last year's same month
    """

    mean_df = data.mean(axis=0)
    # Rearranging the index
    mean_df.index = pd.to_datetime(mean_df.index, format="%Y_%m_%d").strftime("%Y-%m")

    # Available dates for yearly change
    regex = re.compile(r"-(0[1-3]|0[5-6]|12)")
    reduced_dates = list(filter(lambda d: not regex.search(d), mean_df.index))

    monthly_change = mean_df.iloc[1:,].pct_change() * 100
    yearly_change = (
        mean_df.filter(reduced_dates, axis=0).pct_change(periods=6).dropna() * 100
    )

    return monthly_change, yearly_change


def figure_maker_func(turkstat_data, analysis_data, freq):
    """Function for generating figures.

    Depending on the frequency of data appropriate title is assigned.

    Args:
        | turkstat_data(pd.Dataframe): the TurkStat dataset containing percentage
            changes with dates on the index
        | analysis_data (pd.Dataframe): the dataset containing percentage price
            changes with dates on the index
        | freq (str): frequency of data

    Returns:
        the figure and also saves it with appropriate title
    """

    if freq == "yearly":
        title = "Percentage Price Change Compared the Last Year's Same Month"
    elif freq == "monthly":
        title = "Monthly Percentage Price Change"

    plt.figure(figsize=[14, 5])
    plt.title(title)
    plt.ylabel("Percentage Change(%)")
    plt.plot(turkstat_data, "r-s", color="blue", linestyle="dashed")
    plt.plot(analysis_data, "r-s", color="red")
    plt.legend(labels=["Accomodation Services(TurkStat)", "Analysis(Airbnb)"])
    plt.grid()

    plt.savefig(ppj("OUT_FIGURES", f"{freq}_change_figure.png"))


if __name__ == "__main__":

    dates = sys.argv[1:]
    analysis_freq = ["monthly", "yearly"]

    pred_df = pd.DataFrame()
    for date in dates:
        with open(ppj("OUT_PREDICTION", f"{date}_prediction.csv"), "rb") as p:
            pred_iter = pd.read_csv(p)
            pred_df = pd.concat([pred_df, pred_iter], axis=1)

    for f in analysis_freq:
        with open(ppj("IN_DATA", f"TurkStat_data/{f}_change_ist.csv"), "rb") as tr:
            locals()["turkstat_" + f] = pd.read_csv(tr, sep="|", index_col=0)

    monthly_change, yearly_change = data_prep(pred_df)

    figure_maker_func(turkstat_monthly, monthly_change, freq="monthly")
    figure_maker_func(turkstat_yearly, yearly_change, freq="yearly")
