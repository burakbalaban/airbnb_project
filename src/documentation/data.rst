.. _data:

*************
Data
*************

There are three files in **src/data**: Airbnb_data, Foursquare_data and TurkStat_data.

Airbnb data
===========

The monthly data for Airbnb listings in Istanbul is from April 2018 up to November 2019 except May and June 2018, thus there are 18 files. The name of each file indicates the scraping date of the dataset meaning that the dataset includes all the houses in Istanbul offered on that date. It includes house features including the number of rooms, beds, utilities offered, its location, its price and many others.

The Airbnb data is retrieved from insideairbnb website and further information regarding scraping methodology and the data can be found on the website :cite:`insideairbnb`.

Foursquare data
===============

This dataset needs to be downloaded from https://drive.google.com/file/d/0BwrgZ-IdrTotZ0U0ZER2ejI3VVk :cite:`yang2016participatory`. A detalied explanation can be found in the zip file. The downloaded files need to be placed in **src/data/Foursquare_data** folder. Among those files two are used in the analysis part:

	* :file:`dataset_TIST2015_Checkins.txt`: contains check in information of users alongside with time and venue.

	* :file:`dataset_TIST2015_POIs.txt`: contains location information about venues.

TurkStat data
=============

The data is retrieved from Central Dissemination System of Turkish Statistical Institute :cite:`TurkStat`. Only Accommodation Services part in the Consumer Price Index in Istanbul is considered. Data gathering and calculation methods can be found on TurkStat's website. There are two files in the directory;

	* :file:`monthly_change_ist.csv`: contains the monthly percentage change in Accommodation Service's prices in Istanbul starting from August 2018 until December 2019.

	* :file:`yearly_change_ist.csv`: contains the change in Accommodation Service's prices based on last year's same month in Istanbul starting from April 2019 until December 2019.