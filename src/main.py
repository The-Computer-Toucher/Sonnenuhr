import sys
import time
import tkinter as tk
from skyfield.api import wgs84
from satellites import load_tles
from tracking import propagate_tles
from gui import SonnenuhrGUI

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
set_timezone = 0

observer_latitude_degrees = 0
observer_longitude_degrees = 0
observer_elevation_m = 0

# the stations loaction using lat, lon, and alt
observer_location = wgs84.latlon(latitude_degrees=observer_latitude_degrees, longitude_degrees=observer_longitude_degrees, elevation_m=observer_elevation_m)

# todo: later make it so the user can set set/chose the file they are reading from, additonaly add a feature to allow downloading tles form https://celestrak.org/
# loads the satellites from the fillpath
filepath = "tles.txt"
satellites = load_tles(filepath)

# this is the main loop
# todo: later add a sdr++ conection thing so the users dont have to start recording, it will do it for them, and potntioaly have doppler shift cababilities for sstv or ssb/fm signals, or even tlm signals

root = tk.Tk()

gui = SonnenuhrGUI(root)

def update_tracking():
    satellite_data = propagate_tles(satellites, observer_location, set_timezone)

    # checks if there is satellite data loaded
    if satellite_data:
        # displays the first satellite # todo: make a thing so that the user can select the satellite from a list
        gui.update_satellite(satellite_data[30]) # [num] is the number of tles down in the load list of tles

    # this runs again in 500 ms #? if i add the settign to change the update rate, make it 100 ish ms minimum; pretty sure it gets chopy at lower rate becasue it has to update all of the satellites-inefficient
    #? i just had an idea, update the current satellite you the user has selected to track and update it more frequnlty, and update the position of the other satellites in the background at a lower rate
    root.after(int(500), update_tracking) #? maybe add a setting option to change the update rate

update_tracking()




try:
    root.mainloop()

except KeyboardInterrupt:
    print("Program killed")
    root.destroy()
    sys.exit()
