from datetime import datetime, timezone, timedelta

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
            print(f"get_time_utc failed: {e}")
