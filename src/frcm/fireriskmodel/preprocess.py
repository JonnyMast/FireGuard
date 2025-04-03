from frcm.datamodel.model import *
from frcm.fireriskmodel.parameters import delta_t
import numpy as np


def combine_obs_fct(sorted_data_obs, sorted_data_fct, parameter):
    obs = [getattr(obj, parameter) for obj in sorted_data_obs]
    fct = [getattr(obj, parameter) for obj in sorted_data_fct]
    combined = obs + fct
    return combined


def clean_nan(data_vector, time_vector):
    # Treat Data
    nan_indices = np.where(np.isnan(data_vector))
    data_cleaned = np.delete(data_vector, nan_indices)
    # Treat associated time_vector
    time_cleaned = np.delete(time_vector, nan_indices)
    return data_cleaned, time_cleaned


def find_data_gap(*args): # np.array
    max_delta = []
    for arr in args:
        differences = np.diff(arr)
        max_delta.append(np.max(differences))
    return np.max(max_delta)


def preprocess(wd: WeatherData):

    # Should not be necessary, but data is initially sorted according to the timestamps
    sorted_data_obs = sorted(wd.observations.data, key=lambda x: x.timestamp)
    sorted_data_fct = sorted(wd.forecast.data, key=lambda x: x.timestamp)

    # Combine data
    timestamp_vector = combine_obs_fct(sorted_data_obs, sorted_data_fct, 'timestamp')
    temp_vector = combine_obs_fct(sorted_data_obs, sorted_data_fct, 'temperature')
    humidity_vector = combine_obs_fct(sorted_data_obs, sorted_data_fct, 'humidity')
    wind_vector = combine_obs_fct(sorted_data_obs, sorted_data_fct, 'wind_speed')

    # Convert timestamp vector to a vector containing delta time of adjacent elements in seconds, starting at 0.
    timestamp_vector_sec = [round((timestamp - timestamp_vector[0]).total_seconds()) for timestamp in timestamp_vector]
    # Get start of computation as datetime
    start_time = timestamp_vector[0]

    # Identify position of np.nan values and remove from "parameter"_vector and associated "parameter"_timevector
    # Resulting vectors are used in the np interpolation function (np.interp)
    temp_clean, time_temp_clean = clean_nan(data_vector=temp_vector, time_vector=timestamp_vector_sec)
    humidity_clean, time_humidity_clean = clean_nan(data_vector=humidity_vector, time_vector=timestamp_vector_sec)
    wind_clean, time_wind_clean = clean_nan(data_vector=wind_vector, time_vector=timestamp_vector_sec)

    # Create interpolation time vector in seconds. This vector contains all the datapoints for which the np.interp-
    # function shall provide interpolated values.
    interpolation_timevector_sec = [i for i in range(timestamp_vector_sec[0], timestamp_vector_sec[-1] + 1, delta_t)]

    # Find largest gap in data. Currently only considering temperature and humidity. Delta is given in seconds.
    max_time_delta = find_data_gap(time_temp_clean, time_humidity_clean)

    # Interpolate all data
    temp_interpolated = np.interp(interpolation_timevector_sec, time_temp_clean, temp_clean)
    humidity_interpolated = np.interp(interpolation_timevector_sec, time_humidity_clean, humidity_clean)
    wind_interpolated = np.interp(interpolation_timevector_sec, time_wind_clean, wind_clean)

    return start_time, interpolation_timevector_sec, temp_interpolated, humidity_interpolated, wind_interpolated, max_time_delta

