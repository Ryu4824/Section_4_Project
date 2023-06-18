import os
from flask import Flask, render_template, request
import pickle

# 현재 파일의 절대 경로를 기반으로 모델 파일의 경로를 지정
model_path = os.path.join(os.path.dirname(__file__), '../models/model.pkl')

# 모델 로드
with open(model_path, 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('base.html',target_character_id=target_character_id)

@app.route('/predict', methods=['POST'])
def predict():
    gold_left = int(request.form.get('gold_left'))
    last_round = int(request.form.get('last_round'))
    level = int(request.form.get('level'))
    players_eliminated = int(request.form.get('players_eliminated'))
    time_eliminated = float(request.form.get('time_eliminated'))
    total_damage = int(request.form.get('total_damage'))

    input_values = {
        'gold_left': gold_left,
        'last_round': last_round,
        'level': level,
        'players_eliminated': players_eliminated,
        'time_eliminated': time_eliminated,
        'total_damage': total_damage
    }

    for character in target_character_id:
        selected_value = request.form.get(character)
        if selected_value:
            input_values[character] = int(selected_value)
        else:
            input_values[character] = 0

    # 입력된 값들을 모델에 전달하여 예측 수행
    prediction = model.predict([list(input_values.values())])
    return render_template('predict.html', prediction=prediction)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')