import requests
import time
from Database import create_table, insert_data
API_KEY = 'ae435cd78d9e2aa4251238e858'
BASE_URL = f'http://192.168.1.113/{API_KEY}/'

def get_total_energy():
    endpoint = 'get_total_energy'
    url = f'{BASE_URL}{endpoint}'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    print(f"URL: {url}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")  # Yanıtın ham metnini yazdır
    if response.status_code == 200:
        try:
            data = response.json()
            current = data.get('current', [])
            power_active = data.get('power_active', [])
            # Yalnızca ilk veriyi almak için
            current_first_value = current[0] if current else None
            power_active_first_value = power_active[0] if power_active else None
            return current_first_value, power_active_first_value
        except ValueError as e:
            print(f"JSON decoding error: {e}")
            return None, None
    else:
        response.raise_for_status()

def get_current_parameters():
    endpoint = 'get_current_parameters'
    url = f'{BASE_URL}{endpoint}'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    print('*************************************')
    print(f"URL: {url}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")  # Yanıtın ham metnini yazdır
    if response.status_code == 200:
        try:
            data = response.json()
            current = data.get('current', [])
            power_active = data.get('power_active', [])
            # Yalnızca ilk veriyi almak için
            current_first_value = current[0] if current else None
            power_active_first_value = power_active[0] if power_active else None
            return current_first_value, power_active_first_value
        except ValueError as e:
            print(f"JSON decoding error: {e}")
            return None, None
    else:
        response.raise_for_status()

if __name__ == "__main__":
    while True:
        try:
            # Parametre verilerini çek
            current_data, power_active_data = get_current_parameters()
            print("Current Data:", current_data)
            print("Power Active Data:", power_active_data)

            if current_data is not None and power_active_data is not None:
                insert_data(current_data, power_active_data)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        finally:
            print("Waiting for the next request...")
            time.sleep(60)
