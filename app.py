import base64

from flask import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from io import BytesIO

app = Flask(__name__)
df = pd.read_csv('finalized-data1.csv', index_col=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fill-form/", methods=["POST"])
def fillData():
    lat = round((float(request.form["lat"]) - 0.125) / 0.25) * 0.25 + 0.125
    lon = round((float(request.form["long"]) - 0.125) / 0.25) * 0.25 + 0.125
    date_str = request.form["trip-start"]
    lst = date_str.split("-")
    year = int(lst[0])  # make use of this shit later
    month = int(lst[1])
    date = int(lst[2])
    dur = int(request.form["dur"])

    # back end programming here

    def roundPartial(value):
        return round((value - 0.125) / 0.25) * 0.25 + 0.125

    def move(lat, lon, vgs, ugs):
        return lat + vgs, lon + ugs

    def movefordays(year, day, month, lat, lon, daysmoving):

        initialCoor = [lat, lon]
        iniLat = roundPartial(lat)
        iniLon = roundPartial(lon)
        latitude = iniLat
        longitude = iniLon
        # test w/ 43.375,136.625
        vgs1 = df[df.year == year][df.month == month][df.day == day][df.lat == latitude][df.lon == longitude].get(
            'vgs').values[0]
        ugs1 = df[df.year == year][df.month == month][df.day == day][df.lat == latitude][df.lon == longitude].get(
            'ugs').values[0]
        print(vgs1)
        print(ugs1)
        day1 = day
        vgs = vgs1
        ugs = ugs1

        final = []
        tracking = []

        for i in range(daysmoving):
            latitude, longitude = move(latitude, longitude, vgs, ugs)
            lati = roundPartial(latitude)
            longi = roundPartial(longitude)
            day1 = day1 + 1

            if (day1 > 28):
                day1 = 1
                month = month + 1

            if (month > 12):
                month = 1
                #  year = year + 1
                
                
            try:
               vgs = df[df.year == year][df.month == month][df.day == day1][df.lat == lati][df.lon == longi].get(
                    'vgs').values[0]
               ugs = df[df.year == year][df.month == month][df.day == day1][df.lat == lati][df.lon == longi].get(
                    'ugs').values[0]
            except:
                print('Out of bounds')
                break
                
            final = [latitude, longitude]
            print(final)
            tracking.append([latitude, longitude])

        return initialCoor, final, tracking

    # dont touch what's below this!!!

    trackingList = movefordays(2018, date, month, lat, lon, dur)

    # The data are given as list of lists (2d list)
    data = np.array(trackingList[2])
    # Taking transpose
    # plot our list in X,Y coordinates
    px = 1 / plt.rcParams['figure.dpi']
    fig = Figure(figsize=[370*px, 450*px])
    ax = fig.subplots()
    x = range(300)
    y = range(300)
    x, y = data.T
    ax.set_ybound(0, 100)
    ax.plot(y, x, linewidth=3, color='firebrick')
    ax.set_ybound(34, 49)
    ax.set_xbound(128, 140)
    buf = BytesIO()
    fig.savefig(buf,format="png")
    data1 = base64.b64encode(buf.getbuffer()).decode("ascii")
    print(data1)
    return render_template("result.html", value=data1, origin=trackingList[0], final=trackingList[1], dateIn=date_str, dur=dur)


# for local testing on editing machine

if __name__ == "__main__":
    app.run(port=2328, host="0.0.0.0", debug=True)
