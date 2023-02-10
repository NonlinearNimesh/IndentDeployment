from flask import Flask, render_template, request, make_response
from flask import jsonify
from datetime import datetime, timedelta
from celery import Celery
from get_prediction import *
from models.models import *
from utils.db_handler import *
from utils.db_handler import SessionLocal, engine
import pandas as pd
from helper_function import *
import csv
import io
from pydantic import BaseModel
from models import models
from crud import crud
from datetime import datetime

print("Establishing Connection with Database .... ")
models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
print("Connection Established Successfully ....")

flask_app = Flask(__name__)
# redis_url = "redis://localhost:6379/0"
# celery_app = Celery('Indent', broker=redis_url)


@flask_app.route('/')
def initial():
    return render_template('login.html')

@flask_app.route('/logintoregister')
def register_page():
    return render_template('registration.html')


class UsersClass(BaseModel):
    name: str = None
    username: str = None
    password: str = None
    email: str = None
    role: str = None
    key_expires: str = None
    created_on: str = None
    secret_key: str = None

@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    db = SessionLocal()
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        #role = request.form['role']
        role = "user"
        existing_user = db.query(models.Users).filter(models.Users.username == username).first()
        if existing_user:
            db.close()
            return "This username is already taken, Please choose another one"
        else:
            x = UsersClass(id=id, name=str(name), username=str(username), password=str(password), email=str(email), role=str(role), key_expires=str(datetime.utcnow()), created_on=str(datetime.utcnow()), secret_key="")
            crud.add_details_to_db(db=db, users=x)
            db.close()
            return render_template("login.html")

@flask_app.route('/homepage')
def index():
    return render_template('index.html')

@flask_app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = SessionLocal()
        username = request.form['username']
        password = request.form['password']
        user = db.query(models.Users).filter(models.Users.username == username).first()
        if user:
            if user.password == password:
                return render_template("index.html", username=username)
            else:
                db.close()
                return "Incorrect Password"
        else:
            db.close()
            return "You are Not register, please Register yourself first."

@flask_app.route('/submit', methods=['POST'])
def submit():
    center = request.form['input1']
    start_date = request.form['input2']
    end_date = request.form['input3']
    end_center = request.form['input4']
    criteria = request.form.get('criteria')
    if criteria == 'date':
        datetime_object_start = datetime.strptime(start_date, '%d-%m-%Y')
        datetime_object_end = datetime.strptime(end_date, '%d-%m-%Y')
        print(datetime_object_start, datetime_object_end)
        rows = session.query(DataNew).filter(DataNew.date.between(datetime_object_start, datetime_object_end)).all()
        with open(f'{start_date}_to_{end_date}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["date", "center", "center_name", "predicted_indent"])
            for row in rows:
                writer.writerow([row.date, row.center, row.center_name, row.predicted_indent])

            si = io.StringIO()
            cw = csv.writer(si)
            cw.writerow(["date", "center", "center_name", "predicted_indent"])  # Write the header row
            for row in rows:
                cw.writerow([row.date, row.center, row.center_name, row.predicted_indent])

            output = make_response(si.getvalue())
            output.headers["Content-Disposition"] = f"attachment; filename={start_date}_to_{end_date}.csv"
            output.headers["Content-type"] = "text/csv"
        return output
    else:
        print(center, end_center)
        rows = session.query(DataNew).filter(DataNew.center.between(center, end_center)).all()
        # Write the rows to a CSV file
        with open(f'{center}_to_{end_center}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["date", "center", "center_name", "predicted_indent"])
            for row in rows:
                writer.writerow([row.date, row.center, row.center_name, row.predicted_indent])

            si = io.StringIO()
            cw = csv.writer(si)
            cw.writerow(["date", "center", "center_name", "predicted_indent"])  # Write the header row
            for row in rows:
                cw.writerow([row.date, row.center, row.center_name, row.predicted_indent])

            output = make_response(si.getvalue())
            output.headers["Content-Disposition"] = f"attachment; filename={center}_to_{end_center}.csv"
            output.headers["Content-type"] = "text/csv"
        return output


@flask_app.route('/prediction', methods=['POST'])
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
    flask_app.run(debug=True)
