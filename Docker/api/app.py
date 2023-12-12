# TODO: dont convert to pickle, but to JSON instead - security, speed
import os
import flask
import utils
from config import models as model_list
from flask import jsonify, render_template, request

models = model_list.models # creating a dict of all models

app = flask.Flask(__name__)
app.config["debug"] = True

@app.route("/")
def home():
    return render_template("index.html", models = list(models.keys()))

@app.route("/predict", methods = ["POST"])
def predict_sales():
    """
    Given the date, predict the number of sales
    """
    print("---------------------------------------------------------------------------------------------------")
    print(os.getcwd())
    try:
        model_name = request.form.get("model_name")
        print("Message-Correct-1--------------------------------------------------------------------------------------------------")
        date_given = request.form.get("date")
        print("Message-Correct-2---------------------------------------------------------------------------------------------------")
        #model = models[model_name]()
        model = "prophet.pckl"
        print("Message-Correct-3---------------------------------------------------------------------------------------------------")
        #pred = utils.ProphetPredictor()
        print("Message-Correct-4---------------------------------------------------------------------------------------------------")
    except KeyError:  # get the value from curl header instead
        model_name = request.headers.get("model_name")
        print("Message 1---------------------------------------------------------------------------------------------------")
        date_given = request.headers.get("date")
        print("Message 2---------------------------------------------------------------------------------------------------")
        model = models[model_name]()
        print("Message 3---------------------------------------------------------------------------------------------------")
        pred = model.predict(date_given)
        print("Message 4---------------------------------------------------------------------------------------------------")
    return jsonify(
        {
            "given_date": date_given,
            "next_date": "test",#model.get_next_date(date_given),
            "sales": "test1",
        },
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0") # running on port 0.0.0.0 means it can be accesed by all IP adresses 