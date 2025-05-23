from service.weather_service import WeatherService, RAIN_DETECTED

if __name__ == "__main__":
  temperature = 25.5
  rain_status = RAIN_DETECTED
  service = WeatherService()
  service.upsert_weather_data(temperature, rain_status)
