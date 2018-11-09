#!/usr/bin/env python2
'''Windows/Window

Creates a Toplevel Window.

Methods used:
set_title
set_default_size

set_geometry_hints
show_all

Functions used:
set_icon_from_file

'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'apple-red.png')

class WindowDemo(gtk.Window):
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
        self.show_all()

def main():
    WindowDemo()
    gtk.main()

if __name__ == '__main__':
    main()
