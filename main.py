from flask import Flask, render_template, request
from flask import jsonify
from datetime import datetime, timedelta
from get_prediction import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    center = request.form['input1']
    start_date = request.form['input2']
    end_date = request.form['input3']
    print(center, start_date, end_date)
    datetime_object_start = datetime.strptime(start_date, '%d-%m-%Y')
    datetime_object_end = datetime.strptime(end_date, '%d-%m-%Y')
    print(datetime_object_start, datetime_object_end)
    delta = datetime_object_end - datetime_object_start
    print("Prediction for "+str(delta)+" days will be done.")
    for i in range(delta.days + 1):
        days = datetime_object_start + timedelta(days=i)
        print("Day is "+str(days.day)+" of month "+str(days.month)+" and Year "+str(days.year))
        st = get_prediction(days.day, days.month, days.year, center)
        print(st)
    return render_template('index_helper.html')

if __name__ == '__main__':
    app.run(debug=True)
