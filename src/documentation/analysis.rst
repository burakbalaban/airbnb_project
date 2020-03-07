.. _analysis:

**************
Main Analysis
**************

Data management of Airbnb datasets constitutes the beginning of the main analysis. The columns in the Airbnb datasets are arranged according to files explained in the :ref:`specs` section and Shared rooms and property types rather than appartments are excluded from the analysis since the features of those offerings have a potential to mislead the results. After cleaning and rearranging the dataset, Extreme Gradient Boosting Algorithm is employed to train a model. Extreme Gradient Boosting is relatively more efficient regarding computational efficiency than other decision tree based methods and tree based methods are able to handle both numeric and categorical data properly :cite:`Chen`. Parameter hypertuning in small scale with scikit-learn package's RandomizedSearchCv is also added in the training process, a more extensive search could have been introduced yet requires more time and computer power :cite:`scikit-learn`. The :file:`generated_house_data.csv` explained in :ref:`data_generation` section is used for prediction. The analysis is done for every Airbnb dataset in **src/Airbnb_data/** and related predictions are stored in **bld/out/predicted_data** folder.

.. automodule:: src.analysis.analysis
    :members: