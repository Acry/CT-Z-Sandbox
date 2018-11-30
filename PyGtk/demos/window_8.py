#!/usr/bin/env python2
'''Windows/Window8
Rudimentary Demo that shows how tu use a masked window as connection between two windows.
'''

import pygtk
pygtk.require('2.0')
import gtk
import os
import gobject

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
ARROWS_IMAGE = os.path.join(IMAGEDIR, 'arrows.svg')


class Window8Demo(gtk.Window):
    def cb(self, windowlist):
        gobject.source_remove(self.timer)
        (x, y) = self.get_position()
        (w, h) = self.get_size()

        wx = x+w+40
        print windowlist
        windowlist[0].move(wx, y)
        windowlist[0].show()

        wx = x+w-30
        wy = y+80
        windowlist[1].move(wx, wy)
        windowlist[1].show()

    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_default_size(200, 200)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)
        box = gtk.HBox()
        self.add(box)
        self.show_all()
        self.timer = None

        windows = []
        window1 = gtk.Window()
        window1.set_default_size(200, 200)
        window1.set_modal(True)
        window1.set_transient_for(self)
        window1.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        windows.append(window1)


        pixbuf = gtk.gdk.pixbuf_new_from_file(ARROWS_IMAGE)
        # pixbuf = pixbuf.scale_simple(100, 100, gtk.gdk.INTERP_BILINEAR)
        pixmap, mask = pixbuf.render_pixmap_and_mask()

        image = gtk.Image()
        image.set_from_pixbuf(pixbuf)
        del pixbuf
        image.show()

        fixed = gtk.Fixed()
        fixed.put(image, 0, 0)
        fixed.show()
        window2 = gtk.Window()
        window2.set_transient_for(self)
        window2.add(fixed)
        window2.shape_combine_mask(mask, 0, 0)
        try:
            window2.shape_combine_mask(mask, 0, 0)  # set alpha if necessary
        except:
            pass
        del pixmap
        window2.set_decorated(False)
        windows.append(window2)

        # I need to set this timer once as a delay before querying main windows pos.
        self.timer = gobject.timeout_add(500, self.cb, windows)


if __name__ == '__main__':
    Window8Demo()
    gtk.main()
