import abc

from frcm.datamodel.model import *


class WeatherDataClient:

    # TODO: add variants for time period on observations and timedelta on forecast

    @abc.abstractmethod
    def fetch_observations(self, location: Location) -> Observations:
        pass

    @abc.abstractmethod
    def fetch_forecast(self, location: Location) -> Forecast:
        pass
