#!/usr/bin/env python2
'''Tree View/ViewIcon0
How do I put icons in a TreeView?
You should use a gtk.CellRendererPixbuf as your column renderer.
Here is an example that shows a stock icon and a label in two columns:
'''

import pygtk
pygtk.require('2.0')
import gobject
import gtk
import os

DEMODIR = os.path.dirname(__file__)
IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
APPLE = os.path.join(IMAGEDIR, 'apple-red.png')
pixbuf = gtk.gdk.pixbuf_new_from_file(APPLE)


class ViewIcon0Demo(gtk.Window):
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

        label = gtk.Label('Treeview with Icon')
        vbox.pack_start(label, False, False)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw)

        (COL_PIXBUF, COL_STRING) = range(2)

        model = gtk.ListStore(gtk.gdk.Pixbuf, str)
        treeview = gtk.TreeView(model)

        model.append([pixbuf, "Lore Ipsum"])

        cell = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn('Icon', cell, pixbuf=COL_PIXBUF)
        treeview.append_column(column)

        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Text', cell, text=COL_STRING)
        treeview.append_column(column)
        sw.add(treeview)
        self.show_all()


if __name__ == '__main__':
    ViewIcon0Demo()
    gtk.main()
