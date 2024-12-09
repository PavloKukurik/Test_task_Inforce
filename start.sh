#!/bin/bash

# Check if all necessary environment variables are set (database connection details)
if [[ -z "$DB_HOST" || -z "$DB_PORT" || -z "$DB_USER" || -z "$DB_PASSWORD" || -z "$DB_NAME" ]]; then
    echo "Error: Missing required environment variables."
    exit 1
fi

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  sleep 1
done

echo "PostgreSQL is ready, starting ETL process..."

python python_scrypt.py
