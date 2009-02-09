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
import sqlite3

import common
import config

form = cgi.FieldStorage()

print "Content-type: text/html; charset=UTF-8\n"

print '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
print '<html>'

common.print_headers(config.TITLE)

common.header()

conn = common.connect()

numposts = common.getnumposts(conn)
if numposts == 0:
    common.print_msg('Nothing here yet. How about you <a href="post.cgi">post</a> something interesting?')
else:
    if form.has_key("id"):
        if common.getnumposts(conn, form.getvalue("id")) > 0:
            (title, text, date) = conn.execute("SELECT title, text, date FROM entries WHERE id = ?", (form.getvalue("id"),)).fetchone()
            common.print_post(title, text, date)
        else:
            common.print_msg("No such post.")
    else:
        offset = 0
        if form.has_key("offset"):
            offset = int(form.getvalue("offset"))
        for (postid, title, text, date) in conn.execute("SELECT id, title, text, date FROM entries ORDER BY date DESC LIMIT ? OFFSET ?", (config.NUMPOSTS, offset)):
            title = '<a href="index.cgi?id=%s">%s</a>' % (postid, title)
            common.print_post(title, text, date)

        # Only print the navigation bar if the number of posts exceeds
        # the number to be displayed per page.
        if numposts > config.NUMPOSTS:
            print '<div id="navigation">'
            if offset > 0:
                newoffset = offset - config.NUMPOSTS
                if newoffset < 0:
                    newoffset = 0
                print '<a href="index.cgi?offset=%s">Prev</a>' % newoffset
            if offset + config.NUMPOSTS < numposts:
                newoffset = offset + config.NUMPOSTS
                print '<a href="index.cgi?offset=%s">Next</a>' % newoffset
            print '</div>'

common.footer()

print '</html>'

conn.close()
