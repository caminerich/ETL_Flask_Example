# ETL, SQLite3, Flask example
Per "CTVA Data Coding Exercise.txt"
- Weather files available here: https://github.com/corteva/code-challenge-template
- Challenge instructions here: CTVA Data Coding Exercise.txt

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
1. **Amazon RDS (Relational Database Service)**: For a managed relational database. Compatible with MySQL or PostgreSQL database engines.

2. **Amazon DynamoDB**: For NoSQL database, DynamoDB is a key-value and document database.

### 3. Scheduled Data Ingestion
1. **AWS Lambda**: This will run the data ingestion code in a serverless manner.
2. **Amazon CloudWatch Events (EventBridge)**: This schedules the Lambda function. Set up rules to trigger the Lambda function at specified intervals (e.g., every hour, daily).

### 4. Detailed Approach
1. **API Deployment**:
   - Write API logic in a Lambda function.
   - Use API Gateway to create RESTful endpoints that trigger the Lambda function.
   - Configure API Gateway to handle authentication, authorization, and throttling.

2. **Database Deployment**:
   - Set up an RDS instance. Configure security groups, backup policies, and scaling options.
   - OR set up a DynamoDB table for NoSql. 

3. **Scheduled Data Ingestion**:
   - Write data ingestion logic in a Lambda function.
   - Use CloudWatch Events to create a rule that triggers the Lambda function on a schedule (e.g., every hour).
   - Ensure the Lambda function has the necessary permissions to read from the data source and write to the database.

### Example Workflow
1. **API Gateway** receives a request and triggers the **Lambda function**.
2. The **Lambda function** processes the request and interacts with the **RDS** or **DynamoDB** database as needed.
3. **CloudWatch Events** triggers the data ingestion **Lambda function** on a schedule.
4. The data ingestion **Lambda function** reads data from the source, processes it, and writes it to the **RDS** or **DynamoDB** database.
