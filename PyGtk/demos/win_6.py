#!/usr/bin/env python2
'''Windows/Window6

Creates a multiples windows.
#Using pop-up windows.
#gtk.WINDOW_POPUP
gtk.WindowGroup
gtk.WindowGroup - a group of gtk.Window widgets
'''

import pygtk
pygtk.require('2.0')
import gtk
import os
import gobject

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')


class Window6Demo(gtk.Window):
    def cb(self, windowlist):
        gobject.source_remove(self.timer)
        (x, y) = self.get_position()
        (w, h) = self.get_size()

        wx = x+w+5
        # print wx
        # wy = y
        for window in windowlist:
            window.move(wx, y)
            window.show()
            wx = wx + w + 5

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

        window2 = gtk.Window()
        window2.set_default_size(200, 200)
        window2.set_modal(True)
        window2.set_transient_for(self)
        window2.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        windows.append(window2)

        self.timer = gobject.timeout_add(500, self.cb, windows)


if __name__ == '__main__':
    Window6Demo()
    gtk.main()
