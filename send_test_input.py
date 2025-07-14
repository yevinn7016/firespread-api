import requests

url = "https://firespread-api.onrender.com/input"  # 변경된 주소!
# test_input_data.py

data = [
    {
        "grid_id": 10004,
        "lat_min": 37.12,
        "lat_max": 37.13,
        "lon_min": 128.33,
        "lon_max": 128.34,
        "center_lat": 37.125,
        "center_lon": 128.335,
        "avg_fuelload_pertree_kg": 2.1,
        "FFMC": 88,
        "DMC": 75,
        "DC": 410,
        "NDVI": 0.52,
        "smap_20250630_filled": 0.18,
        "temp_C": 33,
        "humidity": 21,
        "wind_speed": 7.3,
        "wind_deg": 120,
        "precip_mm": 0.0,
        "mean_slope": 30,
        "spei_recent_avg": -2.1,
        "farsite_prob": 0.6
    },
{
  "grid_id": 10005,
  "lat_min": 36.88,
  "lat_max": 36.89,
  "lon_min": 128.47,
  "lon_max": 128.48,
  "center_lat": 36.885,
  "center_lon": 128.475,
  "avg_fuelload_pertree_kg": 1.4,
  "FFMC": 95,
  "DMC": 90,
  "DC": 490,
  "NDVI": 0.31,
  "smap_20250630_filled": 0.14,
  "temp_C": 30,
  "humidity": 32,
  "wind_speed": 5.2,
  "wind_deg": 210,
  "precip_mm": 0.5,
  "mean_slope": 18,
  "spei_recent_avg": -1.5,
  "farsite_prob": 0.68
},
{
  "grid_id": 10006,
  "lat_min": 37.00,
  "lat_max": 37.01,
  "lon_min": 128.50,
  "lon_max": 128.51,
  "center_lat": 37.005,
  "center_lon": 128.505,
  "avg_fuelload_pertree_kg": 1.9,
  "FFMC": 85,
  "DMC": 70,
  "DC": 430,
  "NDVI": 0.49,
  "smap_20250630_filled": 0.22,
  "temp_C": 28,
  "humidity": 38,
  "wind_speed": 6.0,
  "wind_deg": 90,
  "precip_mm": 1.2,
  "mean_slope": 22,
  "spei_recent_avg": -1.2,
  "farsite_prob": 0.72
}


]


response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
