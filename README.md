# The Verification of Inflation using Airbnb Data in Istanbul
### by Burak Balaban
This project using multiple dataset containing Airbnb listings in Istanbul tries to examine and verify the change in Accommodation Services, a part of Inflation. As being the most populated city, Istanbul offers many accommodation options including Airbnb. The assumption is change in Accommodation services should reflect the change in Airbnb prices. Ultimately, this project produces two figures and a paper explaning those.

## Usage
- Download the datasets mentioned in notes and place it in data folder.
- Create environment using environment.yaml with `conda env create -f environment.yaml`.
- Run `python waf.py configure`.
- Run `python waf.py build`.
- The detailed documentation about the project will be generated in **bld/src/documentation**.

## Data
This project uses datasets from three different resources.
- The dataset including house features are obtained from [insideairbnb website](http://insideairbnb.com/).
- The data on Accommodation Services as a part of the Consumer Price Index is retrieved from [Turkish Statistical Institute](http://www.turkstat.gov.tr)'s [Central Dissemination System](https://biruni.tuik.gov.tr/medas/?kn=84&locale=en).
- The data containing check-in counts and venue information is retrieved from [Dingqi Yang's website](https://sites.google.com/site/yangdingqi/home/foursquare-dataset).

## Model
For modelling and predicting Extreme Gradient Boosting(XGBoost) is used.

## Important Notes
- Dependencies are included in the **environment.yaml**, thus, it is advised that before running the code create an environment using that file.
- Since two datasets exceed the storage limit, *dataset_TIST2015_Checkins.txt* and *dataset_TIST2015_POIs.txt* need to be downloaded from [here](https://drive.google.com/file/d/0BwrgZ-IdrTotZ0U0ZER2ejI3VVk) and placed into **src/data/Foursquare_data** directory.

## References

Inside Airbnb. Inside airbnb. Adding data to the debate. 2019. Online; accessed 10 February 2020.

Turkish Statistical Institute. Consumer Price Index. Online; accessed 10 February 2020.

Dingqi Yang, Daqing Zhang, and Bingqing Qu. Participatory cultural mapping based on collective behavior data in location-based social networks. ACM Transactions on Intelligent Systems and Technology (TIST), 7(3):1–23, 2016.
