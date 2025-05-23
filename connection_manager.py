import sqlite3
from sqlite3 import Connection

HYDRO_SENSE_DB = 'hydro_sense.db'


class SQLiteConnectionManager:
  """Manages SQLite database connection and ensures the database file is created."""

  def __init__(self):
    self.db_file = HYDRO_SENSE_DB
    self.conn = self.create_connection()

  def create_connection(self) -> Connection:
    """Creates a connection to the SQLite database."""
    try:
      conn = sqlite3.connect(self.db_file)
      return conn
    except sqlite3.Error as e:
      print(f"Error connecting to SQLite database: {e}")
      return None

  def get_connection(self) -> Connection:
    """Returns the active connection."""
    return self.conn

  def close_connection(self):
    """Closes the database connection."""
    if self.conn:
      self.conn.close()
