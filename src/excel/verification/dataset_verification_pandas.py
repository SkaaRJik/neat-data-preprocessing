import datetime

from pandas import ExcelFile, DataFrame

from src.excel.verification.dataset_verification import DatasetVerification
import pandas as pd
import numpy as np


class DatasetVerificationPandas(DatasetVerification):
    _ERROR_VALUE_IS_STRING = 'ERROR_VALUE_IS_STRING'
    _ERROR_LEGEND_INCREMENT_EQUALS_ZERO = 'ERROR_INCREMENT_VALUE_EQUALS_ZERO'

    def __init__(self):
        pass

    # print(df.values[0]) #Чтение построчно в виде массива
    # print(df.loc[1]) #Чтение построчно
    # print(df.columns.values) #Чтение заголовков в виде массива
    # print(df[df.columns.values[0]].values) #Чтение заголовков в виде массива
    def verify_excel(self, file: str):
        xls: ExcelFile = pd.ExcelFile(file)
        df: DataFrame = xls.parse(0, parse_dates=False)

        legend_values: list = df[df.columns.values[0]].values
        self._verify(legend_values)

        # Load a sheet into a DataFrame by name: df1
        # df1 = xl.parse(xl.sheet_names[0])
        #
        # print(df1[0])

    def verify_csv(self, file: str):
        xl = pd.read_csv(file)
        pass

    def _verify(self, legend_values: list):
        legend_error_protocol, legend_inc = self._parseLegendValues(legend_values)
        print(legend_error_protocol, legend_inc)


    def _parseLegendValues(self, legend_values: list):
        legend_inc = {'increment': 0, 'type': None}
        has_error = False
        error_protocol = []

        if len(legend_values) == 0:
            error_protocol.append({'position': 0, 'error': self._ERROR_VALUE_IS_STRING})
            return error_protocol, legend_inc

        for i in range(0, len(legend_values) - 1):
            if type(legend_values[i]) is str:
                has_error = True
                error_protocol.append({'position': i + 1, 'error': self._ERROR_VALUE_IS_STRING})

        if has_error:
            return error_protocol, legend_inc

        legend_diff = 0

        for i in range(len(legend_values) - 1, 1, -1):
            legend_diff += legend_values[i] - legend_values[i - 1]

        inc = legend_diff / len(legend_values)

        if type(legend_values[0]) is np.int64:
            inc = round(legend_inc)

        if inc == 0 or inc is None:
            error_protocol.append({'position': 0, 'error': self.ERROR_INCREMENT_VALUE_EQUALS_ZERO})

        legend_inc = {'increment': inc, 'type': type(legend_values[0])}

        return error_protocol, legend_inc
