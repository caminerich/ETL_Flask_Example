from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_restful_swagger import swagger
import sqlite3
import os

app = Flask(__name__)
api = swagger.docs(Api(app), apiVersion='1.0', api_spec_url="/api/spec")

# Path to SQLite database file
db_file = r"//Users//carrieminerich//Desktop//codderry//weather.db"

# Function to create a new SQLite connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to query weather data
def query_weather(conn, date=None, station_id=None, limit=10, offset=0):
    sql = """SELECT date, SUBSTR(filename,1,11) as weather_station, max_temp_c, min_temp_c, precip
             FROM weather_data
             WHERE 1=1"""
    params = []

    if date:
        sql += " AND date = ?"
        params.append(date)
    if station_id:
        sql += " AND SUBSTR(filename,1,11) = ?"
        params.append(station_id)

    sql += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    return rows

# Function to query weather stats
def query_stats(conn, year=None, station_id=None, limit=10, offset=0):
    sql = """SELECT year, weather_station, avg_max_temp_c, avg_min_temp_c, total_precip_cm
             FROM weather_stats
             WHERE 1=1"""
    params = []
    if year:
        sql += " AND year = ?"
        params.append(year)
    if station_id:
        sql += " AND weather_station = ?"
        params.append(station_id)
    sql += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cur = conn.cursor()
    cur.execute(sql, params)
    stats_data = cur.fetchall()
    return stats_data

# route
@app.route('/')
def index():
    return "Welcome to the Weather Data API!"

# Resource for weather data
class Weather(Resource):
    @swagger.operation(
        notes='Get weather data',
        parameters=[
            {
                "name": "date",
                "description": "Filter by date",
                "required": False,
                "type": "string",
                "paramType": "query"
            },
            {
                "name": "station_id",
                "description": "Filter by station ID",
                "required": False,
                "type": "string",
                "paramType": "query"
            },
            {
                "name": "limit",
                "description": "Limit the number of results",
                "required": False,
                "type": "integer",
                "paramType": "query"
            },
            {
                "name": "offset",
                "description": "Offset the results",
                "required": False,
                "type": "integer",
                "paramType": "query"
            }
        ]
    )
    def get(self):
        conn = create_connection(db_file)
        date = request.args.get('date')
        station_id = request.args.get('station_id')
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
        rows = query_weather(conn, date, station_id, limit, offset)
        return jsonify(rows)

# Resource for weather stats
class WeatherStats(Resource):
    @swagger.operation(
        notes='Get weather stats',
        parameters=[
            {
                "name": "year",
                "description": "Filter by year",
                "required": False,
                "type": "string",
                "paramType": "query"
            },
            {
                "name": "station_id",
                "description": "Filter by station ID",
                "required": False,
                "type": "string",
                "paramType": "query"
            },
            {
                "name": "limit",
                "description": "Limit the number of results",
                "required": False,
                "type": "integer",
                "paramType": "query"
            },
            {
                "name": "offset",
                "description": "Offset the results",
                "required": False,
                "type": "integer",
                "paramType": "query"
            }
        ]
    )
    def get(self):
        conn = create_connection(db_file)
        year = request.args.get('year')
        station_id = request.args.get('station_id')
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
        stats_data = query_stats(conn, year, station_id, limit, offset)
        return jsonify(stats_data)

# Add resources to API
api.add_resource(Weather, '/api/weather')
api.add_resource(WeatherStats, '/api/weather/stats')

#http://127.0.0.1:5000/api/weather?date=19850101&station_id=USC00257715&limit=10&offset=0
#http://127.0.0.1:5000/api/weather/stats?year=1985&station_id=USC0033&limit=10&offset=0

if __name__ == '__main__':
    app.run(debug=True)
