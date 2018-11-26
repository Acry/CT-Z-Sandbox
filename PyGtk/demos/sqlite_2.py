# !/usr/bin/python2
# -*- coding: utf-8 -*-

'''SQLite/S2
Create Table and view from liststore.

SQL STATEMENTS:
CREATE TABLE
INSERT INTO

sqlite-binding:
fetchall

SQLite automatically creates an implicit column named rowid and automatically assigns an integer value whenever you insert a new row.
'''
import sqlite3
import pygtk

pygtk.require('2.0')
import gtk
import os
import gobject

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
SQLITE_IMAGE = os.path.join(IMAGEDIR, 'SQLite.svg')

con = None
con = sqlite3.connect(':memory:')
cur = con.cursor()
cur.execute('CREATE TABLE people (first_name text NOT NULL, last_name text NOT NULL)')
cur.execute("INSERT INTO people (first_name, last_name) VALUES ('John', 'Doe')")
cur.execute("INSERT INTO people (first_name, last_name) VALUES ('Jane', 'Doe')")
cur.execute("INSERT INTO people (first_name, last_name) VALUES ('Peter', 'Parker')")
cur.execute("SELECT  rowid,  first_name,  last_name FROM  people")
data = cur.fetchall()

(
    COLUMN_ID,
    COLUMN_NAME,
    COLUMN_SURNAME,

) = range(3)

#    if con:
#        con.close()
# -> onquit

class S2Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_default_size(300, 200)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)
        vbox = gtk.VBox(False, 8)
        self.add(vbox)

        label = gtk.Label('List of People')
        vbox.pack_start(label, False, False)
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw)

        model = self.__create_model()
        treeview = gtk.TreeView(model)
        treeview.set_rules_hint(True)
        treeview.set_search_column(COLUMN_NAME)
        sw.add(treeview)
        self.__add_columns(treeview)
        self.show_all()

    def __create_model(self):
        lstore = gtk.ListStore(
            gobject.TYPE_UINT,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING)

        for item in data:
            iter = lstore.append()
            lstore.set(iter,
                       COLUMN_ID, item[COLUMN_ID],
                       COLUMN_NAME, item[COLUMN_NAME],
                       COLUMN_SURNAME, item[COLUMN_SURNAME])
        return lstore

    def __add_columns(self, treeview):

        # column for id
        column = gtk.TreeViewColumn('Id', gtk.CellRendererText(),
                                    text=COLUMN_ID)
        column.set_sort_column_id(COLUMN_ID)
        treeview.append_column(column)

        # column for Name
        column = gtk.TreeViewColumn('Name', gtk.CellRendererText(),
                                    text=COLUMN_NAME)
        column.set_sort_column_id(COLUMN_NAME)
        treeview.append_column(column)

        # columns for surname
        column = gtk.TreeViewColumn('Surname', gtk.CellRendererText(),
                                    text=COLUMN_SURNAME)
        column.set_sort_column_id(COLUMN_SURNAME)
        treeview.append_column(column)

if __name__ == '__main__':
    S2Demo()
    gtk.main()
