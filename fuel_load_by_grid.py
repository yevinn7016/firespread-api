import pandas as pd
import requests
import time
import os

# Kakao REST API 키
KAKAO_REST_API_KEY = "491436db61dffa2a15c5c5880dc2d674"

# 격자 파일 불러오기
grids = pd.read_csv("korea_grids_0.01deg.csv")

# 좌표 컬럼 맞추기
latlon = grids[['grid_id', 'center_lat', 'center_lon']].copy()
latlon.columns = ['grid_id', 'lat', 'lon']


# 주소 조회 함수
def get_kakao_address(lat, lon):
    url = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
    params = {"x": lon, "y": lat}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            result = response.json()
            if result['documents']:
                doc = result['documents'][0]
                return pd.Series([doc['region_2depth_name'], doc['region_3depth_name']])  # 시군구, 읍면동
        return pd.Series([None, None])
    except Exception as e:
        return pd.Series([None, None])


# 결과 저장 리스트
results = []

# 시작 인덱스 지정 가능 (중간부터 재시작할 수 있음)
start_idx = 0

# 폴더 생성
output_folder = "reverse_geocoded_chunks"
os.makedirs(output_folder, exist_ok=True)

# 반복 처리
for idx, row in latlon.iloc[start_idx:].iterrows():
    시군구, 읍면동 = get_kakao_address(row['lat'], row['lon'])
    results.append({
        'grid_id': row['grid_id'],
        'lat': row['lat'],
        'lon': row['lon'],
        '시군구': 시군구,
        '읍면동': 읍면동
    })

    # 100건마다 저장
    if (idx + 1) % 100 == 0:
        chunk_df = pd.DataFrame(results)
        chunk_df.to_csv(f"{output_folder}/grid_reverse_geocoded_{idx + 1}.csv", index=False, encoding="utf-8-sig")
        print(f"✅ {idx + 1}개 저장 완료")
        results = []  # 저장 후 리스트 초기화

    time.sleep(0.4)  # 요청 간 딜레이 (초당 2.5건)

# 남은 결과가 있다면 마지막으로 저장
if results:
    chunk_df = pd.DataFrame(results)
    chunk_df.to_csv(f"{output_folder}/grid_reverse_geocoded_{idx + 1}_last.csv", index=False, encoding="utf-8-sig")
    print("✅ 마지막 저장 완료")
