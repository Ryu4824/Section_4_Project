import psycopg2
import requests
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

conn = psycopg2.connect(
    host="rajje.db.elephantsql.com",
    database="zgsqyxsv",
    user="zgsqyxsv",
    password="VqWkTqO1ZHAfB1kS9U0KrsewfimwdlV1"
    )

cur = conn.cursor()
cur.execute("SELECT * FROM tft_db")

# 결과 가져오기
rows = cur.fetchall()
# 컬럼 이름 설정
columns = [desc[0] for desc in cur.description]

# 데이터프레임 생성
df = pd.DataFrame(rows, columns=columns)

# 연결 종료
cur.close()
conn.close()

target_character_id = ['TFT9_Jinx', 'TFT9_Ashe',
       'TFT9_Lissandra', 'TFT9_Ekko', 'TFT9_Sejuani', 'TFT9_Urgot',
       'TFT9_Zeri', 'TFT9_Shen', 'TFT9_Maokai', 'TFT9_Soraka', 'TFT9_Taric',
       'TFT9_Aphelios', 'TFT9_Tristana', 'TFT9_Poppy', 'TFT9_Teemo',
       'TFT9_Senna', 'TFT9_KSante', 'TFT9_Karma', 'TFT9_Gwen', 'TFT9_Nasus',
       'TFT9_Aatrox', 'TFT9_Ahri', 'TFT9_Heimerdinger', 'TFT9_Yasuo', 'TFT9_Sion', 'TFT9_Kled',
       'TFT9_Taliyah', 'TFT9_Swain', 'TFT9_Sona', 'TFT9_VelKoz',
       'TFT9_JarvanIV', 'TFT9_Akshan', 'TFT9_Irelia', 'TFT9_ChoGath',
       'TFT9_Vi', 'TFT9_Reksai', 'TFT9_Kalista', 'TFT9_KaiSa', 'TFT9_Viego',
       'TFT9_Jayce', 'TFT9_Malzahar', 'TFT9_Lux', 'TFT9_Samira',
       'TFT9_Cassiopeia', 'TFT9_Darius', 'TFT9_Katarina', 'TFT9_Azir',
       'TFT9_Kassadin', 'TFT9_BelVeth', 'TFT9_Warwick', 'TFT9_Galio',
       'TFT9_Renekton', 'TFT9_Sett', 'TFT9_Jhin', 'TFT9_Garen', 'TFT9_Zed',
       'TFT9_RyzeShurima', 'TFT9_RyzeFreljord', 'TFT9_Kayle', 'TFT9_Orianna',
       'TFT9_RyzeZaun', 'TFT9_RyzeShadowIsles', 'TFT9_RyzeIonia',
       'TFT9_RyzeDemacia', 'TFT9_RyzeTargon', 'TFT9_RyzeBandleCity',
       'TFT9_RyzePiltover', 'TFT9_RyzeNoxus']

# 컬럼 추가
df = df.reindex(columns=df.columns.tolist() + target_character_id)

# character_id 컬럼 생성 및 값 할당
for i, row in df.iterrows():
    units = row['units']
    for unit in units:
        character_id = unit['character_id']
        tier = unit['tier']
        if character_id in target_character_id:
            df.loc[i, character_id] = tier

# units 컬럼 삭제
df = df.drop('units', axis=1)

# NaN 값은 0으로 채우기
df = df.fillna(0.0)

# 타겟 변수 설정
target = 'placement'

# 특성 변수와 타겟 변수 분리
X = df.drop(target, axis=1)
y = df[target]

# 트레이닝 세트, 검증 세트, 테스트 세트로 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42)

# 랜덤 포레스트 회귀 모델 생성 및 학습
model = RandomForestRegressor()
model.fit(X_train, y_train)

# 검증 세트로 모델 평가
y_pred = model.predict(X_val)
r2 = r2_score(y_val, y_pred)
print(f"Validation R2: {r2}")

# 테스트 세트로 모델 예측
y_pred_test = model.predict(X_test)
print(y_pred_test)
print("-----------------------")
print(y_test)
# 모델 피클링
filename = 'model.pkl'
with open(filename, 'wb') as file:
    pickle.dump(model, file)