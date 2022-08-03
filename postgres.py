import pandas as pd
from sqlalchemy import create_engine

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'buketaicore.cqiteiyhxq0v.us-east-1.rds.amazonaws.com'
USER = 'postgres'
PASSWORD = 'vbsil9Naiads'
PORT = 5432
DATABASE = 'postgres'
engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")


#Connecting to AWS RDS endpoint through pgAdmin4 (using psycopg2).
def write_to_db(datadict, community_name):
    #Creating tables of my scraper data in my pgAdmin4 dataset (AWS server).
    data = pd.DataFrame(list(datadict.values()), index=list(datadict.keys()))
    data.to_sql(community_name, engine, if_exists='replace')


def read_from_db(table_name):
    return pd.read_sql_table(table_name, engine)