from flask import Flask, render_template, request
from flask import jsonify
from datetime import datetime, timedelta
from get_prediction import *
from models.models import *
from utils.db_handler import *
import pandas as pd
from helper_function import *

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

@app.route('/prediction', methods=['POST'])
def prediction():
    results = session.query(DataNew).limit(10000).all()
    print("Request Recieved <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    for result in results:
        df = pd.DataFrame(data=[(result.id, result.indent, result.purchase, result.date, result.center, 0, 0, 0, 0, 0, 0) for result in results], columns=['id', 'indent', 'purchase',"date", "center", "cummulative_indnet", "cummulative_purchase", "ActiveIndent", "likely_to_purchased", "N_Column", "Failure"])
    print("Done")
    print(df.shape, "First")
    df_updated = calc(df)
    print(df_updated.shape, "Second")
    df_up = failure_calc(df_updated)
    print(df_up.shape, "Third")
    df_failuer = failue_calculation(df_up)
    print(df_failuer.shape, "Third")
    df_failuer.to_csv("my_csv_2.csv")
    pred = get_prediction(df_failuer)
    print("prediction status ", pred)
    session.close()
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
