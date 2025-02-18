import numpy as np
import datetime

import frcm.datamodel.model as dm
import frcm.fireriskmodel.parameters as mp
import frcm.fireriskmodel.utils as func
import frcm.fireriskmodel.preprocess as pp


def compute(wd: dm.WeatherData) -> dm.FireRiskPrediction:

    # Get interpolated values #TODO (NOTE) The max_time_delta represents the largest gap in missing data (seconds). It can be used to provide suited warning/error message.
    start_time, time_interpolated_sec, temp_interpolated, humidity_interpolated, wind_interpolated, max_time_delta = pp.preprocess(wd)
    comp_loc = wd.forecast.location

    # Compute RH_in and TTF
    rh_in, ttf = compute_fr(temp_interpolated, humidity_interpolated)

    # Reduce data to once per hour, but the time is still given as seconds
    rf = int(
        3600 / mp.delta_t)  # Reduction factor, i.e., how many intervals per hour. Default delta_t = 720 s, hence rf = 5.
    rh_in_hour = rh_in[::rf]  # Average is not computed, values are extracted per hour.
    ttf_in_hour = ttf[::rf]
    time_in_hour = time_interpolated_sec[::rf] # Time is still in seconds but given for every hour.
    wind_speed_in_hour = wind_interpolated[::rf]

    # Create response according to datamodel
    firerisks = []
    for i in range(len(rh_in_hour)):
        timestamps = start_time + datetime.timedelta(seconds=time_in_hour[i])
        firerisk_i = dm.FireRisk(timestamp=timestamps, ttf=ttf_in_hour[i], wind_speed=wind_speed_in_hour[i])
        firerisks.append(firerisk_i)

    FireRiskResponse = dm.FireRiskPrediction(location=comp_loc, firerisks=firerisks)

    return FireRiskResponse


def compute_fr(temp_c_out, rh_out):

    "Indoor temperature vector"
    temp_c_in = [mp.T_c_in] * len(temp_c_out)  # Potential future changes may involve dynamic in-home temperatures

    """ compute saturation vapor pressures and water concentrations, outdoor and indoor """
    # w = water, sat = saturation
    pw_sat_out = list(map(func.calc_pwsat, temp_c_out))
    cw_sat_out = list(map(func.calc_cwsat, pw_sat_out, temp_c_out))
    cw_out = list(map(func.calc_cw, rh_out, cw_sat_out))
    pw_sat_in = list(map(func.calc_pwsat, temp_c_in))
    cw_sat_in = list(map(func.calc_cwsat, pw_sat_in, temp_c_in))

    # ventilation variables
    ach = list(map(func.calc_ach, temp_c_out, temp_c_in))
    beta = list(map(func.calc_beta, ach))

    # calculate supply per timestep and make a supply vector (for future updates - currently containing constant values)
    supply_pts = (mp.supply_24h / (24 * 3600)) * mp.delta_t
    supply = [supply_pts] * len(temp_c_out)

    """ create wall array and vector """

    # wall array - storing fmc values - rows represent a step in time, columns represent wooden panel layers.
    wall = np.zeros(shape=(len(temp_c_out), mp.sub_layers))
    # used to update the wall array
    wall_vector = np.zeros(mp.sub_layers)

    # initial fmc value in wooden panels
    initial_fmc = func.calc_fmc(mp.RH_in) * mp.rho_wood

    """ placeholders """
    # shall contain wooden surface fmc values
    surface = np.zeros(len(temp_c_out))
    # shall contain wooden surface (boundary layer) rh values
    rh_wall = np.zeros(len(temp_c_out))
    # shall contain bulk air (in-home) rh values
    rh_in = np.zeros(len(temp_c_out))
    # shall contain bulk air (in-home) water concentrations
    cw_in = np.zeros(len(temp_c_out))
    # shall contain water concentration difference between rh_wall and rh_in
    delta_c = np.zeros(len(temp_c_out))
    # shall contain water concentration (contribution) per timestep from wooden surfaces
    c_wall = np.zeros(len(temp_c_out))


    # set initial conditions
    wall[0] = [initial_fmc] * mp.sub_layers
    surface[0] = func.calc_surf(wall[0][0], wall[0][1])
    rh_wall[0] = func.calc_rhwall(surface[0])
    rh_in[0] = mp.RH_in
    cw_in[0] = mp.RH_in * cw_sat_in[0]
    delta_c[0] = func.calc_deltac(rh_in[0], rh_wall[0], cw_sat_in[0])
    c_wall[0] = func.calc_cwall(delta_c[0])

    c_ac = list(map(func.calc_cac, beta, cw_out, temp_c_out, temp_c_in))
    c_supply = (list(map(func.calc_csupply, supply)))

    for i in range(len(temp_c_out) - 1):
        # compute fmc in layer 1
        wall_vector[0] = func.calc_layer1(rh_in[i], rh_wall[i], wall[i][0], wall[i][1], cw_sat_in[i])
        n = 0
        for l in range(mp.sub_layers-2):
            # compute fmc in wall layers 2 to N-1
            n = n + 1
            wall_vector[n] = func.calc_middle_layers(wall[i][n], wall[i][n - 1], wall[i][n + 1])
        # compute fmc in wall layer N (panel backside)
        wall_vector[-1] = func.calc_outer_layer(wall[i][-1], wall[i][-2])
        # update wall array
        wall[i + 1][:] = wall_vector
        # update surface vector
        surface[i + 1] = func.calc_surf(wall[i + 1][0], wall[i + 1][1])
        # update rh_wall
        rh_wall[i + 1] = func.calc_rhwall(surface[i + 1])
        # update water concentration difference between bulk air and boundary layer
        delta_c[i + 1] = func.calc_deltac(rh_in[i], rh_wall[i], cw_sat_in[i])
        # update indoor water concentration
        cw_in[i + 1] = func.calc_cwin(c_ac[i], c_wall[i], c_supply[i], cw_in[i], beta[i])
        # update indoor relative humidity
        rh_in[i + 1] = cw_in[i + 1] / cw_sat_in[i + 1]
        # update c_wall
        c_wall[i + 1] = func.calc_cwall(delta_c[i + 1])

    # Compute ttf
    factor = 100 / mp.rho_wood
    fmc = list(map(lambda x: x*factor, surface))
    ttf = list(map(lambda y: 2 * np.exp(0.16*y),fmc))

    return rh_in, ttf


