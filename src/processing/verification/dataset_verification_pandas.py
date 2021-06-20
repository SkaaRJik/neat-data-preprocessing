import numpy as np
import pandas as pd
from pandas import ExcelFile, DataFrame
from sklearn.impute import SimpleImputer

from src.processing.verification.dataset_verification import DatasetVerification


class DatasetVerificationPandas(DatasetVerification):
    _ERROR_VALUE_IS_STRING = 'ERROR_VALUE_IS_STRING'
    _ERROR_VALUES_IS_EMPTY = 'ERROR_VALUES_IS_EMPTY'
    _ERROR_VALUE_IS_NOT_NUMERIC = 'ERROR_VALUE_IS_NOT_NUMERIC'
    _ERROR_LEGEND_INCREMENT_EQUALS_ZERO = 'ERROR_INCREMENT_VALUE_EQUALS_ZERO'
    _ERROR_VALUES_IS_NOT_INCREMENTAL = 'ERROR_VALUES_IS_NOT_INCREMENTAL'
    _ERROR_MISMATCH_NUMBER_OF_HEADERS_AND_NUMBER_OF_DATA = 'ERROR_MISMATCH_NUMBER_OF_HEADERS_AND_NUMBER_OF_DATA'
    _INFO_VALUE_WAS_PREDICTED = 'INFO_VALUE_WAS_PREDICTED'
    _ERROR_COLUMN_NAME_IS_EMPTY = 'ERROR_COLUMN_NAME_IS_EMPTY'
    _ERROR_LEGEND_COLUMN_NAME_IS_EMPTY = 'ERROR_LEGEND_COLUMN_NAME_IS_EMPTY'


    def __init__(self):
        pass

    # print(df.values[0]) #Чтение построчно в виде массива
    # print(df.loc[1]) #Чтение построчно
    # print(df.columns.values) #Чтение заголовков в виде массива
    # print(df[df.columns.values[0]].values) #Чтение заголовков в виде массива
    def verify_excel(self, file) -> (list, list, dict, list, list, str, list, list, list, int, pd.DataFrame):
        xls: ExcelFile = pd.ExcelFile(file)
        df: DataFrame = xls.parse(0, parse_dates=False)
        df.columns = df.columns.str.strip()
        return self._verify(df)

        # Load a sheet into a DataFrame by name: df1
        # df1 = xl.parse(xl.sheet_names[0])
        #
        # print(df1[0])

    def verify_csv(self, file: str) -> (list, list, dict, list, list, str, list, list, list, int, pd.DataFrame):
        xl = pd.read_csv(file)
        pass

    def _verify(self, df: pd.DataFrame) -> (list, list, dict, list, list, str, list, list, list, int, pd.DataFrame):
        legend_values: list = df[df.columns.values[0]].values
        headers: list = df.columns.values
        legend_error_protocol, legend_info_protocol, legend_inc = self._parse_legend_values(legend_values)
        headers_error_protocol, legend_header, data_headers = self._parse_headers(headers,
                                                                                  len(df[df.columns.values[1:]].T))
        values_error_protocol, values_info_protocol, df = self._parse_values(df)
        rows = df.shape[0]
        return legend_error_protocol, legend_info_protocol, legend_inc, legend_values.tolist(), headers_error_protocol, legend_header, \
               data_headers, values_error_protocol, values_info_protocol, rows,df[df.columns.values[1:]]

    def _parse_legend_values(self, legend_values: list) -> (list, list, dict):
        legend_inc = {'increment': 0, 'type': None}
        has_error = False
        error_protocol = []
        info_protocol = []

        if len(legend_values) == 0:
            error_protocol.append({'position': 0, 'error': self._ERROR_VALUES_IS_EMPTY})
            return error_protocol, info_protocol, legend_inc

        if has_error:
            return error_protocol, legend_inc

        legend_diff = 0

        for i, legend_value in enumerate(legend_values):
            if isinstance(legend_value, str):
                error_protocol.append({'position': i+1, 'error': self._ERROR_VALUE_IS_STRING})
                return error_protocol, info_protocol, legend_inc


        skip = 0
        for i in range(len(legend_values) - 1, 0, -1):
            if pd.isnull(legend_values[i]):
                skip += 1
            else:
                legend_diff = legend_values[i]
                break

        for i in range(0, len(legend_values) - 1):
            if pd.isnull(legend_values[i]):
                skip += 1
            else:
                legend_diff -= legend_values[i]
                break

        inc = legend_diff / (len(legend_values) - 1 - skip)

        if inc == 0 or inc is None or pd.isnull(inc):
            error_protocol.append({'position': 0, 'error': self._ERROR_LEGEND_INCREMENT_EQUALS_ZERO})

        for i in range(0, len(legend_values) - 1):
            if pd.isnull(legend_values[i]):
                predicted = False
                if (i - 1 >= 0):
                    if not pd.isnull(legend_values[i - 1]):
                        legend_values[i] = legend_values[i - 1] + inc
                        predicted = True
                        info_protocol.append({'position': i + 1, 'message': self._INFO_VALUE_WAS_PREDICTED})
                if (i + 1 < len(legend_values) and not predicted):
                    if not pd.isnull(legend_values[i + 1]):
                        legend_values[i] = legend_values[i + 1] - inc
                        info_protocol.append({'position': i + 1, 'message': self._INFO_VALUE_WAS_PREDICTED})
            if pd.isnull(legend_values[i]):
                error_protocol.append({'position': i + 1, 'error': self._ERROR_VALUES_IS_NOT_INCREMENTAL})

        legend_inc = {'increment': inc, 'type': str(type(legend_values[0]))}

        return error_protocol, info_protocol, legend_inc

    def _parse_headers(self, headers: list, data_size: int) -> (dict, str, list):

        error_protocol = []
        header: str
        for header in headers[1:]:
            if 'Unnamed' in header:
                error_protocol.append({'error': self._ERROR_COLUMN_NAME_IS_EMPTY})
                break


        if 'Unnamed' in headers[0]:
            error_protocol.append({'error': self._ERROR_LEGEND_COLUMN_NAME_IS_EMPTY})



        if len(headers[1:]) != data_size:
            error_protocol.append({'error': self._ERROR_MISMATCH_NUMBER_OF_HEADERS_AND_NUMBER_OF_DATA})

        return error_protocol, headers[0], headers[1:].tolist()

    def _parse_values(self, df: pd.DataFrame) -> (dict, dict, pd.DataFrame):
        error_protocol = []
        info_protocol = []

        imp = SimpleImputer(missing_values=np.nan, strategy="mean")  # specify axis

        for column in df.columns[1:]:
            nan_position = -1
            was_error = False
            for i in range(0, len(df[column]) - 1):
                if pd.isnull(df[column].values[i]):
                    nan_position = i
            try:
                df[column] = imp.fit_transform(df[[column]]).ravel()
            except BaseException:
                was_error = True
                error_protocol.append({'error': self._ERROR_VALUE_IS_NOT_NUMERIC, 'columnName': column})
            if (not was_error and nan_position != -1):
                info_protocol.append(
                    {'message': self._INFO_VALUE_WAS_PREDICTED, 'columnName': column, 'position': nan_position})

        return error_protocol, info_protocol, df
