try:
    # import asyncio
    import sys
    import subprocess
    import time
    # import threading
    from sgp4.api import Satrec
    from skyfield.api import EarthSatellite, load, wgs84
    from datetime import datetime, timezone, timedelta

    def text_to_speech(text): # this runs the text to speach script
        subprocess.Popen(["python", "src/Run_TTS.py", text])

    class Satellite:
        def __init__(self, name, line1, line2): # __init__ always exacutes this function when a new object is made
            # self basicaly means this particular object, think of it as a pointer to a specific satellite
            self.name = name # points to a specific satellite with the name from the tle

            self.sat = Satrec.twoline2rv(line1, line2) # SGP4 representation of tle data
            self.sky_sat = EarthSatellite(line1, line2, name) # Skyfield representation of the tle data

        def sgp4_satellite_propagate(self, time): # this function returns the position and velocity of the satellite by converting the time to 
            # the following three lines converts the current time to UNIX seconds and days, then to Julian time as the SGP4 expected format
            jd = time.timestamp() / 86400.0 + 2440587.5 # there are 86400.0 seconds in a day, im pretty sure 2440587.5 is the starting point for Julian time
            jd_int = int(jd)
            jd_frac = jd - jd_int

            error, position, velocity = self.sat.sgp4(jd_int, jd_frac) # this line propagates the spacecraft from the loaded tle and a specified time

            return position, velocity # returns the position and velocity in x, y, z

    # this is an approx tle for texting
    name = "ISS (ZARYA)"
    line1 = "1 25544U 98067A   26100.00000000  .00000000  00000-0  00000-0 0  9999"
    line2 = "2 25544  51.6400 100.0000 0005000 200.0000 160.0000 15.50000000123456"

    # create satellite
    satellite = Satellite(name, line1, line2) # todo: make this loop through each tle in a .txt file

    def get_time_utc(set_timezone): # this function fetches the approx time at utc and the set time zone
        try:
            current_time = datetime.now(timezone.utc) # gets the current time for the set time zone, utc0

            if set_timezone != int(0):
                target_zone = timezone(timedelta(hours=int(set_timezone)))
                local_time = current_time.astimezone(target_zone)
            else:
                local_time = current_time

            return current_time, local_time

        except Exception as e:
            print(f"get_time_utc: {e}")







    while True: # this is test code, only used to test the basic functions of a programe currently
        current_time, local_time = get_time_utc(10)

        # SGP4 position
        position, velocity = satellite.sgp4_satellite_propagate(current_time)
        
        print()
        print("----------------")
        print(f"UTC Time: {current_time}\nLocal Time: {local_time}")
        print("Satellite:", satellite.name)
        print("Raw SGP4 position:", position)
        print("Velocity:", velocity)

        # skyfield time
        ts = load.timescale()
        t = ts.from_datetime(current_time)

        # get WGS-84 coordinates
        geocentric = satellite.sky_sat.at(t)

        subpoint = geocentric.subpoint()

        latitude = subpoint.latitude.degrees
        longitude = subpoint.longitude.degrees
        altitude = subpoint.elevation.km

        print()
        print("WGS-84 Position")
        print("----------------")
        print(f"Latitude: {latitude:.6f}°")
        print(f"Longitude: {longitude:.6f}°")
        text_to_speech(f"Altitude: {altitude:.0f} km")
        time.sleep(2)



except Exception as e:
    print(f"Exception: {e}")

except KeyboardInterrupt:
    print("Programed killed")
    sys.exit()
