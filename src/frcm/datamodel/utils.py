import datetime
import dateutil.parser

import frcm.datamodel.model as dm


def min_time(data: list[dm.WeatherDataPoint]):
    # assume that data is time sorted in ascending order and non-empty
    return data[0].timestamp


def max_time(data: list[dm.WeatherDataPoint]):
    # assume that data is time sorted in ascending order and non-empty
    return data[-1].timestamp


def is_sorted(data: list[dm.WeatherDataPoint]) -> bool:
    i = 1
    ascending = True

    while i < len(data) and ascending:
        ascending = data[i].timestamp > data[i - 1].timestamp

        i = i + 1

    return ascending


def within_timedelta(data: list[dm.WeatherDataPoint], max_delta: datetime.timedelta) -> bool:
    i = 1
    violated = False

    while i < len(data) and (not violated):
        violated = (data[i].timestamp - data[i - 1].timestamp) < max_delta

        i = i + 1

    return violated


def dict_to_wdp(wdp) -> dm.WeatherDataPoint:

    wdp = dm.WeatherDataPoint(
        temperature=wdp['temperature'],
        humidity=wdp['humidity'],
        wind_speed=wdp['wind_speed'],
        timestamp=dateutil.parser.parse(wdp['timestamp']))

    return wdp


def list_to_wdps(wdps) -> list[dm.WeatherDataPoint]:

    return list(map(dict_to_wdp, wdps))


def wdps_list_str(wdps : list[dm.WeatherDataPoint]) -> str:
    # TODO: current string concatenation is inefficient
    format_str = ''
    for wdp in wdps:
        format_str = format_str + str(wdp) + '\n'

    return format_str


# TODO: validate could possibly raise different exceptions depending on violation
# TODO: check also that created is between max_time and min_time
# TODO: check that the required data is also present in the data points

def wd_validate(wd: dm.WeatherData, max_delta: datetime.timedelta):

    max_time_obs = max_time(wd.observations.data)
    min_time_fct = min_time(wd.forecast.data)

    is_sorted_obs = is_sorted(wd.observations.data)
    is_sorted_fct = is_sorted(wd.forecast.data)

    is_delta_obs = within_timedelta(wd.observations.data, max_delta)
    is_delta_fct = within_timedelta(wd.forecast.data, max_delta)

    return ((max_time_obs < min_time_fct) and
            is_sorted_obs and is_sorted_fct and
            is_delta_obs and is_delta_fct and
            (max_time_obs - min_time_fct) < max_delta)
