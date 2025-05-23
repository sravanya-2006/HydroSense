from common.connection_manager import SQLiteConnectionManager


class WaterPumpingLogRepository:

  def __init__(self, connection_manager: SQLiteConnectionManager):
    self.conn = connection_manager.get_connection()
    self.create_table()

  def create_table(self):
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS WATER_PUMPING_LOG (
            date TEXT PRIMARY KEY,
            start_time TEXT,
            end_time TEXT,
            status BOOLEAN,
            notes TEXT
        );
        """
    self.conn.execute(create_table_sql)
    self.conn.commit()

  def get_last_log(self):
    """Fetches the last water pumping log entry."""
    fetch_sql = 'SELECT date, status, start_time, end_time, notes FROM WATER_PUMPING_LOG ORDER BY date DESC LIMIT 1;'
    cursor = self.conn.execute(fetch_sql)
    return cursor.fetchone()

  def insert_log(self, date, status, start_time, end_time, notes):
    """Inserts a new water pumping log entry."""
    insert_sql = '''
        INSERT INTO WATER_PUMPING_LOG (date, status, start_time, end_time, notes)
        VALUES (?, ?, ?, ?, ?);
        '''
    self.conn.execute(insert_sql, (date, status, start_time, end_time, notes))
    self.conn.commit()

  def close(self):
    self.conn.close()
