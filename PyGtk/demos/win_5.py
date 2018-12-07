#!/usr/bin/env python2
'''Windows/Window5

Creates a multiples windows.
#Using pop-up windows.
#gtk.WINDOW_POPUP

'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')


class Window5Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)

        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_default_size(800, 800)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)
        box = gtk.HBox()
        self.add(box)

        #
        # box.pack_start(window1)
        self.show_all()
        #gtk.WINDOW_POPUP
        window1 = gtk.Window()
        window1.set_default_size(200, 200)
        # window1.set_modal( True )
        # window1.set_transient_for( self )
        # window1.set_type_hint( gtk.gdk.WINDOW_TYPE_HINT_DIALOG )
        window1.set_icon_from_file(ICON_IMAGE)
        window1.show()


if __name__ == '__main__':
    Window5Demo()
    gtk.main()
