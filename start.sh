#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  sleep 1
done

echo "PostgreSQL is ready. Starting ETL process..."
python python_scrypt.py
