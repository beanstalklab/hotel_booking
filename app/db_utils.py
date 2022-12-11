import pymysql

from app.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
def connect_db():
    conn = pymysql.connect(
        db=DB_NAME,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def get_cursor(conn):
    conn.begin()
    cur = conn.cursor()
    return cur

def close_db(conn):
    conn.close()