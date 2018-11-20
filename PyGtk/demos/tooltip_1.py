#!/usr/bin/env python2
'''Tooltips/Tooltip1

uses deprecated tooltips API:

Construct Tooltip:
`self.tooltips = gtk.Tooltips()`
`self.tooltips.set_tip(self, "Tooltip of this window")`
'''

import pygtk
pygtk.require('2.0')
import os
import gtk
IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'apple-red.png')


class Tooltip1Demo(gtk.Window):
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
        self.set_border_width(10)

        self.tooltips = gtk.Tooltips()
        self.tooltips.set_tip(self, "Tooltip of this window")

        self.show_all()


def main():
    Tooltip1Demo()
    gtk.main()


if __name__ == '__main__':
    main()