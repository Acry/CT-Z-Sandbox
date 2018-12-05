#!/usr/bin/env python2
'''Tree View/List Store 0
A TreeView widget is the user interface object that displays the data stored in an object that implements the TreeModel interface.

The ListStore provides tabular data storage organized in rows and columns similar to a table in a relational database.

A TreeView display is composed using the following general operations not necessarily in this order:

A tree model object is created usually a ListStore or TreeStore with one or more columns of a specified data type.
The tree model may be populated with one or more rows of data.
A TreeView widget is created and associated with the tree model.
One or more TreeViewColumns are created and inserted in the TreeView. Each of these will present a single display column.
For each TreeViewColumn one or more CellRenderers are created and added to the TreeViewColumn.
The attributes of each CellRenderer are set to indicate from which column of the tree model to retrieve the attribute data. for example the text to be rendered. This allows the CellRenderer to render each column in a row differently.
The TreeView is inserted and displayed in a Window or ScrolledWindow.
The data in the tree model is manipulated programmatically in response to user actions. The TreeView will automatically track the changes.
'''

import pygtk
pygtk.require('2.0')
import gobject
import gtk
import os

DEMODIR = os.path.dirname(__file__)
IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
TEXTFILE = os.path.join(DEMODIR, 'persons.txt')

# read array line by line
array = []
with open(TEXTFILE, "r") as ins:
    for line in ins:
        line = line.rstrip('\n')
        array.append(line)

(
    COLUMN_FIRST,
    COLUMN_LAST
) = range(2)


class ListStore0Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_border_width(8)
        self.set_default_size(300, 250)
        self.set_icon_from_file(ICON_IMAGE)
        vbox = gtk.VBox(False, 8)
        self.add(vbox)

        label = gtk.Label('List of persons')
        vbox.pack_start(label, False, False)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw)

        # create tree model
        model = self.__create_model()

        # create tree view
        treeview = gtk.TreeView(model)
        treeview.set_rules_hint(True)
        # treeview.set_search_column(COLUMN_LAST)
        sw.add(treeview)

        # add columns to the tree view
        self.__add_columns(treeview)
        self.show_all()

    def __create_model(self):
        lstore = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
        for person in array:
            iter = lstore.append()
            person = person.split()
            lstore.set(iter,
                COLUMN_FIRST, person[COLUMN_FIRST],
                COLUMN_LAST, person[COLUMN_LAST])
        return lstore

    def __add_columns(self, treeview):
        model = treeview.get_model()

        # columns for last name
        column = gtk.TreeViewColumn('Last name', gtk.CellRendererText(),
                                    text=COLUMN_LAST)
        column.set_sort_column_id(COLUMN_LAST)
        treeview.append_column(column)

        # column for first name
        column = gtk.TreeViewColumn('First name', gtk.CellRendererText(),
                                     text=COLUMN_FIRST)
        column.set_sort_column_id(COLUMN_FIRST)
        treeview.append_column(column)


if __name__ == '__main__':
    ListStore0Demo()
    gtk.main()
