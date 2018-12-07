#!/usr/bin/env python2
'''Windows/Window7

Creates an undecorated window showing a masked image.
To close the window, click it.
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
STAR_IMAGE = os.path.join(IMAGEDIR, 'star.png')


class Window7Demo(gtk.Window):
    def close(self, win, data):
        win.destroy()
        if __name__ == '__main__':
            gtk.main_quit()

    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_geometry_hints(min_width=100, min_height=100)

        pixbuf = gtk.gdk.pixbuf_new_from_file(STAR_IMAGE)
        pixmap, mask = pixbuf.render_pixmap_and_mask()

        image = gtk.Image()
        image.set_from_pixbuf(pixbuf)
        del pixbuf
        image.show()

        fixed = gtk.Fixed()
        fixed.put(image, 0, 0)
        fixed.show()
        self.add(fixed)

        # This masks out everything except for the image itself
        self.shape_combine_mask(mask, 0, 0)
        try:
            self.shape_combine_mask(mask, 0, 0)  # set alpha if necessary
        except:
            self.window.set_back_pixmap(pixmap, gtk.FALSE)
        del pixmap
        self.connect("delete_event", self.close)
        self.set_events(self.get_events() | gtk.gdk.BUTTON_PRESS_MASK)
        self.connect("button_press_event", self.close)
        self.set_decorated(False)
        self.show()


if __name__ == '__main__':
    Window7Demo()
    gtk.main()
