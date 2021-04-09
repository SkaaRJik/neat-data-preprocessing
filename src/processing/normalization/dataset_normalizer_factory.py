from src.processing.normalization.dataset_normalizer import DatasetNormalizer

from src.processing.normalization.dataset_min_max_normalizer import DatasetMinMaxNormalizer
from src.processing.normalization.dataset_standard_normalizer import StandardScaler


class DatasetNormalizerFactory(object):

    def __init__(self):
        self._minMaxNormalizer: DatasetNormalizer = DatasetMinMaxNormalizer()
        self._standardNormalizer: DatasetNormalizer = StandardScaler()

    def getNormalizer(self, name: str) -> DatasetNormalizer:
        switch = {
            "minMax": self._minMaxNormalizer,
            "standard": self._standardNormalizer
        }
        return switch.get(name)


dataset_normalizer_factory = DatasetNormalizerFactory()