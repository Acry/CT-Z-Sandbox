#!/usr/bin/env python2
'''Windows/Window3

Creates a Toplevel Window, with custom Background Color

Key Code:
`self.modify_bg(gtk.STATE_NORMAL, color)`

    direct color
    `color = (gtk.STATE_NORMAL, gtk.gdk.Color(red=30000)`
    or
    `gtk.gdk.color_parse`
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')

class Window3Demo(gtk.Window):
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
        wish_color = "#2C4958"
        the_gdk_color = gtk.gdk.color_parse(wish_color)

        red = gtk.gdk.Color(red=30000)
        self.modify_bg(gtk.STATE_NORMAL, the_gdk_color)
        self.show_all()

def main():
    Window3Demo()
    gtk.main()

if __name__ == '__main__':
    main()
