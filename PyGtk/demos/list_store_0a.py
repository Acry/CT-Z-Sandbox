#!/usr/bin/env python2
'''Tree View/List Store 0a
Oh no, I messed it up.
I have a list of persons and didn't get the gender right.
Double click to switch gender.
'''

import pygtk
pygtk.require('2.0')
import gobject
import gtk
import os
import random

DEMODIR = os.path.dirname(__file__)
IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
MALE = os.path.join(IMAGEDIR, 'male.svg')
FEMALE = os.path.join(IMAGEDIR, 'female.svg')
male = gtk.gdk.pixbuf_new_from_file(MALE)
female = gtk.gdk.pixbuf_new_from_file(FEMALE)
TEXTFILE = os.path.join(DEMODIR, 'persons.txt')

# read array line by line
array = []
with open(TEXTFILE, "r") as ins:
    for line in ins:
        line = line.rstrip('\n')
        array.append(line)


class ListStore0aDemo(gtk.Window):
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
        sw.add(treeview)
        treeview.connect("button-press-event", self.on_tv_click)

        # add columns to the tree view
        self.__add_columns(treeview)
        self.show_all()


    def __create_model(self):
        lstore = gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_BOOLEAN)
        i = 1
        for person in array:
            iter = lstore.append()
            person = person.split()
            lstore.set(iter,
                0, i,
                1, person[0],
                2, person[1],
                3, bool(random.getrandbits(1)))  # giving random gender
            i = i + 1
        return lstore

    def __add_columns(self, treeview):
        model = treeview.get_model()

        # column number
        column = gtk.TreeViewColumn('#', gtk.CellRendererText(),
                                    text=0)
        column.set_sort_column_id(0)
        treeview.append_column(column)

        # column last name
        column = gtk.TreeViewColumn('Last name', gtk.CellRendererText(),
                                    text=2)
        column.set_sort_column_id(1)
        treeview.append_column(column)

        # column first name
        column = gtk.TreeViewColumn('First name', gtk.CellRendererText(),
                                     text=1)
        column.set_sort_column_id(2)
        treeview.append_column(column)

        # column avatar
        cell = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn('Avatar', cell)
        column.set_cell_data_func(cell, self.set_pixbuf)
        treeview.append_column(column)

    def set_pixbuf(self, column, cell, model, iter):
        gender = model.get_value(iter, 3)
        if gender:
            cell.set_property('pixbuf', male)
        else:
            cell.set_property('pixbuf', female)

    def on_tv_click(self, treeview, event):
        """flip gender on row double click"""
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            coords = event.get_coords()
            path = treeview.get_path_at_pos(int(coords[0]), int(coords[1]))
            model = treeview.get_model()
            iter = model.get_iter(path[0])
            gender = model.get_value(iter, 3)
            gender = not gender
            model.set_value(iter, 3, gender)


if __name__ == '__main__':
    ListStore0aDemo()
    gtk.main()
