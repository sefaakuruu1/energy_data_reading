import mysql.connector
from mysql.connector import Error
import json
from contextlib import contextmanager
from plot_graph import plot_graph
# MySQL bağlantı bilgileri
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '0372.Sefa',
    'database': 'energy_data'
}

@contextmanager
def get_connection_and_cursor():
    """Veritabanı bağlantısını ve kursörü context manager olarak yönetir."""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        yield connection, cursor
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        yield None, None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("MySQL connection is closed.")

def create_table():
    """energy_readings tablosunu oluşturur."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS energy_readings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        current_data JSON,
        power_active_data JSON
    );
    """

    # Context manager kullanarak bağlantıyı ve kursörü al
    with get_connection_and_cursor() as (connection, cursor):
        if connection and cursor:
            cursor.execute(create_table_query)
            connection.commit()  # Tablo oluşturma sorgusunu commit et
            print("Table created successfully.")

def insert_data(current_data, power_active_data):
    """Veriyi energy_readings tablosuna ekler."""
    insert_query = """
    INSERT INTO energy_readings (current_data, power_active_data)
    VALUES (%s, %s)
    """

    # JSON veri formatına dönüştür
    current_data_json = json.dumps(current_data)
    power_active_data_json = json.dumps(power_active_data)

    # Context manager kullanarak bağlantıyı ve kursörü al
    with get_connection_and_cursor() as (connection, cursor):
        if connection and cursor:
            try:
                cursor.execute(insert_query, (current_data_json, power_active_data_json))
                connection.commit()
                print("Data inserted successfully.")
            except Error as e:
                print(f"Error while inserting data: {e}")

def execute_query(query):
    """Verilen SQL sorgusunu çalıştırır ve sonuçları döndürür."""
    with get_connection_and_cursor() as (connection, cursor):
        if connection and cursor:
            try:
                cursor.execute(query)
                return cursor.fetchall()
            except Error as e:
                print(f"Error while executing query: {e}")
                return []

# 10 Dakikalık Veriler İçin Sorgu
query_10_min = """
SELECT 
    DATE_FORMAT(timestamp - INTERVAL MINUTE(timestamp) % 10 MINUTE, '%Y-%m-%d %H:%i:00') AS TimeSlot,
    MAX(CAST(current_data AS DECIMAL(10, 2))) AS MaxCurrentValue,
    AVG(CAST(current_data AS DECIMAL(10, 2))) AS AverageCurrentValue,
    MIN(CAST(current_data AS DECIMAL(10, 2))) AS MinCurrentValue
FROM 
    energy_readings
WHERE 
   timestamp >= '2024-08-16 09:00:00'
&& TIME(timestamp) BETWEEN '09:00:00' AND '17:00:00'
GROUP BY 
    TimeSlot
ORDER BY 
    TimeSlot;
"""

# 60 Dakikalık Veriler İçin Sorgu
query_60_min = """
SELECT 
    DATE_FORMAT(timestamp - INTERVAL MINUTE(timestamp) % 60 MINUTE, '%Y-%m-%d %H:%i:00') AS TimeSlot,
    MAX(CAST(current_data AS DECIMAL(10, 2))) AS MaxCurrentValue,
    AVG(CAST(current_data AS DECIMAL(10, 2))) AS AverageCurrentValue,
    MIN(CAST(current_data AS DECIMAL(10, 2))) AS MinCurrentValue
FROM 
    energy_readings
WHERE 
  timestamp >= '2024-08-16 09:00:00'
&& TIME(timestamp) BETWEEN '09:00:00' AND '17:00:00'
GROUP BY 
    TimeSlot
ORDER BY 
    TimeSlot;
"""
query_1_day = """
SELECT 
    DATE_FORMAT(timestamp, '%Y-%m-%d') AS TimeSlot,
    MAX(CAST(current_data AS DECIMAL(10, 2))) AS MaxCurrentValue,
    AVG(CAST(current_data AS DECIMAL(10, 2))) AS AverageCurrentValue,
    MIN(CAST(current_data AS DECIMAL(10, 2))) AS MinCurrentValue
FROM 
    energy_readings
WHERE 
       timestamp >= '2024-08-16 09:00:00'
&& TIME(timestamp) BETWEEN '09:00:00' AND '17:00:00'
GROUP BY 
    TimeSlot
ORDER BY 
    TimeSlot;

"""



def prepare_data(results):
    """Verileri ayrıştırır ve grafiğe uygun formatta döndürür."""
    time_slots = []
    min_values = []
    max_values = []
    avg_values = []

    for row in results:
        time_slots.append(row[0])
        min_values.append(float(row[2]))  # MinCurrentValue
        max_values.append(float(row[1]))  # MaxCurrentValue
        avg_values.append(float(row[3]))  # AverageCurrentValue

    return time_slots, min_values, max_values, avg_values


results_10_min = execute_query(query_10_min)

# 60 Dakikalık Verileri Çek
results_60_min = execute_query(query_60_min)

results_1_day=execute_query(query_1_day)

# Verileri Hazırla
time_slots_10_min, min_values_10_min, max_values_10_min, avg_values_10_min = prepare_data(results_10_min)
time_slots_60_min, min_values_60_min, max_values_60_min, avg_values_60_min = prepare_data(results_60_min)
time_slots_1_day,min_values_1_day,max_values_1_day,avg_values_1_day=prepare_data(results_1_day)

# Grafik Çizdir
plot_graph(time_slots_10_min, min_values_10_min, max_values_10_min, avg_values_10_min,
           time_slots_60_min, min_values_60_min, max_values_60_min, avg_values_60_min,
           time_slots_1_day,min_values_1_day,max_values_1_day,avg_values_1_day)
