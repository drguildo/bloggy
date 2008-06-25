#!/usr/bin/env python

import cgi
#import cgitb; cgitb.enable()
import sqlite3
import time

import common

def displaypost(date, title, body):
    """Formats and prints a post"""
    print '<h1>%s</h1>' % title
    print '<h3>%s</h1>' % date
    print '<p>%s</p>' % body

starttime = time.time()

form = cgi.FieldStorage()

print "Content-type: text/html; charset=UTF-8\n"

conn = common.connect()

if common.getnumposts(conn) == 0:
    print '<p>Nothing here yet. How about you <a href="post.cgi">post</a> something interesting?</p>'
else:
    if form.has_key("id"):
        if common.getnumposts(conn, form.getvalue("id")) > 0:
            (date, title, text) = conn.execute("SELECT date, title, text FROM entries WHERE id = ?", (form.getvalue("id"),)).fetchone()
            displaypost(date, title, text)
        else:
            print "<p>No such post.</p>"
    else:
        for row in conn.execute("SELECT * FROM entries ORDER BY date DESC"):
            displaypost(row[1], '<a href="index.cgi?id=%s">%s</a>' % (row[0], row[2]), row[3])

print '<hr />'
print '<p>Page generated in %s seconds.</p>' % (time.time() - starttime)

conn.close()
