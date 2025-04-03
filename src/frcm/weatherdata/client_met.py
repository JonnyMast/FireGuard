import requests
import datetime
import json

# see .env.example.py in the root dir.
from decouple import config

from frcm.weatherdata.client import WeatherDataClient
from frcm.weatherdata.extractor import Extractor
from frcm.datamodel.model import Location, Observations, Forecast


class METClient(WeatherDataClient):

    def __init__(self, extractor: Extractor):

        self.forecast_endpoint = 'https://api.met.no/weatherapi/locationforecast/2.0/compact.json'

        self.observations_endpoint = 'https://frost.met.no/observations/v0.jsonld'
        self.sources_endpoint = 'https://frost.met.no/sources/v0.jsonld'

        self.MET_CLIENT_ID = config('MET_CLIENT_ID')
        self.MET_CLIENT_SECRET = config('MET_CLIENT_SECRET')

        self.extractor = extractor

    def send_met_request(self, parameters):

        header = {'User-Agent': 'DYNAMIC Firerisk Model'}

        response = requests.get(self.forecast_endpoint,
                                headers=header,
                                params=parameters,
                                auth=(self.MET_CLIENT_ID, self.MET_CLIENT_SECRET))

        return response

    def fetch_forecast_raw(self, location: Location):

        parameters = {'lat': str(location.latitude),
                      'lon': str(location.longitude)
                      }

        response = self.send_met_request(parameters)

        return response

    def fetch_forecast(self, location: Location) -> Forecast:

        response = self.fetch_forecast_raw(location)

        forecast = self.extractor.extract_forecast(response.text)

        return forecast

    def send_frost_request(self, endpoint, parameters):

        response = requests.get(endpoint,
                                params=parameters,
                                auth=(self.MET_CLIENT_ID, self.MET_CLIENT_SECRET))

        return response

    def get_nearest_station_raw(self, location: Location):
        parameters = {
            'types': 'SensorSystem',
            'elements': 'air_temperature,relative_humidity,wind_speed',
            'geometry':  f'nearest(POINT({location.longitude} {location.latitude}))'}

        response = self.send_frost_request(self.sources_endpoint, parameters)

        return response

    def get_nearest_station_id(self, location: Location) -> str:

        # TODO: more error handling here

        frost_response = self.get_nearest_station_raw(location)

        frost_response_str = frost_response.text

        station_response = json.loads(frost_response_str)

        station_id = station_response['data'][0]['id']

        return station_id

    @staticmethod
    def format_date(dt: datetime.datetime):

        return dt.strftime('%Y-%m-%d')

    @staticmethod
    def format_period(start: datetime.datetime, end: datetime.datetime):

        start_date = METClient.format_date(start)

        end_date = METClient.format_date(end)

        timeperiod = f'{start_date}/{end_date}'

        return timeperiod

    def fetch_observations_raw(self, source: str, start: datetime.datetime, end: datetime.datetime):

        time_period = METClient.format_period(start, end)

        print(f'Fetch observation : {time_period}')

        parameters = {'sources': source,
                      'referencetime': time_period,
                      'elements': 'air_temperature,relative_humidity,wind_speed'
                      }

        response = self.send_frost_request(self.observations_endpoint, parameters)

        return response

    def fetch_observations(self, location: Location, start: datetime.datetime, end: datetime.datetime) -> Observations:

#        print(location)

        station_id = self.get_nearest_station_id(location)

#        print(station_id)

        response = self.fetch_observations_raw(station_id, start, end)

#        print(response.text)

        observations = self.extractor.extract_observations(response.text, location)

        return observations
