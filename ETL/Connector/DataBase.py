import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ProjectIA",
    user="postgres",
    password="Odra20$"
)

cur = conn.cursor()
