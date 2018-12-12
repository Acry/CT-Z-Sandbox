#!/usr/bin/env python2
"""Scribble

The DrawingArea Widget and Drawing.
Handle mouse events, how to draw in a window, and how to do drawing better by using a backing pixmap.

  drawable.draw_point(gc, x, y)

  drawable.draw_line(gc, x1, y1, x2, y2)

  drawable.draw_rectangle(gc, fill, x, y, width, height)

  drawable.draw_arc(gc, fill, x, y, width, height, angle1, angle2)

  drawable.draw_polygon(gc, fill, points)

  drawable.draw_drawable(gc, src, xsrc, ysrc, xdest, ydest, width, height)

  drawable.draw_points(gc, points)

  drawable.draw_lines(gc, points)

  drawable.draw_segments(gc, segments)

  drawable.draw_rgb_image(gc, x, y, width, height, dither, buffer, rowstride)

  drawable.draw_rgb_32_image(gc, x, y, width, height, dither, buffer, rowstride)

  drawable.draw_gray_image(gc, x, y, width, height, dither, buffer, rowstride)
"""
# GTK - The GIMP Toolkit
# Copyright (C) 1995-1997 Peter Mattis, Spencer Kimball and Josh MacDonald
# Copyright (C) 2001-2004 John Finlay
# GPL2

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
# Backing pixmap for drawing area
pixmap = None


def configure_event(widget, event):
    """Create a new backing pixmap of the appropriate size"""
    global pixmap

    x, y, width, height = widget.get_allocation()
    pixmap = gtk.gdk.Pixmap(widget.window, width, height)
    pixmap.draw_rectangle(widget.get_style().white_gc,
                          True, 0, 0, width, height)


def expose_event(widget, event):
    """Redraw the screen from the backing pixmap"""
    x, y, width, height = event.area
    widget.window.draw_drawable(widget.get_style().fg_gc[gtk.STATE_NORMAL],
                                pixmap, x, y, x, y, width, height)


def draw_brush(widget, x, y):
    """Draw a rectangle on the screen"""
    rect = (int(x-5), int(y-5), 4, 4)
    pixmap.draw_rectangle(widget.get_style().black_gc, True,
                          rect[0], rect[1], rect[2], rect[3])
    widget.queue_draw_area(rect[0], rect[1], rect[2], rect[3])


def button_press_event(widget, event):
    if event.button == 1 and pixmap != None:
        draw_brush(widget, event.x, event.y)


def motion_notify_event(widget, event):
    if event.is_hint:
        x, y, state = event.window.get_pointer()
    else:
        x = event.x
        y = event.y
        state = event.state
    if state & gtk.gdk.BUTTON1_MASK and pixmap != None:
        draw_brush(widget, x, y)


class ScribbleDemo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)
        vbox = gtk.VBox(False, 0)
        self.add(vbox)
        vbox.show()
        # Create the drawing area
        drawing_area = gtk.DrawingArea()
        drawing_area.set_size_request(200, 200)
        vbox.pack_start(drawing_area, True, True, 0)
        drawing_area.show()
        # Signals used to handle backing pixmap
        drawing_area.connect("expose_event", expose_event)
        drawing_area.connect("configure_event", configure_event)
        # Event signals
        drawing_area.connect("motion_notify_event", motion_notify_event)
        drawing_area.connect("button_press_event", button_press_event)
        drawing_area.set_events(gtk.gdk.EXPOSURE_MASK
                                | gtk.gdk.LEAVE_NOTIFY_MASK
                                | gtk.gdk.BUTTON_PRESS_MASK
                                | gtk.gdk.POINTER_MOTION_MASK
                                | gtk.gdk.POINTER_MOTION_HINT_MASK)
        # .. And a quit button
        button = gtk.Button("Quit")
        vbox.pack_start(button, False, False, 0)
        button.connect_object("clicked", lambda w: w.destroy(), self)
        button.show()
        self.show()


if __name__ == '__main__':
    ScribbleDemo()
    gtk.main()
