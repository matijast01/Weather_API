from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    station_id = station.zfill(6)
    filename = f"data_small/TG_STAID{station_id}.txt"

    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])

    date_row = df.loc[df['    DATE'] == date]
    temperature = date_row['   TG'].squeeze() / 10

    return {"station": station,
            "date": date,
            "temperature": temperature}


if __name__ == "__main__":
    app.run(debug=True)
