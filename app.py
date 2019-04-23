import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/precipitation<br/>"
        f"<br/>"
        f"/api/stations<br/>"
        f"<br/>"
        f"/api/temperature<br/>"
        f"<br/>"
        f"/api/<start><br/>"
        f"<br/>"
        f"/api/<start>/<end>"
    )

#################################################

@app.route("/api/precipitation")
def precipitation():
    """Convert the query results to a Dictionary using date as the key and prcp as the value.
        Return the JSON representation of your dictionary."""
    results = session.query(Measurement.date, Measurement.prcp).all()

    dates_n_prcp = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        dates_n_prcp.append(prcp_dict)

    return jsonify(dates_n_prcp)

#################################################
@app.route("/api/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    results = session.query(Station.name).all()

    stations_list = []

    for name in results:
        station_dict = {}
        station_dict['name'] = name
        stations_list.append(station_dict)

    return jsonify(stations_list)



#################################################


@app.route("/api/temperature")
def temperature():
    """ query for the dates and temperature observations from a year from the last data point.
        Return a JSON list of Temperature Observations (tobs) for the previous year. """

    results = session.query(Measurement.date, Measurement.tobs ).\
        filter(Measurement.date >= dt.date(2017, 8, 23) - dt.timedelta(days=365))

    tobs_list = []

    for date, tobs in results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)


#################################################

@app.route('/api/v1.0/<date>/')
def given_date(date):
    """Return the average temp, max temp, and min temp for the date"""
    results = session.query(Measurement.date, func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date == date).all()

#Create JSON
    data_list = []
    for result in results:
        row = {}
        row['Date'] = result[0]
        row['Average Temperature'] = float(result[1])
        row['Highest Temperature'] = float(result[2])
        row['Lowest Temperature'] = float(result[3])
        data_list.append(row)

    return jsonify(data_list)


#################################################
@app.route('/api/v1.0/<start_date>/<end_date>/')
def query_dates(start_date, end_date):
    """Return the avg, max, min, temp over a specific time period"""
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    data_list = []
    for result in results:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Average Temperature"] = float(result[0])
        row["Highest Temperature"] = float(result[1])
        row["Lowest Temperature"] = float(result[2])
        data_list.append(row)
    return jsonify(data_list)


#################################################



if __name__ == '__main__':
    app.run(debug=True)
