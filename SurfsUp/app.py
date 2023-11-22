# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from datetime import datetime, timedelta

#################################################
# Database Setup
#################################################

# Create an engine to your database
# Adjust the path according to your file system
engine = create_engine("sqlite:///C:/Users/UT4Me/Documents/GitHub/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# Reflect the tables
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
def home():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # Query to retrieve the last 12 months of precipitation data
    # Adjust the query based on your data analysis
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Convert to dictionary
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    # Convert to list
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    # Query the most active station and its last year of data
    # Adjust the query based on your data analysis
    results = session.query(Measurement.date, Measurement.tobs).all()
    session.close()

    # Convert to list
    tobs_list = {date: tobs for date, tobs in results}
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    # Query TMIN, TAVG, TMAX for all dates greater than and equal to the start date
    # Adjust the query based on your data analysis
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).all()
    session.close()

    # Convert to list
    temps = list(np.ravel(results))
    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    # Query TMIN, TAVG, TMAX between start and end date
    # Adjust the query based on your data analysis
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).all()
    session.close()

    # Convert to list
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)
