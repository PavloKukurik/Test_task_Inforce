# ETL Pipeline for User Data

This repository contains a simple ETL pipeline that extracts data from a CSV file, transforms it, and loads it into a PostgreSQL database. The project is containerized using Docker, allowing for easy setup and execution.


## Setup and Running the Project


### 1. Build the Docker Containers

First, need to build the Docker containers. Open a terminal in the project directory and run the following command:

```bash
docker-compose up --build
```

This command will:

- Build the Python application container.
- Build the PostgreSQL container.
- Start both containers and execute the ETL process automatically.
### 2. Verify the ETL Process

Once the containers are up and running, the ETL process will start automatically. Here is option to check the logs of the containers to verify the process:

```bash
docker-compose logs -f
```

### 3.  Stopping the Containers
When task done, stop the containers by running:

```bash
docker-compose down
```
This will stop and remove the containers, but the data will persist in the postgres_data volume.


### 4. Database Schema
The PostgreSQL database contains a table named user_data with the following schema:
```sql
CREATE TABLE user_data (
    user_id INT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    signup_date DATE,
    domain VARCHAR(255)
);

```

Explanation:
- `user_id:` A unique identifier for each user.
- `name:` The user's full name.
- `email:` The user's email address.
- `signup_date:` The date when the user signed up, in YYYY-MM-DD format.
- `domain:` The email domain extracted from the user's email address (e.g., example.com for user@example.com).

### 6. SQL Queries
The following SQL queries are included in the `queries` directory in separated files:


- 1. Retrieve the count of users who signed up on each day:
```sql
SELECT signup_date, COUNT(*) 
FROM user_data
GROUP BY signup_date
ORDER BY signup_date;
```

- 2. List all unique email domains present in the database:
```sql
SELECT DISTINCT domain
FROM user_data;
```

- 3. Retrieve the details of users whose signup_date is within the last 7 days:
```sql
SELECT *
FROM user_data
WHERE signup_date >= CURRENT_DATE - INTERVAL '7 days';
```

- 4. Find the user(s) with the most common email domain:
```sql
SELECT domain, COUNT(*) 
FROM user_data
GROUP BY domain
ORDER BY COUNT(*) DESC
LIMIT 1;
```

- 5. Delete records where the email domain is not from a specific list:
```sql
DELETE FROM user_data
WHERE domain NOT IN ('gmail.com', 'yahoo.com', 'example.com');
```

### 5. Assumptions
The CSV file (`data/generated_data.csv`) contains the following columns: `user_id`, `name`, `email`, and `signup_date` (timestamp format).
Only valid email addresses are retained in the database. Invalid emails are filtered out during the transformation process.
The `signup_date` is converted to the YYYY-MM-DD format.
A new column, `domain`, is added to the dataset, which contains the domain part of the email address.

### 6. Generation data
The procees of generation data is described in `Test_task.ipynb`

