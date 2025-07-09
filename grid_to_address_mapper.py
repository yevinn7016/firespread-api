import pandas as pd
import requests
import time
from tqdm import tqdm

# VWorld API 키
VWORLD_API_KEY = "3C3B4E8D-E920-312B-A175-84AAA2600E99"

# 입력 격자 데이터 (center_lat, center_lon 포함)
df = pd.read_csv("korea_grids_0.01deg.csv")
df = df.dropna(subset=["center_lat", "center_lon"]).copy()

# 결과 리스트 초기화
results = []

# 실패 로그 파일
error_log = open("vworld_geocode_errors.txt", "w", encoding="utf-8")

for idx, row in tqdm(df.iterrows(), total=len(df)):
    lat = row["center_lat"]
    lon = row["center_lon"]
    grid_id = row["grid_id"]

    url = (
        "https://api.vworld.kr/req/address?"
        f"service=address&request=getAddress&format=json"
        f"&type=BOTH&point={lon},{lat}&crs=EPSG:4326&key={VWORLD_API_KEY}"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if data["response"]["status"] == "OK" and data["response"]["result"]:
            res = data["response"]["result"][0]
            structure = res.get("structure", {})
            results.append({
                "grid_id": grid_id,
                "center_lat": lat,
                "center_lon": lon,
                "region_1depth": structure.get("level1"),
                "region_2depth": structure.get("level2"),
                "region_3depth": structure.get("level3"),
                "region_4depth": structure.get("level4_l"),
                "full_address": res.get("text")
            })
        else:
            msg = f"❌ Empty result at idx {idx} (grid_id {grid_id})"
            print(msg)
            error_log.write(msg + "\n")
            results.append({
                "grid_id": grid_id,
                "center_lat": lat,
                "center_lon": lon,
                "region_1depth": None,
                "region_2depth": None,
                "region_3depth": None,
                "region_4depth": None,
                "full_address": None
            })

    except Exception as e:
        msg = f"❗Error at idx {idx} (grid_id {grid_id}): {e}"
        print(msg)
        error_log.write(msg + "\n")
        results.append({
            "grid_id": grid_id,
            "center_lat": lat,
            "center_lon": lon,
            "region_1depth": None,
            "region_2depth": None,
            "region_3depth": None,
            "region_4depth": None,
            "full_address": None
        })

    # 중간 저장
    if idx % 10000 == 0 and idx > 0:
        pd.DataFrame(results).to_csv("grids_with_address_partial_vworld.csv", index=False, encoding="utf-8-sig")
        print(f"✅ Saved partial result at idx {idx}")

    time.sleep(0.15)  # 과도한 요청 방지

# 최종 저장
pd.DataFrame(results).to_csv("grids_with_address_vworld.csv", index=False, encoding="utf-8-sig")
error_log.close()
print("🎉 모든 작업 완료! → grids_with_address_vworld.csv 생성됨")
