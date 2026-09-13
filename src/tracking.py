import numpy
from skyfield.api import load
from time_utils import get_time_utc
from signals import signal_metrics


def satellite_relative_metrics(satellite, observer_location, sky_time): # this function finds the relative position/veloctiy/az/evl/ragne rate
    difference = satellite.sky_sat - observer_location

    topocentric = difference.at(sky_time)

    elevation, azimuth, distance = topocentric.altaz() # relative elevation/azimuth/distance from the station

    position = topocentric.position.km # relative position

    velocity = topocentric.velocity.km_per_s # relative velocity

    relative_speed = numpy.linalg.norm(velocity) # turns the the velocity vecter in relative speed

    range_rate = numpy.dot(position, velocity) / numpy.linalg.norm(position) # range rate is the speed the spacecraft is move toward/away relative to the station

    return elevation.degrees, azimuth.degrees, distance.km, relative_speed, range_rate


def propagate_tles(satellites, observer_location, set_timezone):
    current_time, local_time = get_time_utc(set_timezone) # fetches time for utc and utc+(selected time zone)

    ts = load.timescale() # skyfield time convertion
    sky_time = ts.from_datetime(current_time)

    results = [] # this arry/list is used to send all of the data together

    for satellite in satellites:
        error, position, velocity = (satellite.sgp4_satellite_propagate(current_time)) # the error is 7 diffrent code wich can be found on sgp4 page, for example 6 means "The orbit has decayed: the computed position is underground"
        if error != 0:
            print(f"SGP4 error for {satellite.name}: error-{error}") # prints the error code from sgp4, the code 0 means everything is okay
            continue

        # gets the satellite position above earth
        geocentric = satellite.sky_sat.at(sky_time)
        subpoint = geocentric.subpoint()
        latitude = subpoint.latitude.degrees
        longitude = subpoint.longitude.degrees
        altitude = subpoint.elevation.km

        # observer relative information stuff
        relative_elevation, relative_azimuth, relative_distance, relative_velocity, range_rate = satellite_relative_metrics(satellite, observer_location, sky_time) # this function finds the relative position/veloctiy/az/evl/ragne rate

        # signal info
        sig_latency = signal_metrics(relative_distance) # todo: later return the dopller values as well

        # appending all the data together
        satellite_data = {
            "name": satellite.name,

            "position": position,
            "velocity": velocity,

            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude,

            "elevation": relative_elevation,
            "azimuth": relative_azimuth,
            "distance": relative_distance,

            "relative_velocity": relative_velocity,
            "range_rate": range_rate,

            "latency": sig_latency # todo: return the dopller values
        }
        results.append(satellite_data)

    return results
