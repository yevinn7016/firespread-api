########openWeatherMap 테스트해보는 코드##############
import requests

def get_weather(lat, lon, api_key):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result = {
            "위도": lat,
            "경도": lon,
            "기온 (℃)": data["main"]["temp"],
            "습도 (%)": data["main"]["humidity"],
            "풍속 (m/s)": data["wind"]["speed"],
            "풍향 (°)": data["wind"]["deg"],
        }
        return result
    else:
        return {"error": response.text}

# 예시 좌표 (속초시)
lat, lon = 38.204, 128.591
api_key = "679d0560c78e749ee4c20f8fb72be52a"

weather_data = get_weather(lat, lon, api_key)
print(weather_data)
