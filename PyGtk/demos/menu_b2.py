#!/usr/bin/env python2
'''Menu/MenuB2

Populate the menu horizontal and vertical
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')

class MenuB2Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_default_size(400, 200)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=200, min_height=100)
        vbox = gtk.VBox(False, 0)
        self.add(vbox)

        mb = gtk.MenuBar()

        filemenu = gtk.Menu()
        file = gtk.MenuItem("File")
        file.set_submenu(filemenu)
        open = gtk.MenuItem("Open")
        open.connect("activate", self.menuitem_response, "Open picked")
        filemenu.append(open)
        exit = gtk.MenuItem("Exit")
        exit.connect("activate", self.menuitem_response, "Exit pressed")
        filemenu.append(exit)
        mb.append(file)

        viewmenu = gtk.Menu()
        view = gtk.MenuItem("View")
        view.set_submenu(viewmenu)
        set = gtk.MenuItem("Set View")
        set.connect("activate", self.menuitem_response, "Set View pressed")
        viewmenu.append(set)
        mb.append(view)

        infomenu = gtk.Menu()
        info = gtk.MenuItem("Info")
        info.set_submenu(infomenu)
        see = gtk.MenuItem("See Info")
        see.connect("activate", self.menuitem_response, "See Info pressed")
        infomenu.append(see)
        mb.append(info)

        vbox.pack_start(mb, False, False, 2)
        self.show_all()

    def menuitem_response(self, widget, string):
        print "%s" % string


if __name__ == '__main__':
    MenuB2Demo()
    gtk.main()
