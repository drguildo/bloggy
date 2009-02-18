#!/usr/bin/env python

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

import cgi
#import cgitb; cgitb.enable()
import time

import common
import config

edit_title = "Please enter a title."
edit_text = "Type something interesting."

conn = common.connect()

form = cgi.FieldStorage()

print 'Content-type: text/html; charset=UTF-8\n'

print '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
print '<html>'

common.print_headers(config.TITLE + " - Post")

if form.has_key("delete"):
    for postid in form.getlist("delete"):
        common.deletepost(conn, postid)
elif form.has_key("preview"):
    edit_title = form.getvalue("title")
    edit_text = form.getvalue("body")
elif form.has_key("edit"):
    (_, edit_title, edit_text) = common.getpost(conn, form.getvalue("edit"))
elif form.has_key("title") and form.has_key("body"):
    if form.has_key("update"):
        common.updatepost(conn, form.getvalue("update"),
                form.getvalue("title"), form.getvalue("body"))
    else:
        common.addpost(conn, form.getvalue("title"), form.getvalue("body"))

print '<form action="post.cgi" method="post">'

if common.getnumposts(conn) == 0:
    common.print_msg("Nothing here yet.")
else:
    print '<table id="postlist">'
    print '<tr><th>ID</th><th>Date</th><th>Title</th><th>Delete</th></tr>'
    for (postid, date, title, _) in common.getposts(conn):
        print '<tr>'
        print '<td>%s</td>' % postid
        print '<td>%s</td>' % time.strftime("%y/%m/%d %H:%M:%S", time.gmtime(date))
        print '<td>%s</td>' % ('<a href="index.cgi?id=' + str(postid) + '">' + title + '</a>')
        print '<td><input type="checkbox" name="delete" value="%s"></td>' % postid
        print '<td><a href="post.cgi?edit=%s">Edit</a></td>' % postid
        print '</tr>'
    print '</table>'

if form.has_key("edit"):
    print '<p><b>Editing post %s.</b></p>' % form.getvalue("edit")
    print '<input type="hidden" name="update" value="%s">' % form.getvalue("edit")

if form.has_key("preview"):
    # Perpetuate the update key so that when the post is submitted it
    # correctly replaces an existing post rather than inserting a new
    # one.
    if form.has_key("update"):
        print '<input type="hidden" name="update" value="%s">' % form.getvalue("update")
    common.print_post(edit_title, edit_text)

print '<div id="editing">'
print '<input name="title" id="posttitle" type="text" value="%s">' % cgi.escape(edit_title, True)
print '<textarea name="body" id="postbody">%s</textarea>' % cgi.escape(edit_text, True)

print '<p>'
print '<input type="submit" name="preview" value="Preview" class="button">'
print '<input type="submit" name="submit" value="Submit" class="button">'
print '</p>'
print '</div>'

print '</form>'

print '</html>'

conn.commit()
conn.close()
