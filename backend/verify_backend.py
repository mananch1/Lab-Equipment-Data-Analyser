import requests
import pandas as pd
import io

data = """Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor 1,Reactor,100,50,200
Pump A,Pump,50,10,25
Reactor 2,Reactor,80,45,190
Mixer 1,Mixer,20,5,30
"""

csv_file = io.StringIO(data)

url = 'http://127.0.0.1:8000/api/upload/'
files = {'file': ('test_data.csv', csv_file)}

print(f"Testing Upload to {url}...")
try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:
        print("Upload Successful!")
        print("Response:", response.json())
    else:
        print(f"Upload Failed: {response.text}")
except Exception as e:
    print(f"Upload Error: {e}")

print("\nTesting History...")
try:
    response = requests.get('http://127.0.0.1:8000/api/history/')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("History Fetch Successful!")
        print("Response:", response.json())
    else:
        print(f"History Fetch Failed: {response.text}")
except Exception as e:
    print(f"History Error: {e}")
