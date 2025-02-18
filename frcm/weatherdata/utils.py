import dateutil.parser

from frcm.datamodel.model import WeatherDataPoint


def weatherdata_parse(datadict) -> list[WeatherDataPoint]:

    data = list()

    for item in datadict:

        temperature = item['temperature']
        humidity = item['humidity']
        wind_speed = item['wind_speed']
        timestamp = dateutil.parser.parse(item['timestamp'])

        wd_point = WeatherDataPoint(temperature=temperature,
                                    humidity=humidity,
                                    wind_speed=wind_speed,
                                    timestamp=timestamp)

        data.append(wd_point)

    return data

