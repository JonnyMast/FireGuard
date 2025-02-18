import datetime

from frcm.datamodel.model import FireRiskPrediction, Location, WeatherData, Observations, Forecast
from frcm.weatherdata.client import WeatherDataClient
import frcm.fireriskmodel.compute

from frcm.weatherdata.client_met import METClient
from frcm.weatherdata.extractor_met import METExtractor


class FireRiskAPI:

    def __init__(self, client: WeatherDataClient):
        self.client = client
        self.timedelta_ok = datetime.timedelta(days=1) # TODO: when during a day is observations updated? (12:00 and 06:00)
        # TODO (NOTE): Short term forecast updates every 3rd hour with long term forecast every 12th hour at 12:00 and 06:00
        self.interpolate_distance = 720

    def compute(self, wd: WeatherData) -> FireRiskPrediction:

        return frcm.fireriskmodel.compute.compute(wd)

    def get_wd_observations_to_now(self, location: Location, time_now, obs_delta: datetime.timedelta) -> Observations:

        start_time = time_now - obs_delta

        observations = self.client.fetch_observations(location=location, start=start_time, end=time_now)

        return observations

    def get_wd_forecast_from_now(self, location: Location) -> Forecast:

        forecast = self.client.fetch_forecast(location)

        return forecast

    def get_wd_now(self, location: Location, obs_delta: datetime.timedelta) -> WeatherData:

        time_now = datetime.datetime.now()

        observations = self.get_wd_observations_to_now(location, time_now, obs_delta)

        # print(observations)

        forecast = self.get_wd_forecast_from_now(location)

        # print(forecast)

        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)

        return wd

    def compute_now(self, location: Location, obs_delta: datetime.timedelta) -> FireRiskPrediction:

        wd = self.get_wd_now(location, obs_delta)

        # print(wd.to_json())

        prediction = self.compute(wd)

        return prediction

    def compute_now_period(self, location: Location, obs_delta: datetime.timedelta, fct_delta: datetime.timedelta):
        pass

    def compute_period(self, location: Location, start: datetime, end: datetime) -> FireRiskPrediction:
        pass

    def compute_period_delta(self, location: Location, start: datetime, delta: datetime.timedelta) -> FireRiskPrediction:
        pass


class METFireRiskAPI:

    def __init__(self):
        self.met_extractor = METExtractor()

        self.met_client = METClient(extractor=self.met_extractor)

        self.frc = FireRiskAPI(client=self.met_client)

    def get_weatherdata_now(self, location: Location, obs_delta: datetime.timedelta) -> WeatherData:

        wd = self.frc.get_wd_now(location, obs_delta)

        return wd

    def compute(self, wd: WeatherData) -> FireRiskPrediction:
        return self.frc.compute(wd)

    def compute_now(self, location: Location, obs_delta: datetime.timedelta) -> FireRiskPrediction:
        return self.frc.compute_now(location, obs_delta)

