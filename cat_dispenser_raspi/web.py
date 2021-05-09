import datetime
import json
from flask import Flask, jsonify

app = Flask(__name__)

text_url="../RaspberryPiTemp-dispenser/mealdata.txt" # 파일 위치

@app.route("/")
def http_prepost_response():
    return "Hello word"

@app.route("/api/mealdata/<count>")
def get_mealdata(count):
    meal_times = read_file(int(count))
    return jsonify(meal_times), 200

def read_file(count):
    meal_times = []
    f=open(text_url,"r",encoding="utf8")
    lines=f.readlines()
    f.close()

    i = -1

    length = len(lines)
    meal_count = 0

    while abs(i) < length and meal_count < count:

        while True:
            if lines[i].startswith("eat time"):
                break
            i = i - 1

        meal_time = dict()   
        try: 
            meal_time["eat_time"] = int(lines[i].split(':')[1])
        except ValueError :
            meal_time["eat_time"] = 0 
        i -= 1
        try: 
            meal_time["weight"] = int(lines[i].split(':')[1])
        except ValueError :
            meal_time["weight"] = 0 

        i -= 1
        meal_time["time"] = lines[i].split(' ')[0].rstrip()
        meal_time["date_m_s"] = lines[i][0:7].rstrip()
        i -= 1
        meal_time["date"] = lines[i].rstrip()
        i -= 1
        meal_times.append(meal_time)
        meal_count += 1
    
    return meal_times

@app.route("/api/avg_meal_weight")
def get_avg_meal_weight():
    meal_times = read_file(21)
    total_meal_weight = 0
    for meal_time in meal_times:
        total_meal_weight += int(meal_time["weight"])
    
    avg_weight = round(total_meal_weight / len(meal_times),1)

    avg_weight_dict = dict()
    avg_weight_dict["avg_weight"] = avg_weight

    return jsonify(avg_weight_dict), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0")