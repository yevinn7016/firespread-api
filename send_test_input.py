import requests

url = "https://firespread-api.onrender.com/input"  # 변경된 주소!
# test_input_data.py

data = [
    {
        "grid_id": 10001,
        "lat_min": 36.94,
        "lat_max": 36.95,
        "lon_min": 128.44,
        "lon_max": 128.45,
        "center_lat": 36.945,
        "center_lon": 128.445,
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
    },
    {
        "grid_id": 10002,
        "lat_min": 36.94,
        "lat_max": 36.95,
        "lon_min": 128.44,
        "lon_max": 128.45,
        "center_lat": 36.955,
        "center_lon": 128.455,
        "avg_fuelload_pertree_kg": 1.7,
        "FFMC": 92,
        "DMC": 85,
        "DC": 450,
        "NDVI": 0.38,
        "smap_20250630_filled": 0.20,
        "temp_C": 29,
        "humidity": 35,
        "wind_speed": 6.5,
        "wind_deg": 150,
        "precip_mm": 0.0,
        "mean_slope": 24,
        "spei_recent_avg": -1.8,
        "farsite_prob": 0.7
    },
    {
        "grid_id": 10003,
        "lat_min": 36.94,
        "lat_max": 36.95,
        "lon_min": 128.44,
        "lon_max": 128.45,
        "center_lat": 36.965,
        "center_lon": 128.465,
        "avg_fuelload_pertree_kg": 1.7,
        "FFMC": 92,
        "DMC": 85,
        "DC": 450,
        "NDVI": 0.45,
        "smap_20250630_filled": 0.16,
        "temp_C": 31,
        "humidity": 28,
        "wind_speed": 8.2,
        "wind_deg": 150,
        "precip_mm": 0.0,
        "mean_slope": 24,
        "spei_recent_avg": -1.8,
        "farsite_prob": 0.7
    }
]


response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
