.. _data_generation:

***************
Data Generation
***************

The :file:`house_data_generation.py` file randomly generates house features to be used in prediction part of analysis. The number of houses to be generated and random seed can be adjusted in the py file. There are two types of columns to be generated; columns with categorical data and numerical data. The values for categorical data and, minimum and maximum values of numerical data are contained in the **src/specs** folder and explained in :ref:`specs` section. Numpy package is used for random generation of values. For categorical data, random sample follows a uniform distribution. For the numerical samples there are three different distributions are used; discrete uniform, chi squared and reversed chi squared. Reversed chi square is that most of the occurences are close to a pre-defined maximum and occurences decrease if they are closer to zero. Given the Airbnb datasets, if a feature strictly follows a chi square or reversed chi square distribution, random generation process employs such distribution. That decision making process is done in the data exploring phase of the project and not included in the file. The generated data is stored in :file:`generated_house_data.csv`.

.. automodule:: src.data_generation.house_data_generation
    :members: