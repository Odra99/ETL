import psycopg2

from ETL.Connector.ConnectionConf import *

conn = psycopg2.connect(
    host=hostParam,
    database=databaseParam,
    user=userParam,
    password=passwordParam
)

cur = conn.cursor()
