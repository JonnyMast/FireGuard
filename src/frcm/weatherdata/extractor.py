import abc

from frcm.datamodel.model import Observations, Forecast


class Extractor:
    @abc.abstractmethod
    def extract_observations(self, data: str) -> Observations:
        pass

    @abc.abstractmethod
    def extract_forecast(self, data: str) -> Forecast:
        pass



