from flask import Flask
from flask import render_template
import requests

app = Flask(__name__)

raspi_endpoint = "http://127.0.0.1:5000/api"

@app.route('/')
def index():
    try:
        meal_times = get_meal_times()
        avg_weight = calc_avg(meal_times)

        chart_lables = []
        chart_datas = []
        for meal_time in meal_times:
            chart_lables.append(f'{meal_time["date"]} {meal_time["date_m_s"]}')
            chart_datas.append(meal_time["weight"])
        chart_datastr = ",".join(str(i) for i in chart_datas)

        schedules = get_schedules()

        param_dict = dict()
        param_dict["chart_datastr"] = chart_datastr
        param_dict["chart_lables"] = chart_lables
        param_dict["avg_weight"] = avg_weight
        param_dict["schedules"] = schedules
       

    except Exception as e:
        print('Error occured.', e)
        return render_template('error.html')

    return render_template('index.html', params=param_dict)


def get_meal_times():
    response = requests.get(f'{raspi_endpoint}/mealdata/21')
    meal_times = response.json()

    meal_times = sorted(meal_times, key=(lambda x: (x['date'],x['date_m_s'])) )
    return meal_times

def calc_avg(meal_times):
    total_meal_weight = 0
    for meal_time in meal_times:
        total_meal_weight += int(meal_time["weight"])

    avg_weight = round(total_meal_weight / len(meal_times),1)
    return avg_weight

def get_schedules():
    # response = requests.get(f'{raspi_endpoint}/mealdata/21')
    # meal_times = response.json()

    schedules = dict()
    schedules["breakfast"] = {"start": "09:00", "end":"10:00"}
    schedules["lunch"] = {"start": "09:00", "end":"10:00"}
    schedules["dinner"] = {"start":"09:00", "end":"10:00"}

    return schedules

if __name__ == '__main__':
 app.run(host='0.0.0.0', port="8080")