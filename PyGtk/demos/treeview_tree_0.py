#!/usr/bin/env python2
'''Tree View/Model Tree 0

Basic Treeview connected to TreeStore.

The TreeView widget displays lists and trees displaying multiple columns.
It replaces the previous set of List, CList, Tree and CTree widgets with a much more powerful and flexible set of
objects that use the Model-View-Controller (MVC) principle to provide the following features:

two pre-defined models:
one for lists and one for trees

multiple views of the same model are automatically updated when the model changes
selective display of the model data
use of model data to customize the TreeView display on a row-by-row basis
pre-defined data rendering objects for displaying text, images and boolean data
stackable models for providing sorted and filtered views of the underlying model data
reorderable and resizeable columns
automatic sort by clicking column headers
drag and drop support

support for custom models (generic models) entirely written in Python
support for custom cell renderers entirely written in Python
'''

import pygtk
pygtk.require('2.0')
import gtk

class ModelTree0Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_default_size(200, 200)
        self.set_border_width(8)

        # create a TreeStore with one string column to use as the model
        treestore = gtk.TreeStore(str)

        # we'll add some data now - 4 rows with 3 child rows each
        for parent in range(4):
            piter = treestore.append(None, ['parent %i' % parent])
            for child in range(3):
                treestore.append(piter, ['child %i of parent %i' %
                                              (child, parent)])

        # create the TreeView using treestore
        treeview = gtk.TreeView(treestore)

        # create the TreeViewColumn to display the data
        tvcolumn = gtk.TreeViewColumn('Column 0')

        # add tvcolumn to treeview
        treeview.append_column(tvcolumn)

        # create a CellRendererText to render the data
        cell = gtk.CellRendererText()

        # add the cell to the tvcolumn and allow it to expand
        tvcolumn.pack_start(cell, True)

        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        tvcolumn.add_attribute(cell, 'text', 0)

        # make it searchable
        treeview.set_search_column(0)

        # Allow sorting on the column
        tvcolumn.set_sort_column_id(0)

        # Allow drag and drop reordering of rows
        treeview.set_reorderable(True)

        self.add(treeview)
        self.show_all()


if __name__ == '__main__':
    ModelTree0Demo()
    gtk.main()
