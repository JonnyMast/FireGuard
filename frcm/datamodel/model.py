import datetime

from pydantic import BaseModel


class Location(BaseModel):

    latitude: float
    longitude: float


class WeatherDataPoint(BaseModel):

    temperature: float
    humidity: float
    wind_speed: float
    timestamp: datetime.datetime

    def __str__(self):

        format_str = f'WeatherData[{self.timestamp}] {self.temperature, self.humidity, self.wind_speed}]'

        return format_str


class Observations(BaseModel):

    source: str
    location: Location
    data: list[WeatherDataPoint]

    def __str__(self):
        format_str = f'Observations [Source: {self.source} @ Location: {self.location}]\n'

        # Join all data points using '\n' as a separator
        data_strings = '\n'.join(map(str, self.data))

        return format_str + data_strings + '\n'


class Forecast(BaseModel):

    location: Location
    data: list[WeatherDataPoint]

    def __str__(self):
        format_str = f'Forecast @ Location: {self.location}\n'

        # Join all data points using '\n' as a separator
        data_strings = '\n'.join(map(str, self.data))

        return format_str + data_strings + '\n'


class WeatherData(BaseModel):

    created: datetime.datetime

    observations: Observations
    forecast: Forecast

    def to_json(self):
        return self.model_dump_json()


class FireRisk(BaseModel):

    timestamp: datetime.datetime
    ttf: float
    wind_speed: float

    def __str__(self):
        format_str = f'FireRisks[{self.timestamp} TTF({self.ttf}) WindSpeed({self.wind_speed})]'

        return format_str


class FireRiskPrediction(BaseModel):

    location: Location
    firerisks: list[FireRisk]

    def __str__(self):
        format_str = f'FireRiskPrediction[{self.location}]\n'

        # Generate list of formatted data points
        data_str = [str(data_point) for data_point in self.firerisks]

        # Join the list of formatted data points
        format_str += '\n'.join(data_str)

        return format_str
