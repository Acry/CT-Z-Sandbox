#!/usr/bin/env python2
'''Tree View/Tree Store 0


'''

import pygtk
pygtk.require('2.0')
import gobject
import gtk


class TreeStore0Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_default_size(650, 400)
        self.set_border_width(8)

        vbox = gtk.VBox(False, 8)
        self.add(vbox)

        label = gtk.Label("Jonathan's Holiday Card Planning Sheet")
        vbox.pack_start(label, False, False)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw)

        # create model
        model = self.__create_model()

        # create treeview
        treeview = gtk.TreeView(model)
        treeview.set_rules_hint(True)

        self.__add_columns(treeview)

        sw.add(treeview)

        # expand all rows after the treeview widget has been realized
        treeview.connect('realize', lambda tv: tv.expand_all())

        self.show_all()

    def __create_model(self):

        # create tree store
        model = gtk.TreeStore(
                    gobject.TYPE_STRING,
                    gobject.TYPE_BOOLEAN,
                    gobject.TYPE_BOOLEAN,
                    gobject.TYPE_BOOLEAN,
                    gobject.TYPE_BOOLEAN,
                    gobject.TYPE_BOOLEAN,
                    gobject.TYPE_BOOLEAN,
                    gobject.TYPE_BOOLEAN)

        # add data to the tree store
        for month in toplevel:
            iter = model.append(None)
            model.set(iter,
                HOLIDAY_NAME_COLUMN, month[HOLIDAY_NAME_COLUMN],
                ALEX_COLUMN, False,
                HAVOC_COLUMN, False,
                TIM_COLUMN, False,
                OWEN_COLUMN, False,
                DAVE_COLUMN, False,
                VISIBLE_COLUMN, False,
                WORLD_COLUMN, False
           )

            # add children
            for holiday in month[-1]:
                child_iter = model.append(iter);
                model.set(child_iter,
                    HOLIDAY_NAME_COLUMN, holiday[HOLIDAY_NAME_COLUMN],
                    ALEX_COLUMN, holiday[ALEX_COLUMN],
                    HAVOC_COLUMN, holiday[HAVOC_COLUMN],
                    TIM_COLUMN, holiday[TIM_COLUMN],
                    OWEN_COLUMN, holiday[OWEN_COLUMN],
                    DAVE_COLUMN, holiday[DAVE_COLUMN],
                    VISIBLE_COLUMN, True,
                    WORLD_COLUMN, holiday[WORLD_COLUMN-1]
               )

        return model

    def on_item_toggled(self, cell, path_str, model):

        # get selected column
        column = cell.get_data('column')

        # get toggled iter
        iter = model.get_iter_from_string(path_str)
        toggle_item = model.get_value(iter, column)

        # do something with the value
        toggle_item = not toggle_item

        # set new value
        model.set(iter, column, toggle_item)


    def __add_columns(self, treeview):
        model = treeview.get_model()

        # column for holiday names
        renderer = gtk.CellRendererText()
        renderer.set_property("xalign", 0.0)

        #col_offset = gtk.TreeViewColumn("Holiday", renderer, text=HOLIDAY_NAME_COLUMN)
        column = gtk.TreeViewColumn("Holiday", renderer, text=HOLIDAY_NAME_COLUMN)
        #column = gtk_tree_view_get_column(GTK_TREE_VIEW(treeview), col_offset - 1);
        column.set_clickable(True)

        treeview.append_column(column)

        # alex column */
        renderer = gtk.CellRendererToggle()
        renderer.set_property("xalign", 0.0)
        renderer.set_data("column", ALEX_COLUMN)

        renderer.connect("toggled", self.on_item_toggled, model)

        column = gtk.TreeViewColumn("Alex", renderer, active=ALEX_COLUMN,
                                    visible=VISIBLE_COLUMN, activatable=WORLD_COLUMN)

        # set this column to a fixed sizing(of 50 pixels)
        #column = gtk_tree_view_get_column(GTK_TREE_VIEW(treeview), col_offset - 1);
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(50)
        column.set_clickable(True)

        treeview.append_column(column)

        # havoc column
        renderer = gtk.CellRendererToggle();
        renderer.set_property("xalign", 0.0)
        renderer.set_data("column", HAVOC_COLUMN)

        renderer.connect("toggled", self.on_item_toggled, model)

        column = gtk.TreeViewColumn("Havoc", renderer, active=HAVOC_COLUMN,
                                    visible=VISIBLE_COLUMN)

        #column = treeview.get_column(col_offset - 1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(50)
        column.set_clickable(True)

        treeview.append_column(column)

        # tim column
        renderer = gtk.CellRendererToggle();
        renderer.set_property("xalign", 0.0)
        renderer.set_data("column", TIM_COLUMN)

        renderer.connect("toggled", self.on_item_toggled, model)

        column = gtk.TreeViewColumn("Tim", renderer, active=TIM_COLUMN,
                                    visible=VISIBLE_COLUMN, activatable=WORLD_COLUMN)

        #column = treeview.get_column(col_offset - 1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(50)
        column.set_clickable(True)

        treeview.append_column(column)

        # owen column
        renderer = gtk.CellRendererToggle();
        renderer.set_property("xalign", 0.0)
        renderer.set_data("column", OWEN_COLUMN)

        renderer.connect("toggled", self.on_item_toggled, model)

        column = gtk.TreeViewColumn("Owen", renderer, active=OWEN_COLUMN,
                                    visible=VISIBLE_COLUMN)

        #column = treeview.get_column(col_offset - 1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(50)
        column.set_clickable(True)

        treeview.append_column(column)

        # dave column
        renderer = gtk.CellRendererToggle();
        renderer.set_property("xalign", 0.0)
        renderer.set_data("column", DAVE_COLUMN)

        renderer.connect("toggled", self.on_item_toggled, model)

        column = gtk.TreeViewColumn("Dave", renderer, active=DAVE_COLUMN,
                                    visible=VISIBLE_COLUMN)

        #column = treeview.get_column(col_offset - 1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(50)
        column.set_clickable(True)

        treeview.append_column(column)


if __name__ == '__main__':
    TreeStore0Demo()
    gtk.main()
