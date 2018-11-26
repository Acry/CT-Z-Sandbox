# !/usr/bin/python2
# -*- coding: utf-8 -*-

'''SQLite/S4
Import names from file, create a second table and connect it.

-Foreign key and INNER JOIN-

You can have a lot of details in a row.
First name and last name are just a bare minimum to figure something real.
Lets say the persons are members of a club.
The club elects a member of the year
And we want to flip through year and see who was the member of the year.

Things are getting slightly more complex.
Editing and filtering will be done later.
For now focus on the relationship.

In the context of relational databases, a foreign key is a field (or collection of fields) in one table that uniquely identifies a row of another table or the same table.
In other words, the foreign key is defined in a second table, but it refers to the primary key or a unique key in the first table.

In Sqlite foreign keys need to be enabled.
'PRAGMA foreign_keys = ON'

Now we need to mark a column in people as primary key:
'id INTEGER PRIMARY KEY'

And create a foreign key the second table:
  person INTEGER,
  FOREIGN KEY(person) REFERENCES people(rowid)

Finally we getting the wanted data by using an INNER JOIN:
"SELECT  year,  last_name FROM people INNER JOIN years on years.person = people.id"

depicting the relation:
'''
import sqlite3
import pygtk

pygtk.require('2.0')
import gtk
import os
import gobject

DEMODIR = os.path.dirname(__file__)
IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
SQLITE_IMAGE = os.path.join(IMAGEDIR, 'SQLite.svg')
TEXTFILE = os.path.join(DEMODIR, 'persons.txt')

with open(TEXTFILE, "r") as ins:
    array = []
    for line in ins:
        line = line.rstrip('\n')
        array.append(line)

con = None
con = sqlite3.connect(':memory:')
cur = con.cursor()
cur.execute('PRAGMA foreign_keys = ON')
cur.execute('CREATE TABLE people (id INTEGER PRIMARY KEY, first_name text NOT NULL, last_name text NOT NULL)')


for person in array:
    person = person.split()
    first_name = person[0]
    last_name = person[1]
    cur.execute("INSERT INTO people (first_name, last_name) VALUES (?, ?)", (first_name, last_name))

cur.execute("SELECT  id,  first_name,  last_name FROM  people")
data = cur.fetchall()

(
    COLUMN_ID,
    COLUMN_NAME,
    COLUMN_SURNAME,

) = range(3)

cur.execute('CREATE TABLE years (year INTEGER, person INTEGER, FOREIGN KEY(person) REFERENCES people(id))')

winners = ((2015, 2), (2016, 31), (2017, 14))

for winner in winners:
    cur.execute("INSERT INTO years (year, person) VALUES (?,?)", winner)


cur.execute("SELECT  year,  last_name FROM people INNER JOIN years on years.person = people.id")
years = cur.fetchall()
# print years

(
    COLUMN_YEAR,
    COLUMN_NAME,
) = range(2)
#    if con:
#        con.close()
# -> onquit


class S4Demo(gtk.Window):
    def cb(self):
        gobject.source_remove(self.timer)
        (x, y) = self.get_position()
        (w, h) = self.get_size()
        window1 = gtk.Window()
        window1.set_default_size(200, 200)
        wx = x+w
        # wy = y
        window1.move(wx,y)
        window1.set_title("Member of the year")
        window1.set_icon_from_file(ICON_IMAGE)
        window1.set_transient_for(self)
        model = self.__create_winner_model()
        # print type(model)
        treeview = gtk.TreeView(model)
        # print type(treeview)
        treeview.set_rules_hint(True)
        # treeview.set_search_column(COLUMN_NAME)
        window1.add(treeview)
        treeview.show()
        self.__add_winner_columns(treeview)
        window1.show()

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
        # self.connect("configure-event", self.cb)
        self.show_all()

        self.timer = None
        self.timer = gobject.timeout_add(500, self.cb)


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
        column = gtk.TreeViewColumn('Id', gtk.CellRendererText(),
                                    text=COLUMN_ID)
        column.set_sort_column_id(COLUMN_ID)
        treeview.append_column(column)
        column = gtk.TreeViewColumn('Name', gtk.CellRendererText(),
                                    text=COLUMN_NAME)
        column.set_sort_column_id(COLUMN_NAME)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Surname', gtk.CellRendererText(),
                                    text=COLUMN_SURNAME)
        column.set_sort_column_id(COLUMN_SURNAME)
        treeview.append_column(column)

    def __create_winner_model(self):
        lstore = gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_STRING)
        for year in years:
            iter = lstore.append()
            lstore.set(iter, COLUMN_YEAR, year[0], COLUMN_NAME, year[1])
        return lstore

    def __add_winner_columns(self, treeview):
        column = gtk.TreeViewColumn('Year', gtk.CellRendererText(),
                                    text=COLUMN_YEAR)
        column.set_sort_column_id(COLUMN_YEAR)
        treeview.append_column(column)
        column = gtk.TreeViewColumn('Surname', gtk.CellRendererText(),
                                    text=COLUMN_NAME)
        column.set_sort_column_id(COLUMN_NAME)
        treeview.append_column(column)



if __name__ == '__main__':
    S4Demo()
    gtk.main()
