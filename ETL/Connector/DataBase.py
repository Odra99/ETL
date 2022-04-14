import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="projectIA",
    user="postgres",
    password="Odra20$"
)

cur = conn.cursor()
