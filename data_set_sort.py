import pandas as pd

# 1. 기준이 되는 전체 격자 정보 로드
grids_df = pd.read_csv("korea_grids_0.01deg.csv")  # grid_id, lon_center, lat_center 등이 포함

# 2. fuel_data_resujip.csv 파일 로드 (일부 grid_id만 포함된 연료 데이터)
fuel_df = pd.read_csv("fuel_data_re.csv")  # grid_id, avg_fuel 등

# 3. 기준 격자를 기준으로 left join → 누락된 grid_id는 NaN으로 채움
merged_df = grids_df.merge(fuel_df, on="grid_id", how="left")

# 4. grid_id 기준으로 정렬 (보통 0부터 정렬되도록 함)
merged_df = merged_df.sort_values(by="grid_id").reset_index(drop=True)

# 5. 최종 파일 저장
merged_df.to_csv("fuel_data_aligned_to_grids.csv", index=False)
