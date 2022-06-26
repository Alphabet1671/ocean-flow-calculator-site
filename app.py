from flask import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
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


    df = pd.read_csv('translated avg.csv')

    df['velocity'] = np.sqrt(df['ugs'] ** 2 + df['vgs'] ** 2)

    year_vgs = df.groupby(['year', 'month', 'day', 'lat', 'lon'])['vgs'].mean()
    year_ugs = df.groupby(['year', 'lat', 'lon'])['ugs'].mean()
    year_vel = df.groupby(['year', 'lat', 'lon'])['velocity'].mean()

    def Plot_Quiver(year):
        year_len = len(df[(df['year'] == year) & (df['month'] == 1) & (df['day'] == 1)])
        for i in range(len(year_vgs.index)):
            if (year_vgs.index[i] == (year, 34.125, 127.625)):
                vgs = year_vgs[year_vgs.index[i:i + year_len]].values
                ugs = year_ugs[year_ugs.index[i:i + year_len]].values
                vel = year_vel[year_vel.index[i:i + year_len]].values

        vel_q_25 = (np.median(vel) + vel.min()) / 2
        vel_q_50 = np.median(vel)
        vel_q_75 = (np.median(vel) + vel.max()) / 2

        q_25_index = []
        for i in range(len((vel < vel_q_25))):
            if (vel < vel_q_25)[i]:
                q_25_index.append(i)

        q_50_index = []
        for i in range(len(((vel < vel_q_50) & (vel > vel_q_25)))):
            if ((vel < vel_q_50) & (vel > vel_q_25))[i]:
                q_50_index.append(i)

        q_75_index = []
        for i in range(len(((vel < vel_q_75) & (vel > vel_q_50)))):
            if ((vel < vel_q_75) & (vel > vel_q_50))[i]:
                q_75_index.append(i)

        q_75_index_over = []
        for i in range(len((vel < vel_q_75))):
            if (vel > vel_q_75)[i]:
                q_75_index_over.append(i)

        lat = df['lat'][i:i + year_len]
        lon = df['lon'][i:i + year_len]

        plt.figure(figsize=(10, 10))

        plt.quiver(lon.iloc[q_75_index_over], lat.iloc[q_75_index_over], ugs[q_75_index_over], vgs[q_75_index_over],
                   color='red', label='Velocity > Q3', scale=10, width=0.005)
        plt.quiver(lon.iloc[q_75_index], lat.iloc[q_75_index], ugs[q_75_index], vgs[q_75_index], color='orange',
                   label='Q2 < Velocity < Q3', scale=10)
        plt.quiver(lon.iloc[q_50_index], lat.iloc[q_50_index], ugs[q_50_index], vgs[q_50_index], color='yellow',
                   label='Q1 < Velocity < Q2', scale=7)
        plt.quiver(lon.iloc[q_25_index], lat.iloc[q_25_index], ugs[q_25_index], vgs[q_25_index], color='blue',
                   label='Velocity < Q1', scale=5)
        plt.legend()

    def roundPartial(value):
        return round((value - 0.125) / 0.25) * 0.25 + 0.125

    def getVGS(year, month, day, lat, lon):
        return df[df.year == year][df.month == month][df.day == day][df.lat == lat][df.lon == lon].get('vgs').values[0]

    def getUGS(year, month, day, lat, lon):
        return df[df.year == year][df.month == month][df.day == day][df.lat == lat][df.lon == lon].get('ugs').values[0]

    def move(lat, lon, vgs, ugs):
        return lat + vgs, lon + ugs

    def movefordays(year, day, month, lat, lon, daysmoving):
        initialCoor = [lat, lon]
        iniLat = roundPartial(lat)
        iniLon = roundPartial(lon)
        latitude = iniLat
        longitude = iniLon

        vgs1 = getVGS(year, month, day, latitude, longitude)
        ugs1 = getUGS(year, month, day, latitude, longitude)

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
                year = year + 1

            vgs = getVGS(year, month, day1, lati, longi)
            ugs = getUGS(year, month, day1, lati, longi)
            final = [latitude, longitude]
            tracking.append([latitude, longitude])

        return initialCoor, final, tracking

    def plotTracking(trackingList):
        import numpy as np
        import matplotlib.pyplot as plt

        # The data are given as list of lists (2d list)
        data = np.array(trackingList)
        # Taking transpose

        # plot our list in X,Y coordinates
        img = plt.imread("Capture.jpg")
        px = 1 / plt.rcParams['figure.dpi']
        fig, ax = plt.subplots(figsize=(370 * px, 450 * px))
        x = range(300)
        x, y = data.T
        ax.set_ybound(0, 100)
        ax.plot(y, x, linewidth=5, color='firebrick')
        ax.set_ybound(34, 49)
        ax.set_xbound(128, 140)

        x, y = data.T

        # plot our list in X,Y coordinates
        plt.show()

        plt.savefig("test.svg")

def finalFunction(lon, lat, year, month, day, days):
  initialCoor, final, tracking = movefordays(year, day, month, lat, lon, days)

  print("Initial Position: " + initialCoor)
  print("Initial Final: " + final)
  print("After " + days + " days")

  plotTracking(tracking)
#for local testing on editing machine
if __name__ == "__main__":
    app.run(port=2328, host="0.0.0.0", debug=True)
    


