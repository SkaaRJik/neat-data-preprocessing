from abc import ABCMeta, abstractmethod


class DatasetVerification(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def verify_excel(file: str):
        """verify excel dataset format"""

    def verify_csv(file: str):
        """verify csv dataset format"""
