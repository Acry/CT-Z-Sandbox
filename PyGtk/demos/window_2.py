#!/usr/bin/env python2
'''Windows/Window2

Creates a Toplevel Window with background picture.

New Methods used:
-TBD-
New Functions used:
-TBD-

Image taken from:
http://www.bigfoto.com/stones-background.jpg
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
IMAGE = "stones-background.jpg"
MAIN_IMAGE = os.path.join(IMAGEDIR, IMAGE)

class Window2Demo(gtk.Window):
    def __init__(self, parent=None):

        # Create the toplevel window
        gtk.Window.__init__(self)

        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_default_size(200, 200)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)
        pixbuf = gtk.gdk.pixbuf_new_from_file(MAIN_IMAGE)
        pixmap, mask = pixbuf.render_pixmap_and_mask()
        width, height = pixmap.get_size()

        del pixbuf
        self.set_app_paintable(gtk.TRUE)

        self.resize(width, height)
        self.realize()
        try:
            self.shape_combine_mask(mask, 0, 0)  # set alpha if necessary
        except:
            pass
            self.window.set_back_pixmap(pixmap, gtk.FALSE)
        del pixmap
        self.show_all()


def main():
    Window2Demo()
    gtk.main()

if __name__ == '__main__':
    main()
