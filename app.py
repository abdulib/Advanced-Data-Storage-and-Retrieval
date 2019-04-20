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

@app.route("/api/<start>")
def trip1(start):
    
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

#################################################
@app.route("/api/<start>/<end>")
def trip2(start,end):
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)


#################################################



if __name__ == '__main__':
    app.run(debug=True)
