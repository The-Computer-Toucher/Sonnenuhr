import tkinter as tk # this libary is for windows, buttons, labels, text boxs, dropdowns and menus

class SonnenuhrGUI: # the class that represents the whole gui
    def __init__(self, root): # runs automaticaly when the object is created
        # window settings
        self.root = root
        self.root.title("Sonnenuhr") # windows title 
        self.root.geometry("1200x700") # the windows initial size

        self.main_frame = tk.Frame(self.root) # this is the main tracking container for the ground track
        self.main_frame.pack(fill="both", expand=True)

        # placeholder text for now but this is where the main content will go
        self.main_label = tk.Label(self.main_frame, text="Sonnenuhr\nTracking display", font=("Arial", 24))
        self.main_label.pack(expand=True)

        # this is the bottom metics pannel stuff
        self.metrics_frame = tk.Frame(self.root,bd=2,relief="raised")
        self.metrics_frame.pack(side="bottom", fill="x")

        # the right section
        self.satellite_frame = tk.Frame(self.metrics_frame, bd=1, relief="sunken")
        self.satellite_frame.pack(side="left", fill="both", expand=True)
        self.name_label = self.create_metric("Target:", self.satellite_frame)
        self.altitude_label = self.create_metric("ALT:", self.satellite_frame)
        self.latency_label = self.create_metric("OWD:", self.satellite_frame)
        self.velocity_label = self.create_metric("Rel speed:", self.satellite_frame)
        self.range_rate_label = self.create_metric("Range rate:", self.satellite_frame)
        # todo: make this the doppler shift

        # the left section
        self.tracking_frame = tk.Frame(self.metrics_frame, bd=1, relief="sunken")
        self.tracking_frame.pack(side="left", fill="both", expand=True)
        self.azimuth_label = self.create_metric("AZ:", self.tracking_frame)
        self.elevation_label = self.create_metric("EL:", self.tracking_frame)
        self.distance_label = self.create_metric("Dist:", self.tracking_frame)
        self.latitude_label = self.create_metric("LAT:", self.tracking_frame)
        self.longitude_label = self.create_metric("LON:", self.tracking_frame)

    def create_metric(self, title, parent): # this function creates one metric box 
        frame = tk.Frame(parent, padx=15, pady=8) # i might change the padding 
        frame.pack(side="left", fill="both", expand=True)

        title_label = tk.Label(frame, text=title, font=("Arial", 9))
        title_label.pack()

        value_label = tk.Label(frame, text="---", font=("Arial", 14))
        value_label.pack()

        return value_label

    def update_satellite(self, data): # this function updates the metrics on the window after the satellites are propagated
        self.name_label.config(text=data["name"])
        self.altitude_label.config(text=f"{data['altitude']:.1f} km")
        self.azimuth_label.config(text=f"{data['azimuth']:.3f}°")
        self.elevation_label.config(text=f"{data['elevation']:.3f}°")
        self.distance_label.config(text=f"{data['distance']:.1f} km")
        self.range_rate_label.config(text=f"{data['range_rate']:.1f} km/s")
        self.velocity_label.config(text=f"{data['relative_velocity']:.1f} km/s")
        self.latency_label.config(text=f"{data['latency']:.4f} s")
        self.latitude_label.config(text=f"{data['latitude']:.3f}°")
        self.longitude_label.config(text=f"{data['longitude']:.3f}°")
