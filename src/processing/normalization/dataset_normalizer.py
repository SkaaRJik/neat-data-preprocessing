from abc import ABCMeta, abstractmethod

import numpy
import pandas as pd
import numpy as np
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.preprocessing import MinMaxScaler


class DatasetNormalizer(object):
    def __init__(self, scaler: (TransformerMixin, BaseEstimator)):
        self._scaler: (TransformerMixin, BaseEstimator) = scaler

    def normalize(self, file: str, log: bool = False) -> pd.DataFrame:
        csv: pd.DataFrame = pd.read_csv(file, sep=';')
        scaled_data = csv[csv.columns]
        log = log if scaled_data.values.min() > 0 else False
        if log:
            scaled_data = np.log(scaled_data)
        scaled_data = self._scaler.fit_transform(X=scaled_data)

        csv = pd.DataFrame(data=scaled_data, columns=csv.columns.values)
        return csv


    def denormalize(self, dataframe_to_denormolize: pd.DataFrame, source_data_frame: pd.DataFrame,log: bool = False) -> pd.DataFrame:




        for column_name in dataframe_to_denormolize.columns.values:
            source_column = source_data_frame[column_name].to_numpy()
            if log:
                source_column = np.log(source_column)
            source_column = self._scaler.fit_transform(source_column.reshape(-1, 1))
            inversed = self._scaler.inverse_transform(dataframe_to_denormolize[column_name].to_numpy().reshape(-1, 1))
            if log:
                inversed = np.exp(inversed.reshape(-1))
            dataframe_to_denormolize[column_name] = inversed

        return dataframe_to_denormolize
        # source_ndarray =  []
        # predicted_ndarray = []
        #
        #
        # for column_name in dataframe_to_denormolize.columns.values:
        #     source_ndarray.append(source_data_frame[column_name].to_numpy())
        #     predicted_ndarray.append(dataframe_to_denormolize[column_name].to_numpy())
        #
        # source_ndarray = numpy.transpose(source_ndarray)
        # predicted_ndarray = numpy.transpose(predicted_ndarray)
        #
        #
        #
        #
        #
        #
        # if log:
        #     source_ndarray = np.log(source_ndarray)
        # source_ndarray = self._scaler.fit_transform(X=source_ndarray)
        #
        # inversed = self._scaler.inverse_transform(X=predicted_ndarray)
        #
        # if log:
        #     inversed = np.exp(inversed)
        #
        # inversed: pd.DataFrame = pd.DataFrame(data=inversed, columns=dataframe_to_denormolize.columns.values)
        # return inversed
