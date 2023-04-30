import numpy as np
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

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temperature/<start><br/>"
        f"/api/v1.0/temperature_range/<start>/<end>"
    )

###############################################Precipitation#################################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date_year_ago = dt.datetime.strptime(start_date[0], "%Y-%m-%d") - dt.timedelta(days=365)
    """Return a list of all dates and precipitation"""
    # Query all dates and prcp
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date_year_ago).order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal dict
    all_data = {date:prcp for date,prcp in results}
       

   # all_data = []
    #for date, prcp in results:
    #    data_dict = {}
     #   data_dict["date"] = date
      #  data_dict["prcp"] = prcp
       # all_data.append(data_dict)
    return jsonify(all_data)
###############################################Station#################################################################
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of all dates and precipitation"""
    # Query all stations
    results = session.query(Measurement.station).all()
                    

    session.close()

    # Convert list of tuples into normal list
    
    all_data = []
    for station in results:
        data_dict = {}
        data_dict["station"] = station
        
        all_data.append(data_dict)
    return jsonify(all_data)
###############################################Tobs#################################################################
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return  minimum temperature, the average temperature, and the max temperature for a given start or start-end range"""
    # Query the dates and temperature observations of the most active station for the latest year of data
    start_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date_year_ago = dt.datetime.strptime(start_date[0], "%Y-%m-%d") - dt.timedelta(days=365)


    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= date_year_ago).filter(Measurement.station == "USC00519281").order_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_data
    all_data = []
    for date, tobs in results:
        data_dict = {}
        data_dict["date"] = date
        data_dict["tobs"] = tobs
        all_data.append(data_dict)

    return jsonify(all_data)

@app.route("/api/v1.0/temperature/<start>")
def temperature(start = None):

    session = Session(engine)


    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date > start ).all()

    session.close()

    reslutlist = list (np.ravel(results))

    return jsonify(reslutlist)

@app.route("/api/v1.0/temperature_range/<start>/<end>")
def temperature_range(start = None, end = None):

    session = Session(engine)


    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date <= end).all()

    session.close()

    reslutlist = list (np.ravel(results))

    return jsonify(reslutlist)



if __name__ == '__main__':
    app.run(debug=True)