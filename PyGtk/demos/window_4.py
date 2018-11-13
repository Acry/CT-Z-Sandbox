#!/usr/bin/env python2
'''Windows/Window4

Creates a Toplevel Window, with custom Background Color Gradient
(horizontal this time)

Key Code:
Need cairo for this.
Constructing a cairo surface on the DrawingArea Window
see the rest in the expose callback

For now use:
http://corecoding.com/utilities/rgb-or-hex-to-float.php
for float RGB
'''

import pygtk
pygtk.require('2.0')
import gtk
import os
import cairo

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'apple-red.png')

class Window4Demo(gtk.Window):
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

        darea = gtk.DrawingArea()
        darea.connect("expose-event", self.expose)
        self.add(darea)
        self.show_all()

    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        ww = self.allocation.width
        wh = self.allocation.height
        cr.rectangle(0, 0, ww, wh)
        # x0 (float) - x coordinate of the start point
        # y0 (float) - y coordinate of the start point
        # x1 (float) - x coordinate of the end point
        # y1 (float) - y coordinate of the end point
        lg = cairo.LinearGradient(0.0, 0.0, float(ww), 0.0)
        lg.add_color_stop_rgba(0.0, 0.086, 0.133, 0.169, 1.0)
        lg.add_color_stop_rgba(1.0, 0.224, 0.373, 0.447, 1.0)
        cr.set_source(lg)
        cr.fill()


def main():
    Window4Demo()
    gtk.main()

if __name__ == '__main__':
    main()
