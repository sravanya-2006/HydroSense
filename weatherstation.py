import time
import Adafruit_BME280
import Adafruit_ADS1x15
from RPLCD.i2c import CharLCD

from service.weather_service import WeatherService

# Initialize BME280 sensor (I2C address 0x76)
bme = Adafruit_BME280.BME280(address=0x76)

# Initialize the ADS1115 ADC
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1  # Gain setting for the ADS1115

# Initialize the LCD display
lcd = CharLCD('PCF8574', 0x27)  # Replace 0x27 with your I2C address if needed

service = WeatherService()

# Function to read rain sensor value
def read_rain_sensor():
    value = adc.read_adc(0, gain=GAIN)  # Read from channel 0
    return value

# Function to read light intensity value
def read_light_intensity():
    value = adc.read_adc(1, gain=GAIN)  # Read from channel 1 (adjust as necessary)
    return value

# Function to display a message for a set time
def display_message(message, duration=2):
    lcd.clear()
    lcd.write_string(message)
    time.sleep(duration)

# Main loop
try:
    while True:
        # Read BME280 sensor values
        temperature = bme.read_temperature()  # in Celsius
        pressure = bme.read_pressure() / 100  # in hPa
        humidity = bme.read_humidity()  # in %

        # Read rain sensor value
        rain_value = read_rain_sensor()
        
        # Read light intensity value
        light_intensity = read_light_intensity()

        # Check if rain is detected (adjust threshold as needed)
        rain_status = 'Rain Detected!' if rain_value < 32767 else 'No Rain Detected'

        # Cycle through the values
        display_message(f'Temp: {temperature:.1f}C')
        display_message(f'Pressure: {pressure:.1f}hPa')
        display_message(f'Humidity: {humidity:.1f}%')
        display_message(f'Light Intensity: {light_intensity}')
        display_message(rain_status)
        # Upsert weather Data
        service.upsert_weather_data(temperature, rain_status)
        # Sleep the Process for 1min for next iteration
        time.sleep(60)

except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    lcd.clear()
