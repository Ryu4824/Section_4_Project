import psycopg2
import requests
import pandas as pd
import json

def collect_data():
    conn = psycopg2.connect(
        host="rajje.db.elephantsql.com",
        database="zgsqyxsv",
        user="zgsqyxsv",
        password="VqWkTqO1ZHAfB1kS9U0KrsewfimwdlV1"
        )

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tft_db(
            Gold_Left INT,
            Last_Round INT,
            Level INT,
            Players_Eliminated INT,
            Time_Eliminated FLOAT,
            Total_Damage INT,
            Units JSONB,
            Placement INT
        );
    """)
    conn.commit()
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
    match_url = f'https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count=10&api_key={api_key}'
    response = requests.get(match_url)
    print(response)
    match_data = response.json()

    # 3. 대전 기록의 JSON 응답을 출력합니다.
    print(match_data)

    for match_id in match_data:
        game_url = f'https://asia.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={api_key}'
        response = requests.get(game_url)
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
            units_json = json.dumps(units)
            placement = participant["placement"]
            cur.execute("INSERT INTO TFT_DB VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;",
                        (gold_left, last_round, level, players_eliminated, time_eliminated,
                        total_damage_to_players,units_json, placement))
    conn.commit()
    cur.close()
    conn.close()