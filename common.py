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

import config

import markdown2

def connect():
    try:
        conn = sqlite3.connect(config.DBPATH)
        conn.execute("CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, date , title TEXT, text TEXT)")
    except sqlite3.OperationalError:
        print_error("Failed to connect to database. Check file and \
                directory permissions.")
        sys.exit(1)
    return conn

def getnumposts(conn, postid=None):
    """Enumerate the number of posts in the database. If an ID is
    specified then enumerate the number of posts with that ID. The
    result of the latter should be 0 or 1 as essentially this is a check
    for whether the specified post exists.
    """
    if postid:
        numposts = conn.execute("SELECT count(id) FROM entries WHERE id = ?",
                (postid,)).fetchone()
    else:
        numposts = conn.execute("SELECT count(id) FROM entries").fetchone()
    return int(numposts[0])

def print_headers(title):
    print '<head>'
    print '<title>' + title + '</title>'
    print '<link href="default.css" rel="stylesheet" type="text/css">'
    print '</head>'

def print_class(msg, class_):
    print '<div class="%s">' % class_
    print '<p>%s</p>' % msg
    print '</div>'

def print_error(msg):
    print_class(msg, "error")

def print_msg(msg):
    print_class(msg, "message")

def print_post(title, body, date=None):
    """Formats and prints a post"""
    print '<div class="blogpost">'
    print '<h1>%s</h1>' % title
    if date:
        print '<h3>%s</h3>' % date
    print markdown2.markdown(body)
    print '</div>'
