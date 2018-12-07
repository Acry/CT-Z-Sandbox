#!/usr/bin/env python2
"""Windows/Scrolling 1

INFO HERE
"""

import pygtk
pygtk.require('2.0')
import gtk

class Scrolling1Demo(gtk.Window):
    def __init__(self, parent=None):
        # Create toplevel window
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_border_width(0)
        self.set_size_request(300, 300)

        rootbox = gtk.HBox(False, 0)
        self.add(rootbox)
        # create a new scrolled window.
        sw = gtk.ScrolledWindow()
        sw.set_border_width(10)
        rootbox.pack_start(sw)

        self.show_all()

def main():
    Scrolling1Demo()
    gtk.main()

if __name__ == '__main__':
    main()
