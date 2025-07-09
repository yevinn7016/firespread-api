import pandas as pd
import matplotlib.pyplot as plt

# 1. 파일 불러오기
df = pd.read_csv('fuel_data_re.csv')

# 2. 유효한 연료량 값 필터링
df = df[df['avg_fuelload_pertree_kg'].notna()]

# 3. 시각화
plt.figure(figsize=(10, 12))
sc = plt.scatter(
    df['center_lon'], df['center_lat'],
    c=df['avg_fuelload_pertree_kg'],
    cmap='hot', s=10, marker='s'
)

plt.colorbar(sc, label='Avg Fuel Load per Tree (kg)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('🔥 Grid Fuel Load over Land (Filtered)')
plt.axis('equal')
plt.grid(True)
plt.show()
