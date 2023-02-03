import pandas as pd
from models.models import *
from utils.db_handler import *
import pandas as pd
from helper_function import *

def calc(df):
    try:
        print("In Calc......................................")
        prev = 0
        prev_purchase = 0
        can_be_purchased = 0
        for index, row in df.iterrows():
            cum_indent = prev + row["indent"]
            #print(prev_purchase, ">>>>>>>>>>>>>>" ,row["purchase"])
            cum_purchase = prev_purchase + row["purchase"]
            df.loc[index, "cummulative_indnet"] = cum_indent
            df.loc[index, "cummulative_purchase"] = cum_purchase
            df.loc[index, "ActiveIndent"] = row["cummulative_indnet"] - row["cummulative_purchase"]
            likely_purchased = can_be_purchased + row["ActiveIndent"]
            df.loc[index, "likely_to_purchased"] = likely_purchased
            prev = cum_indent
            prev_purchase = cum_purchase
            can_be_purchased = likely_purchased
        return df
    except Exception as e:
        print("In calc Exception ::::::::::::::::::::::::::::::::::::::", e)



def failure_calc(df):
    try:
        column_N = []
        for k,l in zip(df.likely_to_purchased[3:], df.ActiveIndent):
          someting_N_column = k - l
          column_N.append(someting_N_column)
        print("Done")
        column_N.insert(0, 0)
        column_N.insert(1, 0)
        column_N.insert(2, 0)
        print(len(column_N))
        df["N_Column"] = column_N
        return df
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        #print("In failure calc Exception...............", e)


def failue_calculation(df):
    print(df["likely_to_purchased"], "<<<<<<<<<<<<<<<", df["N_Column"])
    df["Failure"] = df["likely_to_purchased"] - df["N_Column"]
    df.Failure[0] = 0
    df.Failure[1] = 0
    df.Failure[2] = 0
    df = df.drop(columns=['cummulative_indnet', 'cummulative_purchase', 'ActiveIndent', 'likely_to_purchased', 'N_Column'])
    print("Done <<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>")
    return df

def get_prediction(df):
    import pickle
    model = pickle.load(open("ml_model/indent_rf_random.pkl", "rb"))
    print("Model Loaded")
    for index, row in df.iterrows():
        try:
            day_ = pd.to_datetime(row["date"], format="%d-%m-%Y").day
            month_ = pd.to_datetime(row["date"], format = "%d-%m-%Y").month
            year_ = pd.to_datetime(row["date"], format = "%d-%m-%Y").year
            failure_ = row["Failure"]
            center_ = row["center"]
            print(center_ ,day_, month_, year_, failure_)
            prediction = model.predict([[center_ ,day_, month_, year_, failure_]])
            results = session.query(DataNew).filter(DataNew.id == row["id"]).first()
            results.predicted_indent = prediction[0]
            session.commit()
            df.loc[index, "predicted_indent"] = prediction[0]
            session.close()
            return "success"
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return "failed"