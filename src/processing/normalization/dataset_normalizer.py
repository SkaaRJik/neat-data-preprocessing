from abc import ABCMeta, abstractmethod
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class DatasetNormalizer(object):
    def __init__(self, scaler):
        self._scaler = scaler

    def normalize(self, file: str, log: bool = False) -> pd.DataFrame:
        csv: pd.DataFrame = pd.read_csv(file, sep=';')
        scaled_data = csv[csv.columns]
        log = log if scaled_data.values.min() > 0 else False
        if log:
            scaled_data = np.log(scaled_data)
        scaled_data = self._scaler.fit_transform(X=scaled_data)

        csv = pd.DataFrame(data=scaled_data, columns=csv.columns.values)
        return csv


    def denormalize(self, file: str) -> pd.DataFrame:
        csv: pd.DataFrame = pd.read_csv(file, sep=';')
        inversed = self._min_max_scaler.inverse_transform(X=csv[csv.columns])
        csv = pd.DataFrame(data=inversed, columns=csv.columns.values)
        return csv
