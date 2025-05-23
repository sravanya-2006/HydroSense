import configparser
import time
from datetime import datetime, timedelta

from common.connection_manager import SQLiteConnectionManager
from common.enums import RainIntensity
from service.repository.pumping_log_repository import WaterPumpingLogRepository
from service.repository.weather_repository import WeatherRepository

# Path to the configuration file
CONFIG_FILE = 'config.properties'


class WaterPumpingJob:
  def __init__(self, db_manager):
    self.db_manager = db_manager
    self.pumping_log_repository = WaterPumpingLogRepository(db_manager)
    self.weather_repository = WeatherRepository(db_manager)
    self.config = self.load_config()
    self.watering_frequency_days = self.config.getint('settings', 'watering_frequency_days')
    self.daily_watering_duration_minutes = self.config.getint('settings', 'daily_watering_duration_minutes')

  def load_config(self):
    """Loads the configuration file."""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

  def run(self):
    """Executes the water pumping job based on the last log and configured frequency."""
    current_date = datetime.now().date()
    last_log = self.pumping_log_repository.get_last_log()

    if last_log:
      last_pump_date = datetime.strptime(last_log[0], '%Y-%m-%d').date()
      days_since_last_pump = (current_date - last_pump_date).days

      if self.check_rain_conditions():
        print("Skipping watering due to rain conditions.")
        return

      extra_time = 1 if self.check_high_temperature() else 0

      if days_since_last_pump >= self.watering_frequency_days:
        self.trigger_watering(current_date, extra_time)
      else:
        print(f"No need for watering today. Last watering was {days_since_last_pump} days ago.")
    else:
      # No records exist, trigger the first watering
      self.trigger_watering(current_date, 0)

    self.pumping_log_repository.close()

  def trigger_watering(self, current_date, extra_time):
    """Triggers the watering and logs the event."""
    start_time = datetime.now().strftime('%H:%M:%S')
    total_watering_minutes = self.daily_watering_duration_minutes + extra_time * 60
    print(f"Triggering water pump on {current_date} at {start_time} for {total_watering_minutes} minutes.")

    # Simulate watering duration
    time.sleep(60 * total_watering_minutes)

    end_time = datetime.now().strftime('%H:%M:%S')
    print(f"Water pump stopped on {current_date} at {end_time}")

    self.pumping_log_repository.insert_log(
      current_date.isoformat(), True, start_time, end_time, "Water pump activated."
    )

  def check_rain_conditions(self):
    """Check for heavy rain in past 7 days or moderate rain in past 3 days."""
    current_date = datetime.now().date()
    seven_days_ago = current_date - timedelta(days=7)
    three_days_ago = current_date - timedelta(days=3)

    weather_data = self.weather_repository.get_weather_data(seven_days_ago, current_date)

    heavy_rain_found = any(
      rain_intensity == RainIntensity.HEAVY.value for _, _, _, _, rain_intensity in weather_data
    )
    moderate_rain_found_in_3_days = any(
      rain_intensity == RainIntensity.MODERATE.value and record_date >= three_days_ago
      for record_date, _, _, _, rain_intensity in weather_data
    )

    return heavy_rain_found or moderate_rain_found_in_3_days

  def check_high_temperature(self):
    """Check if the average temperature in the past 3 days is > 39°C."""
    current_date = datetime.now().date()
    three_days_ago = current_date - timedelta(days=3)

    weather_data = self.weather_repository.get_weather_data(three_days_ago, current_date)

    total_temperature = sum(max_temperature for _, max_temperature, _, _, _ in weather_data)
    avg_temperature = total_temperature / len(weather_data) if weather_data else 0

    return avg_temperature > 39


if __name__ == "__main__":
  # Initialize the SQLite connection manager
  db_manager = SQLiteConnectionManager()

  # Run the water pumping job
  water_job = WaterPumpingJob(db_manager)
  water_job.run()
