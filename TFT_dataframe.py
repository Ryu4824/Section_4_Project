import requests
import pandas as pd

api_key = 'RGAPI-be4ffd61-2068-401c-95b8-034a06a0283e'
summoner_name = 'YOUCHESS'

# 1. 소환사명을 사용하여 소환사의 고유 ID를 가져옵니다.
summoner_url = f'https://kr.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}?api_key={api_key}'
response = requests.get(summoner_url)
print(response)

summoner_data = response.json()
puuid = summoner_data['puuid']
print(puuid)

# 2. 소환사의 고유 ID를 사용하여 대전 기록을 가져옵니다.
match_url = f'https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={api_key}'
response = requests.get(match_url)
print(response)
match_data = response.json()

# 3. 대전 기록의 JSON 응답을 출력합니다.
print(match_data)

# 데이터 프레임 생성을 위한 빈 리스트 생성
df_data = []

for match_id in match_data:
    game_url = f'https://asia.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={api_key}'
    response = requests.get(game_url)
    print(response)
    game_data = response.json()

    participants = game_data["info"]["participants"]

    for participant in participants:
        gold_left = participant["gold_left"]
        last_round = participant["last_round"]
        level = participant["level"]
        players_eliminated = participant["players_eliminated"]
        time_eliminated = participant["time_eliminated"]
        total_damage_to_players = participant["total_damage_to_players"]
        units = []
        for unit in participant["units"]:
            character_id = unit["character_id"]
            tier = unit["tier"]
            units.append({"character_id": character_id, "tier": tier})

        placement = participant["placement"]
        df_data.append([gold_left, last_round, level, players_eliminated, time_eliminated, total_damage_to_players, units, placement])

# 데이터 프레임 생성
columns = ["Gold_Left", "Last_Round", "Level", "Players_Eliminated", "Time_Eliminated", "Total_Damage", "Units", "Placement"]
df = pd.DataFrame(df_data, columns=columns)

# character_id 컬럼 생성 및 값 할당
for i, row in df.iterrows():
    units = row['Units']
    for unit in units:
        character_id = unit['character_id']
        tier = unit['tier']
        df.loc[i, character_id] = tier

# units 컬럼 삭제
df = df.drop('Units', axis=1)

# NaN 값은 0으로 채우기
df = df.fillna(0)
df
