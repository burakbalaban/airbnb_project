import json
import re

import numpy as np
import pandas as pd

from bld.project_paths import project_paths_join as ppj

# Number of observations to generate
obs_size = 20

# Seed determination for reproducibility
np.random.seed(19)

if __name__ == "__main__":

    # Load data
    # House features that has numerical values
    with open(ppj("IN_SPECS", "features_min_max.txt"), "rb") as f:
        features_dict_min_max = json.load(f)

    # Categorical features of Houses
    with open(ppj("IN_SPECS", "features_categorical.txt"), "rb") as f:
        features_categorical = json.load(f)

    # Features that approaximately follow chi square distribution
    chi_squ_list = [
        "host_listings_count",
        "accommodates",
        "cleaning_fee",
        "guests_included",
        "extra_people",
    ]

    generated_data = pd.DataFrame()

    # Random generation of numeric features
    for col in features_dict_min_max.keys():
        min, max = features_dict_min_max[col]

        if col in chi_squ_list:
            obs_list = np.random.chisquare(1, obs_size)
            obs_list *= np.exp(obs_list)
            obs_list *= max / np.max(obs_list)
            obs_list += min

        # Review features follow approximately reversed chi square distribution
        elif not re.match(r"^review", col) is None:
            obs_list = np.random.chisquare(1, obs_size)
            obs_list = max - obs_list

        else:
            obs_list = np.random.randint(low=min, high=max + 1, size=obs_size)

        generated_data[col] = list(map(int, obs_list))

    # Random generation of categorical features
    for col in features_categorical.keys():
        generated_data[col] = np.random.choice(
            features_categorical[col], size=obs_size, replace=True
        )

    # Out data
    with open(ppj("OUT_DATA", "generated_house_data.csv"), "w") as out_file:
        generated_data.to_csv(out_file, index=False)
