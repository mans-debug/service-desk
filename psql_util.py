import psycopg2 as pg
import psycopg2.pool as pgpool

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

pool = pgpool.ThreadedConnectionPool(
    2,
    10,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)


def execute_PG_query(query):
    conn = pool.getconn()
    cursor = conn.cursor()
    cursor.execute(query)
    result_set = cursor.fetchall()
    cursor.close()
    pool.putconn(conn)
    return result_set
