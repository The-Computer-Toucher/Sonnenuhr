import sys
import time
import subprocess
from skyfield.api import wgs84
from satellites import load_tles
from tracking import propagate_tles

def load_settings():
    pass

def save_settings():
    pass

def text_to_speech(text): # this function runs the text to speach script
    try:
        subprocess.Popen(["python", "run_tts.py", text])
    except Exception as e:
        print(f"text_to_speech failed: {e}")

# todo: latter make these load from the settings.json
# preliminary settings 
set_timezone = 10

observer_latitude_degrees = 0
observer_longitude_degrees = 0
observer_elevation_m = 0

# the stations loaction using lat, lon, and alt
observer_location = wgs84.latlon(
    latitude_degrees=observer_latitude_degrees,
    longitude_degrees=observer_longitude_degrees,
    elevation_m=observer_elevation_m)

# todo: later make it so the user can set set/chose the file they are reading from, additonaly add a feature to allow downloading tles form https://celestrak.org/
# loads the satellites from the fillpath
filepath = "tles.txt"
satellites = load_tles(filepath)

# this is the main loop
try:
    while True:
        satellite_data = propagate_tles(satellites, observer_location, set_timezone)

        for satellite in satellite_data:

            print()
            print("Satellite:", satellite["name"])
            print(f"Latitude: {satellite['latitude']:.6f}°")
            print(f"Longitude: {satellite['longitude']:.6f}°")
            print(f"Altitude: {satellite['altitude']:.3f} km")
            print(f"Elevation: {satellite['elevation']:.2f}°")
            print(f"Azimuth: {satellite['azimuth']:.2f}°")
            print(f"Distance: {satellite['distance']:.2f} km")
            print(f"Relative velocity: {satellite['relative_velocity']:.3f} km/s")
            print(f"Range rate: {satellite['range_rate']:.3f} km/s")
            print(f"Latency: {satellite['latency']:.3f} s")

        time.sleep(1)

except KeyboardInterrupt:
    print("Program killed")
    sys.exit()
