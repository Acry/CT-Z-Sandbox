# !/usr/bin/python2
# -*- coding: utf-8 -*-

'''SQLite/S1
Import SQLite and query version.
If you get an error message you probably don't have the sqlite module.

SQL Statement:
SELECT

SQLite binding:
connect
cursor
execute
fetchone
:memory: DB
'''
import sqlite3
import pygtk

pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
SQLITE_IMAGE = os.path.join(IMAGEDIR, 'SQLite.svg')

con = None
try:
    con = sqlite3.connect(':memory:')
    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')
    """
        From the connection, we get the cursor object. The cursor is used to traverse the records from the result set.
        We call the execute() method of the cursor and execute the SQL statement.
        
    """
    data = cur.fetchone()
    data = str(data[0])

except sqlite3.Error, e:
    data = "Error %s:" % e.args[0]


#    if con:
#        con.close()
# -> onquit


class S1Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_default_size(200, 200)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)
        dialog = gtk.MessageDialog(self, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_OK, "You are running SQLite Version %s" % data)
        pixbuf = gtk.gdk.pixbuf_new_from_file(SQLITE_IMAGE)
        width = pixbuf.get_width()/10
        height = pixbuf.get_height()/10

        pixbuf = pixbuf.scale_simple(width, height, gtk.gdk.INTERP_BILINEAR)
        img = gtk.Image()
        img.set_from_pixbuf(pixbuf)
        img.show()
        dialog.set_image(img)
        dialog.run()
        dialog.destroy()


if __name__ == '__main__':
    S1Demo()
    gtk.main()
