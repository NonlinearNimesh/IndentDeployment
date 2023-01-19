import pickle
import warnings
warnings.filterwarnings("ignore")


def get_prediction(day, month, year, center, failure=0):
    print("IN GET ROWS")
    try:
        model = pickle.load(open("indent_rf_random.pkl", "rb"))
        day = day
        month = month
        year = year
        center = center
        list_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 25, 26, 27, 28, 29,30]  # date of start and end month when mills are shut
        list_month = [6, 7, 8, 9, 10]
        print(day, month, year, center)
        if month not in list_month:
            prediction = model.predict([[center, day, month, year, failure]])
            print("This is the prediction "+str(prediction[0])+" for day "+str(day)+" month "+str(month)+" year "+str(year))
        elif month == 6 or month == 10:
            if day not in list_day:
                prediction = model.predict([[center, day, month, year, failure]])
                print("This is the prediction "+str(prediction[0])+" for day "+str(day)+" month "+str(month)+" year "+str(year))
            else:
                print("Mill will be shut, get data from master table")
        else:
            print("Mill will be shut, get data from master table")

        return "Prediction Done"
    except Exception as e:
        print(e)
