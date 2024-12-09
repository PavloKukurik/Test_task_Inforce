# Import libs
import re
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


class ETL:
    """
    Implementation of the ETL pipeline
    """
    def __init__(self, csv_path: str, db_connection: str):
        """
        Initialize the ETL
        :param csv_path: path to csv file with generated data
        :param db_connection: Information about the database connection
        """
        self.csv_path = csv_path
        self.db_connection_str = db_connection
        self.engine = create_engine(self.db_connection_str)

    def extract(self) -> pd.DataFrame:
        """
        Extract data from CSV
        """
        try:
            return pd.read_csv(self.csv_path)
        except Exception as e:
            print(f"Error reading CSV: {e}")
            raise

    @staticmethod
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform data: convert date, filter emails, add domain
        :param df:  name of dataset (pd.DataFrame)
        :return: transformed dataset
        """
        df['signup_date'] = pd.to_datetime(df['signup_date']).dt.date

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        df = df[df['email'].apply(lambda x: re.match(email_regex, x) is not None)]

        df['domain'] = df['email'].apply(lambda x: x.split('@')[-1])

        return df

    def load(self, df: pd.DataFrame, table_name: str) -> None:
        """
        Load data to PostgreSQL
        :param df: name of dataset (pd.DataFrame)
        :param table_name: name of PostgreSQL table
        :return: Nothing
        """
        try:
            # Using 'append' to avoid recreating the table every time
            df.to_sql(table_name, self.engine, if_exists='append', index=False)
        except Exception as e:
            print(f"Error loading data to PostgreSQL: {e}")
            raise

    def execute_sql_from_file(self, file_path: str):
        """
        Execute SQL queries from a file
        :param file_path: Path to the SQL file
        :return: Nothing
        """
        try:
            with open(file_path, 'r') as f:
                sql_query = f.read()
            with self.engine.connect() as connection:
                connection.execute(text(sql_query))
            print(f"SQL query from {file_path} executed successfully.")
        except Exception as e:
            print(f"Error executing SQL from {file_path}: {e}")
            raise

    def run(self, table_name: str) -> None:
        """
        Run the full ETL process
        :param table_name: name of PostgreSQL table
        :return: Nothing
        """
        df = self.extract()
        df = self.transform(df)
        self.load(df, table_name)

        queries_dir = "queries"
        sql_files = [
            "first.sql",
            "second.sql",
            "third.sql",
            "fourh.sql"
        ]

        for sql_file in sql_files:
            file_path = os.path.join(queries_dir, sql_file)
            self.execute_sql_from_file(file_path)

        print("ETL process completed successfully and SQL queries executed.")


# Params initialisation
load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

db_connection_str = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

etl = ETL(csv_path="data/generated_data.csv", db_connection=db_connection_str)
etl.run(table_name="user_data")
