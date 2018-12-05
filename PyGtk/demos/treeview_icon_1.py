#!/usr/bin/env python2
'''Tree View/ViewIcon1
How do I put icons in a TreeView?
If you want to see the icon and the string in the same column.
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

DEMODIR = os.path.dirname(__file__)
IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
APPLE = os.path.join(IMAGEDIR, 'apple-red.png')
pixbuf = gtk.gdk.pixbuf_new_from_file(APPLE)
del APPLE

class ViewIcon1Demo(gtk.Window):
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

        label = gtk.Label('Treeview with icon and text')
        vbox.pack_start(label, False, False)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw)

        (COL_PIXBUF, COL_STRING, COL_STRING2) = range(3)

        model = gtk.ListStore(gtk.gdk.Pixbuf, str, str)
        treeview = gtk.TreeView(model)
        model.append([pixbuf, "Apple", "Lore Ipsum"])

        # text and icon column
        cell = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn('Icon + Text', cell, pixbuf=COL_PIXBUF)
        cell = gtk.CellRendererPixbuf()
        column.pack_start(cell, expand=False)
        cell = gtk.CellRendererText()
        column.pack_start(cell, expand=False)
        column.add_attribute(cell, 'text', COL_STRING)
        treeview.append_column(column)
        # Text only column
        column = gtk.TreeViewColumn('Text only', gtk.CellRendererText(),
                                    text=COL_STRING2)
        treeview.append_column(column)
        sw.add(treeview)
        self.show_all()


if __name__ == '__main__':
    ViewIcon1Demo()
    gtk.main()
