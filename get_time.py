import utime
import urequests
import logger

debug_logging = True

TIME_API_BASE = "http://worldtimeapi.org/api/timezone/"
TIME_API_LOCATION = "America/Chicago"


class TimeData:
    def __init__(self, api_data):
        # Parse the datetime string
        datetime_str = api_data.get("datetime")
        # "2024-11-09T12:52:42.282163-06:00" -> separate date and time
        date_part, time_part = datetime_str.split("T")
        time_only = time_part.split(".")[0]  # Get only HH:MM:SS
        
        # Further split date and time
        self._year, self._month, self._day = map(int, date_part.split("-"))
        self._hour, self._minute, self._second = map(int, time_only.split(":"))
        
        # zero padded formatting
        self.year = f"{self._year:04d}"
        self.month = f"{self._month:02d}"
        self.day = f"{self._day:02d}"
        self.hour = f"{self._hour:02d}"
        self.minute = f"{self._minute:02d}"
        self.second = f"{self._second:02d}"
        
        self.formatted_datetime = f"{self.year}-{self.month}-{self.day} {self.hour}:{self.minute}:{self.second}"
        
        # Other data
        self.utc_offset = api_data.get("utc_offset")
        self.timezone = api_data.get("timezone")
        self.unixtime = api_data.get("unixtime")
        self.day_of_week = api_data.get("day_of_week")
        self.day_of_year = api_data.get("day_of_year")
        self.week_number = api_data.get("week_number")
        self.dst = api_data.get("dst")
        self.abbreviation = api_data.get("abbreviation")
        

def get_time_data(base=TIME_API_BASE, timezone=TIME_API_LOCATION):
    try:
        response = urequests.get(f"{base}{timezone}")
        if response.status_code == 200:
            api_data = response.json()
            return TimeData(api_data)
        else:
            print(f"Failed to retrieve data, status code: {response.status_code}")
            logger.send_debug_to_graylog_udp(debug_logging, f"Failed to retrieve data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching time data: {e}")
        logger.send_debug_to_graylog_udp(debug_logging, f"Error fetching time data: {e}")
        return None

    
if __name__ == "__main__":
    
    
    time_data = get_time_data()
    
    if time_data:
        print(f"Hour: {time_data.hour}")
        print(f"Minute: {time_data.minute}")
        print(f"Second: {time_data.second}")
        print(f"Timezone: {time_data.timezone}")
        print(f"Day of Week: {time_data.day_of_week}")
        print(f"UTC Offset: {time_data.utc_offset}")
    
