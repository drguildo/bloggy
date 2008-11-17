#!/usr/bin/env python

import cgi
#import cgitb; cgitb.enable()
import sqlite3
import time

import common
import config

def displaypost(date, title, body):
    """Formats and prints a post"""
    print '<h1>%s</h1>' % title
    print '<h3>%s</h1>' % date
    print '<p>%s</p>' % body

starttime = time.time()

form = cgi.FieldStorage()

print "Content-type: text/html; charset=UTF-8\n"

conn = common.connect()

numposts = common.getnumposts(conn)
if numposts == 0:
    print '<p>Nothing here yet. How about you <a href="post.cgi">post</a> something interesting?</p>'
else:
    if form.has_key("id"):
        if common.getnumposts(conn, form.getvalue("id")) > 0:
            (date, title, text) = conn.execute("SELECT date, title, text FROM entries WHERE id = ?", (form.getvalue("id"),)).fetchone()
            displaypost(date, title, text)
        else:
            print "<p>No such post.</p>"
    else:
        offset = 0
        if form.has_key("offset"):
            offset = int(form.getvalue("offset"))
        for row in conn.execute("SELECT * FROM entries ORDER BY date DESC LIMIT ? OFFSET ?", (config.NUMPOSTS, offset)):
            displaypost(row[1], '<a href="index.cgi?id=%s">%s</a>' % (row[0], row[2]), row[3])
        print '<p align="center">'
        if offset > 0:
            newoffset = offset - config.NUMPOSTS
            if newoffset < 0:
                newoffset = 0
            print '<a href="index.cgi?offset=%s">Prev</a>' % newoffset
        if offset + config.NUMPOSTS < numposts:
            newoffset = offset + config.NUMPOSTS
            print '<a href="index.cgi?offset=%s">Next</a>' % newoffset
        print '</p>'

print '<hr />'
print '<p>Page generated in %s seconds.</p>' % (time.time() - starttime)

conn.close()
