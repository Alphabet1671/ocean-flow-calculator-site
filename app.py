from flask import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fill-form/", methods=["POST","GET"])
def fillData():
    #back end programming here




#for local testing on editing machine
if __name__ == "__main__":
    app.run(port=2328, host="0.0.0.0", debug=True)