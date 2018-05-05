import sqlite3
from sqlite3 import Error


def create_connection():
    print("abdcdffvfd")
    try:
        conn = sqlite3.connect("DiemDanhDatabse.db")
        return conn
    except Error as e:
        print(e)

    return None



