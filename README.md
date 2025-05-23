💧 HydroSense - Smart Irrigation System

**HydroSense** is a Python-based smart irrigation system built using a Raspberry Pi and environmental sensors. It automates water management by collecting real-time weather and soil data, and intelligently controls a water pump to ensure efficient irrigation, especially for agriculture and garden applications.

🌟 Key Features

- 🌦️ **Weather & Soil Monitoring**  
  Gathers real-time data using sensors for temperature, humidity, soil moisture, rainfall, and more.

- 🤖 **Automated Water Pumping**  
  Controls the pump based on sensor readings and weather predictions to conserve water.

- 🔄 **Scheduled and Real-Time Jobs**  
  Periodic checks and dynamic decisions based on changing environmental conditions.

- 📦 **Modular Architecture**  
  Clearly separated Python modules for weather handling, data repositories, job scheduling, and pump control.

 🧰 Hardware & Components

- 🖥️ **Raspberry Pi** (any model with GPIO support)
- 🌡️ **BME280** – Temperature, humidity, and pressure sensor
- 💧 **Soil Moisture Sensor**
- ☔ **Rain Sensor**
- 💡 **LDR Sensor** (optional for light detection)
- 🛠️ **Relay Module** (to control water pump)
- 💡 Optional: OLED/TFT display for real-time readings

🗂️ Project Structure

HydroSense/
├── config.properties # Configuration settings
├── connection_manager.py # Manages database/API connections
├── enums.py # Status enums
├── main.py # Main execution script
├── pumping_log_repository.py # Logs pump actions
├── water_pumping_job.py # Job for controlling the pump
├── weather_repository.py # Stores sensor data
├── weather_service.py # Processes and interprets data
└── weatherstation.py # Reads data from sensors


⚙️ How It Works

1. `weatherstation.py` reads data from connected sensors via GPIO.
2. `weather_service.py` interprets this data to determine weather status.
3. `weather_repository.py` stores or logs the data locally.
4. `water_pumping_job.py` checks conditions (e.g., dry soil + no rain forecast).
5. Pump is controlled via relay if needed, all configured in `config.properties`.

🧪 Requirements

- Raspberry Pi with Raspbian OS
- Python 3.8+
- GPIO access enabled
- `pip install RPi.GPIO` or `gpiozero`
- Optionally: SQLite, MQTT, or HTTP if you're integrating data logging

🚀 Getting Started

1. Connect your sensors and pump to the Raspberry Pi GPIO pins.
2. Clone the repository:
   
   git clone https://github.com/sravanya-2006/HydroSense.git
   cd HydroSense
Install required libraries:

pip install RPi.GPIO
pip install smbus2
pip install adafruit-circuitpython-bme280
Update config.properties with your thresholds and GPIO pin numbers.

Run the system:
python3 main.py

📈 Use Cases
🌾 Precision agriculture

🏡 Automated garden watering

🏞️ Environmentally conscious irrigation for smart homes

📄 License
This project is licensed under the MIT License.

