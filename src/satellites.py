from sgp4.api import Satrec
from skyfield.api import EarthSatellite, load, wgs84
from datetime import datetime, timezone, timedelta

def load_tles(filepath): # this loads the elements from a .txt file 
        try:
            satellites = [] # the satellites are put into an array

            with open(filepath, "r") as file: # this line actully opens the file as read
                lines = [line.strip() for line in file if line.strip()] # this gos through the file line by line and strips the white space

            for i in range(0, len(lines), 3): # this groups each line in groups of 3 as its a three line element
                line0 = lines[i + 0]
                line1 = lines[i + 1]
                line2 = lines[i + 2]

                satellite = Satellite(line0, line1, line2) # adds all three lines of the tle into one variable
                satellites.append(satellite)

            return satellites
        except Exception as e:
            print(f"load_tles failed: {e}")

class Satellite:
    def __init__(self, line0, line1, line2): # __init__ always exacutes this function when a new object is made
        # self basicaly means this particular object, think of it as a pointer to a specific satellite
        self.name = line0 # points to a specific satellite with the name from the tle

        self.sat = Satrec.twoline2rv(line1, line2) # SGP4 representation of tle data
        self.sky_sat = EarthSatellite(line1, line2, line0) # Skyfield representation of the tle data

    def sgp4_satellite_propagate(self, time): # this function returns the position and velocity of the satellite by converting the time to 
        # the following three lines converts the current time to UNIX seconds and days, then to Julian time as the SGP4 expected format
        jd = time.timestamp() / 86400.0 + 2440587.5 # there are 86400.0 seconds in a day, im pretty sure 2440587.5 is the starting point for Julian time
        jd_int = int(jd)
        jd_frac = jd - jd_int

        error, position, velocity = self.sat.sgp4(jd_int, jd_frac) # this line propagates the spacecraft from the loaded tle and a specified time

        return error, position, velocity # returns the position and velocity in x, y, z along with the error code from sgp4
