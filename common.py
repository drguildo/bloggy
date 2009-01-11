import sqlite3
import sys

import config

def connect():
    try:
        conn = sqlite3.connect(config.DBPATH)
        conn.execute("CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, date , title TEXT, text TEXT)")
    except sqlite3.OperationalError:
        print 'Failed to connect to database. Check file and directory permissions.'
        sys.exit(1)
    return conn

def getnumposts(conn, id=None):
    """Enumerate the number of posts in the database. if an ID is specified
    then enumerate the number of posts with that ID. The latter should be 0 or
    1 so essentially this is a check for whether the specified post exists.
    """
    if id:
        numposts = conn.execute("SELECT count(id) FROM entries WHERE id = ?", (id,)).fetchone()
    else:
        numposts = conn.execute("SELECT count(id) FROM entries").fetchone()
    return int(numposts[0])

def printheaders(title):
    print '<head>'
    print '<title>' + title + '</title>'
    print '<link href="default.css" rel="stylesheet" type="text/css">'
    print '</head>'
