import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
from datetime import datetime as dt,timedelta
#------------------------------------------------
# Database Setup
#------------------------------------------------
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
measurements = Base.classes.measurement
station = Base.classes.station
session = Session(engine)
#------------------------------------------------
# Flask Setup
#------------------------------------------------
app = Flask(__name__)
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>/>"
        
    )
#Convert the query results to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precipitation():
    Recent_date = session.query(measurements.date).order_by(measurements.date.desc()).first()
    Recent_date [0]
    Previous_date = dt.strptime(Recent_date[0], "%Y-%m-%d")
    Previous_date = Previous_date-timedelta(days=365)
    Lastyr_date = Previous_date.strftime("%Y-%m-%d")
    Lastyr_date
# Perform a query to retrieve the date and precipitation scores
    Prec_date = session.query (measurements.date, measurements.prcp).filter(measurements.date >=Lastyr_date).all()
    #Prec_date
    Data_date ={}
    for date,prcp in Prec_date:
        Data_date [date]=prcp
    return jsonify(Data_date)
#Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    Calculate_count=session.query(station.station)
    Station_name =[]
    for st in Calculate_count:
        Station_name.append(st.station)
    return jsonify(Station_name) 

#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    Recent_date = session.query(measurements.date).order_by(measurements.date.desc()).first()
    Recent_date [0]
    Previous_date = dt.strptime(Recent_date[0], "%Y-%m-%d")
    Previous_date = Previous_date-timedelta(days=365)
    Lastyr_date = Previous_date.strftime("%Y-%m-%d")
    Lastyr_date
    Meas_state=session.query(measurements.station,func.count(measurements.station)).group_by(measurements.station).order_by(func.count(measurements.station).desc())
    Last_12 = session.query(measurements.tobs, measurements.date).filter(measurements.date > Lastyr_date).filter(measurements.station==Meas_state[0][0]).all()
    Emp_data = []
    for tob in Last_12:
        Emp_data.append (tob)
    return jsonify(Emp_data) 

if __name__ == '__main__':
    app.run(debug=True)
