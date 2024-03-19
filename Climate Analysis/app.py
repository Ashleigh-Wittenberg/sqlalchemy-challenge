# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine,reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# Start page with all routes listed

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp_by/start_date/<start_date><br/>"
        f"/api/v1.0/temp_by/start_date/end_date/<start_date>/<end_date>"
    )

# Percipitation page showing prcp amount for each date

@app.route("/api/v1.0/precipitation")
def percipitation():
    session = Session(engine)
    last_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_date).all()
    session.close()
    percip_mes = list(np.ravel(results))
    return jsonify(percip_mes)

# Station page showing the list of all the data collerction stations

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    total_stations = session.query(Station.station)
    session.close()

    station_list = []
    for st in total_stations:
        station_dict = {
            "Station": st.station,
        }
        station_list.append(station_dict)
    return jsonify(station_list)

# Tobs page showing the temperature information for the most active station for the previous year of data

@app.route("/api/v1.0/tobs")
def tobs():
     session = Session(engine)
     last_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
     active=session.query(Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date >= last_date).all()
     most_act = list(np.ravel(active))
     return jsonify(most_act)

# Start date page showing the calculated temp-min, temp-ave, and temp-max from the start date specified by the user to the end date of the dataset

@app.route("/api/v1.0/temp_by/start_date/<start_date>")
def temp_by_start(start_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs) ,func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()

    temp_list = []
    for result in results:
        temp_dict = {
            "Tmin": result[0],
            "Tavg": result[1],
            "Tmax": result[2]
        }
        temp_list.append(temp_dict)
    return jsonify(temp_list)

# Start & end date page showing the calculated temp-min, temp-ave, and temp-max from the start & end date specified by the user

@app.route("/api/v1.0/temp_by/start_date/end_date/<start_date>/<end_date>")
def temp_by_start_end(start_date, end_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date ).all()
    session.close()

    temp_list = []
    for result in results:
        temp_dict = {
            "Tmin": result[0],  
            "Tavg": result[1],  
            "Tmax": result[2]   
        }
        temp_list.append(temp_dict)
    return jsonify(temp_list)


if __name__ == "__main__":
    app.run(debug=True)

