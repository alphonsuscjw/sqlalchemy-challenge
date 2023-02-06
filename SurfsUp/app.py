import numpy as np

# Python SQL toolkit and Object Relational Mapper
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Flask app
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Homepage that lists all available api routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Homepage<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd (Enter a start date in YYYY-MM-DD format. Start date must be no later than 2017-08-23.)<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd (Enter a start date followed by an end date in YYYY-MM-DD format. Dates must be no later than 2017-08-23.)"
    )

# Precipitation route that returns jsonified precipitation data for the last year in the database
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and precipitation for the last year in the database"""
    # Query all dates and precipitation for the last year in the database
    results = session.query(Measurement.date, Measurement.prcp).filter((Measurement.date >= "2016-08-23") \
        & (Measurement.date <= "2017-08-23")).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

# Stations route that returns jsonified data of all of the stations in the database
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return relevant data of all stations"""
    # Query relevant data of all stations
    results = session.query(Station.station, Station.name, Station.latitude, \
        Station.longitude, Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longtitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)

# Tobs route that returns jsonified data for the most active station (USC00519281) for the last year in the database
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tempratures of the last year in the database for the most active station"""
    # Query all dates and temperatures of the last year in the database for the most active station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station=="USC00519281").filter((Measurement.date >= "2016-08-18") \
            & (Measurement.date <= "2017-08-18")).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_temp
    all_temp = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temperature"] = tobs
        all_temp.append(tobs_dict)

    return jsonify(all_temp)

# Start route that returns the minimum, average and maximum temperatures
# calculated from the given start date to the end of the dataset
@app.route("/api/v1.0/<start>")
def start_only(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the minimum, average and maximum temperatures calculated from a specified start date to the end of the dataset"""
    # Query and calculate the minimum, average and maximum temperatures from a specified start date to the end of the dataset
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()
    
    # Create a dictionary from the row data and append to a list of all_temp_start
    all_temp_start = []
    for min, avg, max in results:
        temp_start_dict = {}
        temp_start_dict["min"] = min
        temp_start_dict["avg"] = avg
        temp_start_dict["max"] = max
        all_temp_start.append(temp_start_dict)

    return jsonify(all_temp_start)

# Start/end route that returns the minimum, average and maximum temperatures
# calculated from the given start date to the given end date
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the minimum, average and maximum temperatures calculated from a specified start date to a specified end date"""
    # Query and calculate the minimum, average and maximum temperatures from a specified start date to a specified end date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter((Measurement.date >= start) & (Measurement.date <= end)).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_temp_start_end
    all_temp_start_end = []
    for min, avg, max in results:
        temp_start_end_dict = {}
        temp_start_end_dict["min"] = min
        temp_start_end_dict["avg"] = avg
        temp_start_end_dict["max"] = max
        all_temp_start_end.append(temp_start_end_dict)

    return jsonify(all_temp_start_end)

# Define main behaviour
if __name__ == "__main__":
    app.run(debug=True)