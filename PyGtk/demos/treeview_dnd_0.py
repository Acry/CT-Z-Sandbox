#!/usr/bin/env python2
'''Tree View/Drag and Drop

This example (treeviewdnd.py) is a list that URLs can be dragged from and dropped on.
Also the URLs in the list can be reordered by dragging and dropping within the TreeView.
A couple of buttons are provided to clear the list and to clear a selected item.
'''
# pygtk version: John Finlay

import pygtk
pygtk.require('2.0')
import gtk

class DragAndDropDemo(gtk.Window):

    TARGETS = [
        ('MY_TREE_MODEL_ROW', gtk.TARGET_SAME_WIDGET, 0),
        ('text/plain', 0, 1),
        ('TEXT', 0, 2),
        ('STRING', 0, 3),
        ]

    def clear_selected(self, button, treeview):
        selection = treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            model.remove(iter)
        return

    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_border_width(5)
        self.set_size_request(400, 200)
        self.set_title("URL Cache")

        scrolledwindow = gtk.ScrolledWindow()
        vbox = gtk.VBox()
        hbox = gtk.HButtonBox()
        vbox.pack_start(scrolledwindow, True)
        vbox.pack_start(hbox, False)
        b0 = gtk.Button('Clear All')
        b1 = gtk.Button('Clear Selected')
        hbox.pack_start(b0)
        hbox.pack_start(b1)

        # create a liststore with one string column to use as the model
        liststore = gtk.ListStore(str)

        # create the TreeView using liststore
        treeview = gtk.TreeView(liststore)

        # create a CellRenderer to render the data
        cell = gtk.CellRendererText()

        # create the TreeViewColumns to display the data
        tvcolumn = gtk.TreeViewColumn('URL', cell, text=0)

        # add columns to treeview
        treeview.append_column(tvcolumn)
        b0.connect_object('clicked', gtk.ListStore.clear, liststore)
        b1.connect('clicked', self.clear_selected, treeview)
        # make treeview searchable
        treeview.set_search_column(0)

        # Allow sorting on the column
        tvcolumn.set_sort_column_id(0)

        # Allow enable drag and drop of rows including row move
        treeview.enable_model_drag_source( gtk.gdk.BUTTON1_MASK,
                                                self.TARGETS,
                                                gtk.gdk.ACTION_DEFAULT|
                                                gtk.gdk.ACTION_MOVE)
        treeview.enable_model_drag_dest(self.TARGETS,
                                             gtk.gdk.ACTION_DEFAULT)

        treeview.connect("drag_data_get", self.drag_data_get_data)
        treeview.connect("drag_data_received",
                              self.drag_data_received_data)

        scrolledwindow.add(treeview)
        self.add(vbox)
        self.show_all()

    def drag_data_get_data(self, treeview, context, selection, target_id,
                           etime):
        treeselection = treeview.get_selection()
        model, iter = treeselection.get_selected()
        data = model.get_value(iter, 0)
        selection.set(selection.target, 8, data)

    def drag_data_received_data(self, treeview, context, x, y, selection,
                                info, etime):
        model = treeview.get_model()
        data = selection.data
        drop_info = treeview.get_dest_row_at_pos(x, y)
        if drop_info:
            path, position = drop_info
            iter = model.get_iter(path)
            if (position == gtk.TREE_VIEW_DROP_BEFORE
                or position == gtk.TREE_VIEW_DROP_INTO_OR_BEFORE):
                model.insert_before(iter, [data])
            else:
                model.insert_after(iter, [data])
        else:
            model.append([data])
        if context.action == gtk.gdk.ACTION_MOVE:
            context.finish(True, True, etime)
        return

def main():
    DragAndDropDemo()
    gtk.main()

if __name__ == '__main__':
    main()
