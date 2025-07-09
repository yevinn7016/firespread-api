#########수집한 NDVI geotiff 파일에 대해 더 자세히 만드는 코드##########
import rasterio
from rasterio.transform import from_bounds
from rasterio.crs import CRS

# 1. 기존 NDVI tif 파일 경로
input_tif = "NDVI_LATEST_250m.tif"

# 2. 새로 저장할 파일 경로
output_tif = "NDVI_LATEST_250m_fixed.tif"

# 3. 위도·경도 범위 (예빈이가 확인한 값 기준)
lat_min, lat_max = 32.9996, 38.5400
lon_min, lon_max = 124.4998, 130.5005

# 4. 기존 tif 불러오기
with rasterio.open(input_tif) as src:
    ndvi = src.read(1)  # 첫 번째 밴드
    height, width = src.height, src.width

# 5. 좌표계 및 transform 설정
transform = from_bounds(lon_min, lat_min, lon_max, lat_max, width, height)
crs = CRS.from_epsg(4326)  # WGS84 좌표계 (EPSG:4326)

# 6. GeoTIFF 다시 저장
with rasterio.open(
    output_tif,
    "w",
    driver="GTiff",
    height=height,
    width=width,
    count=1,
    dtype=ndvi.dtype,
    crs=crs,
    transform=transform,
) as dst:
    dst.write(ndvi, 1)

print("✅ GeoTIFF 저장 완료:", output_tif)
