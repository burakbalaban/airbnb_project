.. _data_management:

***************
Data Management
***************

The Foursquare data explained in :ref:`data` section contains check-in and venue information seperately and in global scale. Only venues in Istanbul and their check-in counts are needed for the analysis. Venue data has a country indicator, yet there is no information about the city, only the coordinates are available. After eliminating private houses, by using longitute and latitute information venues within Istanbul's boundaries are filtered. For the north and south boundaries, straight lines are used since there is not another city in the South or North of Istanbul but only sea. For eastern and western boundaries, two straight lines with constant slope are employed. Using the check-in information every venues' check-in count is calculated and venues with less than a check-in per day on average are excluded. The information of venues' coordinates and check-in counts are stored in :file:`reduced_check_in_dataset.csv`.

.. automodule:: src.data_management.data_management_checkin
    :members:
