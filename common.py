# Copyright (c) 2008, 2009, Simon Morgan <sjm@spamcop.net>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import sqlite3
import sys
import time

import config

import markdown2

# Database interactions.

def connect():
    try:
        conn = sqlite3.connect(config.DBPATH)
        conn.execute("CREATE TABLE IF NOT EXISTS entries (id INTEGER \
                PRIMARY KEY, date INTEGER, title TEXT, text TEXT)")
    except sqlite3.OperationalError:
        print_error("Failed to connect to database. Check file and \
                directory permissions.")
        sys.exit(1)
    return conn

def addpost(conn, title, body):
    curtime = int(time.time())
    # Convert hours to seconds.
    curtime = curtime + (config.TOFFSET * 60 * 60)
    conn.execute("INSERT INTO entries VALUES (NULL, ?, ?, ?)",
            (curtime, title, body))

def getnumposts(conn, postid=None):
    """Enumerate the number of posts in the database.

    If an ID is specified then enumerate the number of posts with that
    ID. The result of the latter should be 0 or 1 as essentially this is
    a check for whether the specified post exists.
    """
    if postid:
        numposts = conn.execute("SELECT count(id) FROM entries WHERE id = ?",
                (postid,)).fetchone()
    else:
        numposts = conn.execute("SELECT count(id) FROM entries").fetchone()
    return int(numposts[0])

def getposts(conn, offset=0, numposts=0):
    """Return a list of numposts posts beginning at offset.

    SQLite doesn't seem to support the use of OFFSET without LIMIT so
    whenever numposts is ommited, we return every post.
    """
    posts = []
    if numposts == 0:
        for row in conn.execute("SELECT * FROM entries ORDER BY date DESC"):
            posts.append(row)
    else:
        for row in conn.execute("SELECT * FROM entries ORDER BY date DESC LIMIT ? OFFSET ?",
                (numposts, offset)):
            posts.append(row)
    return posts

def getpost(conn, postid):
    row = conn.execute("SELECT * FROM entries WHERE id = ?",
            (postid,)).fetchone()
    # No need to return the ID as it's one of the parameters.
    return row[1:]

def updatepost(conn, postid, title, body):
    conn.execute("UPDATE entries SET title = ?, text = ? WHERE id = ?",
            (title, body, postid))

def deletepost(conn, postid):
    conn.execute("DELETE FROM entries WHERE id = ?", (postid,))

# Output formatting.

def print_headers(title):
    print '<head>'
    print '<title>' + title + '</title>'
    print '<link href="default.css" rel="stylesheet" type="text/css">'
    print '</head>'

def print_class(msg, class_):
    print '<div class="%s">%s</div>' % (class_, msg)

def print_id(msg, id_):
    print '<div id="%s">%s</div>' % (id_, msg)

def print_error(msg):
    print_class(msg, "error")

def print_msg(msg):
    print_class(msg, "message")

def print_post(title, body, date=None):
    """Formats and prints a post"""
    print '<div class="blogpost">'
    print '<h1>%s</h1>' % title
    if date:
        print '<h3>%s</h3>' % time.ctime(date)
    print markdown2.markdown(body)
    print '</div>'

def header():
    print_id(config.HEADER, "header")

def footer():
    print_id(config.FOOTER, "footer")
