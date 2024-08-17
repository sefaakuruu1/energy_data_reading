import mysql.connector
from mysql.connector import Error
import json
from contextlib import contextmanager
import matplotlib.pyplot as plt
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
        if cursor :
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
    """Verilen SQL sorgusunu çalıştırır ve sonuçları yazdırır."""
    with get_connection_and_cursor() as (connection, cursor):
        if connection and cursor:
            try:
                # Sorguyu çalıştır
                cursor.execute(query)

                # Sonuçları al
                results = cursor.fetchall()

                # Sonuçları yazdır
                for row in results:
                    print(row)
            except Error as e:
                print(f"Error while executing query: {e}")

# Örnek kullanım:
query = """
SELECT 
    DATE_FORMAT(timestamp - INTERVAL MINUTE(timestamp) % 60 MINUTE, '%Y-%m-%d %H:%i:00') AS TimeSlot,
    MAX(current_data) AS MaxCurrentValue,
    AVG(current_data) AS AverageCurrentValue,
    MIN(current_data) AS MinCurrentValue
FROM 
    energy_readings
WHERE 
    timestamp >= '2024-08-16 09:00:00'
GROUP BY 
    TimeSlot
ORDER BY 
    TimeSlot;
"""

execute_query(query)