from datetime import date

from common.connection_manager import SQLiteConnectionManager
from common.enums import RainIntensity


class WeatherRepository:

  def __init__(self, connection_manager: SQLiteConnectionManager):
    self.conn = connection_manager.get_connection()
    self.create_table()

  def create_table(self):
    """Create table if it doesn't exist."""
    create_table_sql = '''
        CREATE TABLE IF NOT EXISTS weather (
            date TEXT PRIMARY KEY,
            max_temperature REAL,
            rain_traces BOOLEAN,
            rain_duration INTEGER,
            rain_intensity TEXT CHECK(rain_intensity IN ('Light', 'Moderate', 'Heavy'))
        );
        '''
    self.conn.execute(create_table_sql)
    self.conn.commit()

  def upsert_data(self, record_date: date, max_temperature: float, rain_traces: bool,
                  rain_duration: int, rain_intensity: RainIntensity):
    """Inserts or updates data into the table."""
    upsert_sql = '''
        INSERT INTO weather (date, max_temperature, rain_traces, rain_duration, rain_intensity)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET
            max_temperature = excluded.max_temperature,
            rain_traces = excluded.rain_traces,
            rain_duration = excluded.rain_duration,
            rain_intensity = excluded.rain_intensity;
        '''
    self.conn.execute(upsert_sql, (record_date, max_temperature, rain_traces, rain_duration, rain_intensity.value))
    self.conn.commit()

  def get_data(self, record_date: str):
    fetch_sql = 'SELECT * FROM weather WHERE date = ?;'
    cursor = self.conn.execute(fetch_sql, (record_date,))
    records = cursor.fetchall()
    return records

  def get_weather_data(self, start_date, end_date):
    query = 'SELECT date, max_temperature, rain_traces, rain_duration, rain_intensity FROM weather WHERE date BETWEEN ? AND ? ;'

    cursor = self.conn.execute(query, (start_date, end_date))

    # Fetch all rows
    weather_data = cursor.fetchall()

    # Close the cursor
    cursor.close()

    # Return the fetched data
    return weather_data
