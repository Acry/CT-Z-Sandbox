#!/usr/bin/env python2
'''Tooltips/Tooltip4

uses new tooltip API

Construct custom Tooltip with icon on Window:

`icon = gtk.gdk.pixbuf_new_from_file(ICON_IMAGE)`
`self.set_property("has-tooltip", True)`
# connect to the callback function that for the tooltip
# with the signal "query-tooltip"
`self.connect("query-tooltip", self.tooltip_callback, icon)`

`def tooltip_callback(...)`


'''

import pygtk
pygtk.require('2.0')
import os
import gtk
IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'apple-red.png')


class Tooltip4Demo(gtk.Window):
    def tooltip_callback(self, widget, x, y, keyboard_mode, tooltip, icon):
        # set the text for the tooltip
        tooltip.set_text("Tooltip of this window")
        # set an icon fot the tooltip
        tooltip.set_icon(icon)
        # show the tooltip
        return True
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

        icon = gtk.gdk.pixbuf_new_from_file(ICON_IMAGE)
        self.set_property("has-tooltip", True)
        # connect to the callback function that for the tooltip
        # with the signal "query-tooltip"
        self.connect("query-tooltip", self.tooltip_callback, icon)

        self.show_all()


def main():
    Tooltip4Demo()
    gtk.main()

if __name__ == '__main__':
    main()