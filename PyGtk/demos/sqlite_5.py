# !/usr/bin/python2
# -*- coding: utf-8 -*-

'''SQLite/S5
Entity Relationships
Now it is getting more complex and more interesting.

Types of Relationships
a. One-One Relationship (1-1 Relationship)
b. One-Many Relationship (1-M Relationship)
c. Many-Many Relationship (M-M Relationship)

One-to-One (1-1) relationship is defined as the relationship between two tables,
where both the tables should be associated with each other based on only one matching row.
This relationship can be created using Primary key - Unique foreign key constraints.

-Say you can have only one president of the club.


The One-to-Many (1-M Relationship) relationship is defined as a relationship between two tables where a row from one table can have multiple matching rows in another table.
This relationship can be created using Primary key - Foreign key relationship.

-That is what was done in S4 (with or without knowing it). The member of the year could have been 3 times the same person.

Now a Many-Many Relationship (M-M Relationship) will be implemented.
In some cases, you may need multiple instances on both sides of the relationship.

There are services to be done in the Club.
-Clean up the Club-House
-Make the garden around the Club-House
-Decorate the Club-House

On the one hand we have the entity person and on the other hand we have the entity service.

Now we wanna do bookkeep which person did which service.

You will often encounter situations where the junction of two entitities is a new entity.

So many people do many services, hence Many-Many Relationship.

Done Services is the new entity.

An associative (or junction) table maps two or more tables together by referencing the primary keys of each data table.
In effect, it contains a number of foreign keys, each in a many-to-one relationship from the junction table to the individual data tables.

For these relationships, we need to create an extra table:
Done Services will be our junction table.

If you really care about DB-Design, read the Epilog in the source.
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

#region DB
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

cur.execute('CREATE TABLE services (id INTEGER PRIMARY KEY, name text NOT NULL)')

services = ["clean", "garden", "decorate"]
i=1
for service in services:
    # print service
    cur.execute('INSERT INTO services (id, name) VALUES (?,?)', (i, service))
    i = i+1

#Done Services
cur.execute('CREATE TABLE done_services (person_id INTEGER NOT NULL, service_id INTEGER NOT NULL, FOREIGN KEY('
            'person_id) REFERENCES people(id), FOREIGN KEY(service_id) REFERENCES services(id), primary key ('
            'person_id, service_id) )')

(
    COLUMN_YEAR,
    COLUMN_NAME,
) = range(2)

#    if con:
#        con.close()
# -> onquit
#endregion


class S5Demo(gtk.Window):
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
    S5Demo()
    gtk.main()

'''Epilog
I covered:
One-One Relationship (1-1 Relationship)
One-Many Relationship (1-M Relationship)
Many-Many Relationship (M-M Relationship)

Building the users-interface takes quite some time.
Drag and drop will be involved.
Show up tables services and done services. In a real environment one may need a time for the done service also.

The methods to create the columns for the View and the Model must be refactored to accept arbitrary arguments.
At this point we got so much code to respond on thousands use-cases.

I could implement a Database Design tool that helps with an Entity Relationship Diagram (ERD) and common usual stuff.
Rapid prototype implementation would cost a week or two but it isn't worth to do that in PyGTK.
Better go with an hybrid framework if getting serious.
'''