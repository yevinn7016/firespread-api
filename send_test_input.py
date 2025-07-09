import requests

url = "http://127.0.0.1:8000/input"
data = {
    "grid_id": 10001,
    "lat_min": 36.95,
    "lat_max": 36.97,
    "lon_min": 128.45,
    "lon_max": 128.47,
    "center_lat": 36.96,
    "center_lon": 128.46,
    "avg_fuelload_pertree_kg": 1.7,
    "FFMC": 92,
    "DMC": 85,
    "DC": 450,
    "NDVI": 0.45,
    "smap_20250630_filled": 0.20,
    "temp_C": 31,
    "humidity": 28,
    "wind_speed": 6.5,
    "wind_deg": 150,
    "precip_mm": 0.0,
    "mean_slope": 24,
    "spei_recent_avg": -1.8,
    "farsite_prob": 0.7
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
