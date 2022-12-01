from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def specific_data(station, date):
    station_id = station.zfill(6)
    filename = f"data_small/TG_STAID{station_id}.txt"

    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])

    date_row = df.loc[df['    DATE'] == date]
    temperature = date_row['   TG'].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": temperature}


@app.route("/api/v1/annual/<station>/<year>")
def year_data(station, year):
    station_id = station.zfill(6)
    filename = f"data_small/TG_STAID{station_id}.txt"

    df = pd.read_csv(filename, skiprows=20)
    df["TG"] = df["   TG"] / 10
    df = df[["    DATE", "TG"]]
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    for date_temp in result:
        date_temp["    DATE"] = date_temp["    DATE"][:4] \
                                + "-" + date_temp["    DATE"][4:6] \
                                + "-" + date_temp["    DATE"][6:]
    return result


@app.route("/api/v1/<station>")
def all_data(station):
    station_id = station.zfill(6)
    filename = f"data_small/TG_STAID{station_id}.txt"

    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    df["TG"] = df["   TG"] / 10
    df = df[["    DATE", "TG"]]
    result = df.to_dict(orient="records")

    return result


if __name__ == "__main__":
    app.run(debug=True)
