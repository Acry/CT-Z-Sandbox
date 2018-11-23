#!/usr/bin/env python2
'''Menu/MenuB3

Adding Images with `gtk.ImageMenuItem`

See the source for 3 different "methods" to do that.
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
APPLE = os.path.join(IMAGEDIR, 'apple-red.png')
OPEN = os.path.join(IMAGEDIR, 'open.png')


class MenuB3Demo(gtk.Window):
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
        # img.set_from_file
        open = gtk.ImageMenuItem("Open")
        img = gtk.Image()
        img.set_from_file(OPEN)
        open.set_image(img)
        open.connect("activate", self.menuitem_response, "Open picked")
        filemenu.append(open)
        exit = gtk.MenuItem("Exit")
        exit.connect("activate", self.menuitem_response, "Exit pressed")
        filemenu.append(exit)
        mb.append(file)

        viewmenu = gtk.Menu()
        # From StockItem
        view = gtk.ImageMenuItem("View")
        img = gtk.image_new_from_stock(gtk.STOCK_REFRESH, gtk.ICON_SIZE_MENU)
        view.set_image(img)
        view.set_submenu(viewmenu)
        set = gtk.MenuItem("Set View")
        set.connect("activate", self.menuitem_response, "Set View pressed")
        viewmenu.append(set)
        mb.append(view)

        infomenu = gtk.Menu()
        info = gtk.MenuItem("Info")
        info.set_submenu(infomenu)
        # PixBuffFromFile with scaling
        see = gtk.ImageMenuItem("See Info")
        pixbuf = gtk.gdk.pixbuf_new_from_file(APPLE)
        pixbuf = pixbuf.scale_simple(20, 20, gtk.gdk.INTERP_BILINEAR)
        img = gtk.Image()
        img.set_from_pixbuf(pixbuf)
        see.set_image(img)
        see.connect("activate", self.menuitem_response, "See Info pressed")
        infomenu.append(see)
        mb.append(info)

        vbox.pack_start(mb, False, False, 2)
        self.show_all()

    def menuitem_response(self, widget, string):
        print "%s" % string


if __name__ == '__main__':
    MenuB3Demo()
    gtk.main()
