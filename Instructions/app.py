import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement_table = Base.classes.measurement
station_table = Base.classes.station
print(Base.classes.keys())



#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################




@app.route("/")
def welcome():
#"""List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"api/v1.0/start"
        f"/api/v1.0/startend"
    )






@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a list of all measurement dates and prcp values
    precipitation_results = session.query(measurement_table.date, measurement_table.prcp).all()
    
    session.close()

    #create dict from the row data and append to a list of all measurement dates
    precipitation_list = []
    # date_list = []
    for date,prcp in precipitation_results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_list.append(precipitation_dict)
        # date_list.append(date)
  
    # print("Here is the date list, sorted")
    # date_list = date_list.sort
    # print(date_list)

    return jsonify(precipitation_list)


    # session.query(measurement.date).order_by(measurement.date.desc()).first()






@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Return a list of all stations and their info
    station_results = session.query(station_table.station,station_table.name,station_table.latitude,station_table.longitude,station_table.elevation).all()
    
    session.close()

    #create dict from the row data and append to a list of all measurement dates
    station_list = []

    for station,name,latitude,longitude,elevation in station_results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_list.append(station_dict)
        

    return jsonify(station_list)




@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Return a list of all stations and their info
    station_activity = session.query(measurement_table.station, func.count(measurement_table.station)).group_by(measurement_table.station).\
    order_by(func.count(measurement_table.station).desc()).all()
    most_active_station = station_activity[0]  

    #return jsonify(most_active_station)


    # Return a list of all measurement dates and prcp values
    temperature_results = session.query(measurement_table.station,measurement_table.date, measurement_table.tobs).all()
    session.close()

    #create dict from the row data and append to a list of all measurement dates
    temperature_list = []

    #print(temperature_results)

    for row in temperature_results:
        #print("testing")
        #print(station[0])
        #print(most_active_station)
        if row[0] == most_active_station[0]:
    
    
            temperature_dict = {}
            temperature_dict["station"] = row[0]
            temperature_dict["date"] = row[1]
            temperature_dict["tobs"] = row[2]
            temperature_list.append(temperature_dict)
            print(row[0])
        else:
            print("skipping")
    print(temperature_list)
    return jsonify(temperature_list)


@app.route("/api/v1.0/start")
def start():
    
    session = Session(engine)

  # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    start_date = dt.date(2010,4, 23)
    end_date = dt.date(2010,5, 1)

    results = session.query(func.min(measurement_table.tobs), func.avg(measurement_table.tobs), func.max(measurement_table.tobs)).\
        filter(measurement_table.date >= start_date).all()

    session.close()

   
    start_date_tobs_list = []
    for min, avg, max in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs_list.append(start_date_tobs_dict)

    return jsonify(start_date_tobs_list)








@app.route("/api/v1.0/startend")
def startend():
    
    session = Session(engine)

  # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    start_date = dt.date(2010,4, 23)
    end_date = dt.date(2010,5, 1)

    results = session.query(func.min(measurement_table.tobs), func.avg(measurement_table.tobs), func.max(measurement_table.tobs)).\
        filter(measurement_table.date >= start_date).filter(measurement_table.date <= end_date).all()

    session.close()

   
    start_end_date_tobs_list = []
    for min, avg, max in results:
        start_end_date_tobs_dict = {}
        start_end_date_tobs_dict["min_temp"] = min
        start_end_date_tobs_dict["avg_temp"] = avg
        start_end_date_tobs_dict["max_temp"] = max
        start_end_date_tobs_list.append(start_end_date_tobs_dict)

    return jsonify(start_end_date_tobs_list)



if __name__ == '__main__':
    app.run(debug=True)
