import sqlite3
import sys

DBFILENAME = "bloggy.db"

def connect():
    try:
        conn = sqlite3.connect(DBFILENAME)
        conn.execute("CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, date , title TEXT, text TEXT)")
    except sqlite3.OperationalError:
        print 'Failed to connect to database. Check file and directory permissions.'
        sys.exit(1)
    return conn

def getnumposts(conn, id=None):
    if id:
        numposts = conn.execute("SELECT count(id) FROM entries WHERE id = ?", (id,)).fetchone()
    else:
        numposts = conn.execute("SELECT count(id) FROM entries").fetchone()
    return int(numposts[0])
