from abc import ABCMeta, abstractmethod
import pandas as pd

class DatasetVerification(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def verify_excel(file: str) -> (list, list, dict, list, list, str, list, list, list, pd.DataFrame):
        """verify processing dataset format"""

    @abstractmethod
    def verify_csv(file: str) -> (list, list, dict, list, list, str, list, list, list, pd.DataFrame):
        """verify csv dataset format"""
