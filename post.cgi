#!/usr/bin/env python

import cgi
#import cgitb; cgitb.enable()
import sqlite3

import common

title = "Please enter a title."
text = "Type something interesting."

form = cgi.FieldStorage()

print 'Content-type: text/html; charset=UTF-8\n'

conn = common.connect()

if form.has_key("delete"):
    for postid in form.getlist("delete"):
        conn.execute("DELETE FROM entries WHERE id = ?", (postid,))
elif form.has_key("edit"):
    (title, text) = conn.execute("SELECT title, text FROM entries WHERE id = ?", (form.getvalue("edit"),)).fetchone()
elif form.has_key("title") and form.has_key("text"):
    if form.has_key("update"):
        conn.execute("UPDATE entries SET title = ?, text = ? WHERE id = ?", (form.getvalue("title"), form.getvalue("text"), form.getvalue("update")))
    else:
        conn.execute("INSERT INTO entries VALUES (NULL, current_timestamp, ?, ?)", (form.getvalue("title"), form.getvalue("text")))

print '<form action="post.cgi" method="post">'

if common.getnumposts(conn) == 0:
    print '<p>Nothing here yet.</p>'
else:
    print '<table border="1">'
    print '<tr><th>ID</th><th>Date</th><th>Title</th><th>Delete</th><th>Update</th></tr>'
    for row in conn.execute("SELECT id, date, title FROM entries ORDER BY date DESC"):
        print '<tr>'
        print '<td>%s</td>' % row[0]
        print '<td>%s</td>' % row[1]
        print '<td>%s</td>' % ('<a href="index.cgi?id=' + str(row[0]) + '">' + row[2] + '</a>')
        print '<td><input type="checkbox" name="delete" value="%s"></td>' % row[0]
        print '<td><input type="radio" name="edit" value="%s"></td>' % row[0]
        print '</tr>'
    print '</table>'

if form.has_key("edit"):
    print '<p><b>Editing post %s.</b></p>' % form.getvalue("edit")
    print '<input type="hidden" name="update" value="%s">' % form.getvalue("edit")

print '<p><input name="title" type="text" value="%s"></p>' % cgi.escape(title, True)
print '<textarea name="text" id="text">%s</textarea>' % cgi.escape(text, True)

print '<p><button type="submit" name="submit">Submit</button></p>'

print '</form>'

conn.commit()
conn.close()
