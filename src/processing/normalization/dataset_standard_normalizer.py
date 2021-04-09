from decimal import Decimal

import pandas as pd
from numpy import ndarray
import numpy as np
from sklearn.preprocessing import StandardScaler

from src.processing.normalization.dataset_normalizer import DatasetNormalizer


class DatasetStandardNormalizer(DatasetNormalizer):


    def __init__(self):
        super().__init__(StandardScaler())

