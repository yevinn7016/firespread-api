#######NDVI 데이터를 격자에서의 중간값으로 저장하는 코드#######
import pandas as pd
import rasterio

# 파일 경로
grid_csv = "korea_grids_0.01deg.csv"
ndvi_tif = "NDVI_LATEST_250m_fixed.tif"

# 데이터 로드
grid = pd.read_csv(grid_csv)

with rasterio.open(ndvi_tif) as src:
    ndvi = src.read(1)
    transform = src.transform

    values = []
    for i, row in grid.iterrows():
        lon = row['center_lon']
        lat = row['center_lat']

        try:
            col, r = ~transform * (lon, lat)
            col = int(round(col))
            r = int(round(r))

            if 0 <= r < ndvi.shape[0] and 0 <= col < ndvi.shape[1]:
                value = ndvi[r, col]
                values.append(value if value > 0 else None)
            else:
                values.append(None)
        except:
            values.append(None)

# 결과 저장
grid["NDVI"] = values
grid.to_csv("NDVI_processed_point.csv", index=False)
print("✅ 중심점 NDVI 추출 완료 (Python)")
