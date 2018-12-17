#!/usr/bin/env python2
"""Drawing Area/Donut

This program creates a donut with `gtk.DrawingArea()` using cairo library.

based on:
ZetCode PyGTK tutorial
Author: Jan Bodnar
http://zetcode.com/gui/pygtk/drawingII/
"""

import pygtk
pygtk.require('2.0')
import gtk
import math
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
# Backing pixmap for drawing area
pixmap = None


class DonutDemo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)
        darea = gtk.DrawingArea()
        darea.set_size_request(300, 300)
        darea.connect("expose-event", self.expose)
        self.add(darea)
        self.show_all()

    def expose(self, widget, event):
        cr = widget.window.cairo_create()

        cr.set_line_width(0.5)

        w = self.allocation.width
        h = self.allocation.height

        cr.translate(w / 2, h / 2)
        cr.arc(0, 0, 120, 0, 2 * math.pi)
        cr.stroke()

        for i in range(36):
            cr.save()
            cr.rotate(i * math.pi / 36)
            cr.scale(0.3, 1)
            cr.arc(0, 0, 120, 0, 2 * math.pi)
            cr.restore()
            cr.stroke()


if __name__ == '__main__':
    DonutDemo()
    gtk.main()
