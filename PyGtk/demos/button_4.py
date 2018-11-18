#!/usr/bin/env python2
'''Buttons/Button 4

Constructs:
 a round "button"

Using an EventBox with a pixmap and mask as button.

Methods used on Button:
None

Constructed Methods:
None

Functions used:
None

'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
IMAGE = "link.png"
MAIN_IMAGE = os.path.join(IMAGEDIR, IMAGE)


class Button4Demo(gtk.Window):
    def on_button_press(self, widget, data):
        print "pressed!"

    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_border_width(10)
        self.set_default_size(200, 200)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)

        rootbox = gtk.HBox(False, 0)
        self.add(rootbox)

        pixbuf = gtk.gdk.pixbuf_new_from_file(MAIN_IMAGE)
        pixmap, mask = pixbuf.render_pixmap_and_mask()
        ebox = gtk.EventBox()
        style = ebox.get_style()
        new_style = style.copy()
        new_style.bg_pixmap[gtk.STATE_NORMAL] = pixmap
        ebox.set_style(new_style)
        ebox.shape_combine_mask(mask, 0, 0)
        ebox.connect('button-press-event', self.on_button_press)
        rootbox.pack_start(ebox, True, True, 0)
        del pixmap, mask
        self.show_all()

    def main(self):
        gtk.main()


def main():
    Button4Demo()
    gtk.main()


if __name__ == '__main__':
    main()
