# Weather data ETL, SQLite3, Flask challenge
## Challenge:
**Weather Data Description**
The wx_data directory has files containing weather data records from 1985-01-01 to 2014-12-31. Each file corresponds to a particular weather station from Nebraska, Iowa, Illinois, Indiana, or Ohio.
Each line in the file contains 4 records separated by tabs: 
1. The date (YYYYMMDD format)
2. The maximum temperature for that day (in tenths of a degree Celsius)
3. The minimum temperature for that day (in tenths of a degree Celsius)
4. The amount of precipitation for that day (in tenths of a millimeter)
Missing values are indicated by the value -9999.\

**Problem 1 - Data Modeling**
Choose a database to use for this coding exercise (SQLite, Postgres, etc.). Design a data model to represent the weather data records. If you use an ORM, your answer should be in the form of that ORM's data definition format. If you use pure SQL, your answer should be in the form of DDL statements\

**Problem 2 - Ingestion**
Write code to ingest the weather data from the raw text files supplied into your database, using the model you designed. Check for duplicates: if your code is run twice, you should not end up with multiple rows with the same data in your database. Your code should also produce log output indicating start and end times and number of records ingested.

**Problem 3 - Data Analysis**
For every year, for every weather station, calculate:
* Average maximum temperature (in degrees Celsius)
* Average minimum temperature (in degrees Celsius)
* Total accumulated precipitation (in centimeters)
Ignore missing data when calculating these statistics.
Design a new data model to store the results. Use NULL for statistics that cannot be calculated.
Your answer should include the new model definition as well as the code used to calculate the new values and store them in the database.

**Problem 4 - REST API**
Choose a web framework (e.g. Flask, Django REST Framework). Create a REST API with the following GET endpoints:
/api/weather
/api/weather/stats
Both endpoints should return a JSON-formatted response with a representation of the ingested/calculated data in your database. Allow clients to filter the response by date and station ID (where present) using the query string. Data should be paginated.
Include a Swagger/OpenAPI endpoint that provides automatic documentation of your API.
Your answer should include all files necessary to run your API locally, along with any unit tests

**Extra Credit - Deployment**
(Optional.) Assume you are asked to get your code running in the cloud using AWS. What tools and AWS services would you use to deploy the API, database, and a scheduled version of your data ingestion code? Write up a description of your approach.

# Answers
## open_and_parse.py
- This script creates a SQLite table called "weather_data" and ingests TXT weather station files from local machine
- This script also creates a SQLite table called "transaction_log" that records the start, end, and duration time of each record as it is ingested into the 'weather_data' table
- Must change database path and file path to your project requirements
- Create sqlite database first by going to command line: "sqlite3 weather.db"

## stats.py
- This script creates a "stat" table with average max C temp, average min C temp, and total accumulated precip for each year and each weather station.

## web_framework.py
- This script is a flask web framework to publish data to two API endpoints:
    - /api/weather
    - api/weather/stats
- Clients can filter the response by date and station id for weather and year and station id for weather stats. 
- Swagger documentation 

## Additional Documentation
- Weather stations data dates are between 1985-01-01 to 2014-12-31
- Weather station states are the first 7 letters of the filename (ie USC00025) and correspond to Nebraska, Iowa, Illinois, Indiana, or Ohio

## Future Improvements 
- Concurrency to increase speed that raw weather TXT data is ingested in SQLlite database 
- Refactor code so only one python script to run modules together
- Set up linting stage in CI/CD pipeline

## Extra Credit
Assume you are asked to get your code running in the cloud using AWS. What tools and AWS services would you use to deploy the API, database, and a scheduled version of your data ingestion code? Write up a description of your approach.

To deploy the API, database, and a scheduled version of the data ingestion code, I would use the following AWS services and tools:

### 1. API Deployment
1. **AWS Lambda**: For serverless execution of the API logic. This allows the code to be run without provisioning or managing servers.
2. **Amazon API Gateway**: To create, publish, maintain, monitor, and secure the API.

## 2. Database Deployment
1. **Amazon RDS (Relational Database Service)**: For a managed relational database.

### 3. Scheduled Data Ingestion
1. **AWS Lambda**: This will run the data ingestion code in a serverless manner.
2. **Amazon EventBridge**: This schedules the Lambda function. Set up rules to trigger the Lambda function at specified intervals (e.g., every hour, daily).

### 4. Detailed Approach
1. **API Deployment**:
   - Write API logic in a Lambda function.
   - Use API Gateway to create RESTful endpoints that trigger the Lambda function.
   - Configure API Gateway to handle authentication, authorization, and throttling.

2. **Database Deployment**:
   - Set up an RDS instance. Configure security groups, backup policies, and scaling options.

3. **Scheduled Data Ingestion**:
   - Write data ingestion logic in a Lambda function.
   - Use CloudWatch to create a rule that triggers the Lambda function on a schedule (e.g., every hour).
   - Ensure the Lambda function has the necessary permissions to read from the data source and write to the database.

### Example Workflow
1. **API Gateway** receives a request and triggers the **Lambda function**.
2. The **Lambda function** processes the request and interacts with the **RDS** database.
3. **CloudWatch** triggers the data ingestion **Lambda function** on a schedule.
4. The data ingestion **Lambda function** reads data from the source, processes it, and writes it to **RDS**.
