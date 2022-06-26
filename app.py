from flask import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fill-form/", methods=["POST", "GET"])
def fillData():
    lat = request.form["latitude"]
    lon = request.form["longitude"]
    month = request.form["month"]
    date = request.form["date"]

    #back end programming here
    f = open("translated avg.csv", "r")


#for local testing on editing machine
if __name__ == "__main__":
    app.run(port=2328, host="0.0.0.0", debug=True)