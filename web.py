from flask import Flask
from datetime import datetime
import requests

app = Flask(__name__)

def get_meal(sc, msc, date):
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    headers = { "Content-type": "application/json" }

    payload_today = {
        "KEY": "your api key",
      #api 키를 your api key 에 넣어주세요
        "Type": "json",
        "pIndex": 1,
        "pSize": 1,
        "ATPT_OFCDC_SC_CODE": msc,
        "SD_SCHUL_CODE": sc,
        "MLSV_YMD": date,
    }

    response_today = requests.get(url, params=payload_today, headers=headers)
    data_today = response_today.json()

    try:
        meal_data_today = data_today["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]
        cleaned_info_today = "<br>".join(''.join(c for c in line if c not in '()0123456789.').strip() for line in meal_data_today.split("<br/>"))
    except KeyError:
        cleaned_info_today = "급식 정보를 불러올 수 없습니다. 이는 오늘 급식이 없거나 서버의 문제일수도 있습니다."

    return cleaned_info_today

@app.route('/')
def get_meal_info():
    now = datetime.now().strftime("%Y%m%d")
    sc = "your school code"
  #학교 코드를 넣어주세요 ex)11223344
    msc = "your region"
  #시도 교육청 코드를 넣어주세요 ex) S10
    today_meal = get_meal(sc,msc,now)
    styled_meal_info = f"<div style='font-size: 20px;'>{today_meal}</div>"
  #font-size : 폰트크기px
    return styled_meal_info

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
  #기본 포트는 겹치기 않기 위해 5555 입니다
