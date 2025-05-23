from datetime import date

from common.connection_manager import SQLiteConnectionManager
from common.enums import RainIntensity
from service.repository.weather_repository import WeatherRepository

RAIN_DETECTED = 'Rain Detected!'
RAIN_NOT_DETECTED = 'No Rain Detected'


class WeatherService:

  def update_rain_intensity(self, rain_duration):
    """Determines rain intensity based on the rain duration."""
    if 1 <= rain_duration < 10:
      return RainIntensity.LIGHT
    elif 10 <= rain_duration < 30:
      return RainIntensity.MODERATE
    elif rain_duration >= 30:
      return RainIntensity.HEAVY
    return RainIntensity.NA

  def process_existing_data(self, first_row, temperature, rain_status):
    """Processes existing data and updates the rain status and temperature."""
    record_date, max_temperature, rain_traces, rain_duration, rain_intensity = first_row

    print(f"Date: {record_date}")
    print(f"Max Temperature: {max_temperature}")
    print(f"Rain Traces: {rain_traces}")
    print(f"Rain Duration: {rain_duration}")
    print(f"Rain Intensity: {rain_intensity}")

    # Update max_temperature if the new temperature is higher
    max_temperature = temperature if temperature > max_temperature else max_temperature

    # Update rain details if rain is detected
    if rain_status == RAIN_DETECTED:
      rain_traces = 1
      rain_duration += 1
      rain_intensity = self.update_rain_intensity(rain_duration)

    return record_date, max_temperature, rain_traces, rain_duration, rain_intensity

  def handle_no_data(self, temperature, rain_status):
    """Handles the case when no data is found."""
    record_date = date.today()
    max_temperature = temperature
    rain_traces = 1 if rain_status == RAIN_DETECTED else 0
    rain_duration = 1 if rain_traces == 1 else 0
    rain_intensity = RainIntensity.LIGHT if rain_traces == 1 else RainIntensity.NR

    print("No data found for the current date.")
    return record_date, max_temperature, rain_traces, rain_duration, rain_intensity

  def upsert_weather_data(self, temperature, rain_status):
    global data
    # Create the connection manager and pass it to the WeatherRepository class
    connection_manager = SQLiteConnectionManager()
    db = WeatherRepository(connection_manager)
    # temperature = 25.5
    # rain_status = RAIN_DETECTED
    # Fetch and process data
    current_date = date.today().isoformat()  # Get current system date in 'YYYY-MM-DD' format
    data = db.get_data(current_date)
    if data:
      # Process the existing data
      first_row = data[0]
      record_date, max_temperature, rain_traces, rain_duration, rain_intensity = self.process_existing_data(
        first_row, temperature, rain_status)
    else:
      # Handle no data case
      record_date, max_temperature, rain_traces, rain_duration, rain_intensity = self.handle_no_data(temperature,
                                                                                                     rain_status)
    # Upsert the updated data
    db.upsert_data(record_date, max_temperature, rain_traces, rain_duration, rain_intensity)
    # Close the connection
    connection_manager.close_connection()
