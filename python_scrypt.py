import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('data/generated_data.csv')

db_connection_str = 'postgresql://postgres:Pavlo0509@db:5432/user_data'
engine = create_engine(db_connection_str)

df.to_sql('user_data', engine, if_exists='replace', index=False)

print('Done')
