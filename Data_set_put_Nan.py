import pandas as pd

# 파일 불러오기
df = pd.read_csv("input_data_set_Nan_x.csv.csv")  # 또는 .xlsx

# 범위 지정: 0~330000번째 행까지만 복사
df_part = df.iloc[:330001].copy()

# 이 범위에 대해서만 빈 셀을 "NaN"으로 채움
df_part.fillna("NaN", inplace=True)

# 나머지 행 (330001 이후)은 그대로 유지
df_rest = df.iloc[330001:]

# 두 개 합치기
df_final = pd.concat([df_part, df_rest])

# 저장
df_final.to_csv("input_data_set.csv", index=False)
