import pandas as pd

# 파일 불러오기
fuel = pd.read_csv('Grid_Fuel_Data.csv')
land = pd.read_csv('land_grid_ids_from_spei.csv')

# 컬럼명 소문자로 정리
fuel.columns = fuel.columns.str.lower().str.strip()
land.columns = land.columns.str.lower().str.strip()

# 육지 grid_id 목록
land_ids = land['grid_id'].unique()

# 육지가 아닌 grid_id의 연료량을 NaN으로 설정
fuel.loc[~fuel['grid_id'].isin(land_ids), 'avg_fuelload_pertree_kg'] = float('nan')

# 결과 저장
fuel.to_csv('Grid_Fuel_Data_filtered_by_land.csv', index=False)
