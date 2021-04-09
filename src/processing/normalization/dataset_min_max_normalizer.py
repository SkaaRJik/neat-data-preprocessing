from decimal import Decimal

import pandas as pd
from numpy import ndarray
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from src.processing.normalization.dataset_normalizer import DatasetNormalizer


class DatasetMinMaxNormalizer(DatasetNormalizer):

    def __init__(self):
        super().__init__(MinMaxScaler(feature_range=(0.4, 0.6)))

