.. _specs:

***************
Specifications
***************

There are five files in **src/specs** folder. Three of them are used in the data management process of Airbnb datasets. They contain column names of Airbnb dataset.

	* :file:`var_convert.txt`: indicates columns have f and t as data and need to be converted to 0 and 1.
	* :file:`var_exclude.txt`: indicates columns to be dropped and excluded from the analysis.
	* :file:`var_lengthen.txt`: indicates columns have string as datatype and length of data is included in the analysis.

The remaining two files are employed in the data generation process explained in the :ref:`data_generation` section.

	* :file:`features_categorical.txt`: indicates categorical features and values of those columns can have.
	* :file:`features_min_max.txt`: includes columns with numerical data and, minimum and maximum values of those features.