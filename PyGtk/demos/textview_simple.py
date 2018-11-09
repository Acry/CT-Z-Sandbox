#!/usr/bin/env python2
'''Text Widget/TextViewSimple

Creates a TextViewWidget in a Window.

Constructor:
gtk.TextView()

Methods used:
textview.get_buffer()
textbuffer.set_text(text)
textview.set_wrap_mode(gtk.WRAP_WORD)
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')

text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."


class TextViewSimpleDemo(gtk.Window):
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

        #region TextView

        #construct TextView
        textview = gtk.TextView()
        #bind TextBuffer
        textbuffer = textview.get_buffer()
        #fill TextBuffer
        textbuffer.set_text(text)

        #set wrapping type
        textview.set_wrap_mode(gtk.WRAP_WORD)
        #add to container (in this case a window)
        self.add(textview)

        #done!

        #endregion

        self.show_all()

def main():
    TextViewSimpleDemo()
    gtk.main()

if __name__ == '__main__':
    main()
