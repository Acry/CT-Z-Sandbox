#!/usr/bin/env python2
'''Windows/Window

Creates a Toplevel Window.

Methods used:
`set_title`
`set_default_size`

`set_geometry_hints`
`show_all`

Functions used:
`set_icon_from_file`
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'apple-red.png')
text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et" \
       " dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum." \
       " Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
text2 = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et" \
       " dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum." \
       " Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
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


        textview = gtk.TextView()
        textbuffer = textview.get_buffer()
        textbuffer.set_text(text)
        textview.set_wrap_mode(gtk.WRAP_WORD)

        sw1 = gtk.ScrolledWindow()
        sw1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw1.add(textview)

        textview2 = gtk.TextView()
        textbuffer2 = textview2.get_buffer()
        textbuffer2.set_text(text2)
        textview2.set_wrap_mode(gtk.WRAP_WORD)

        sw2 = gtk.ScrolledWindow()
        sw2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw2.add(textview2)
        vbox = gtk.VBox()
        self.add(vbox)
        vbox.pack_start(sw1, True, True)
        vbox.pack_start(sw2, True, True)
        self.show_all()

def main():
    WindowDemo()
    gtk.main()

if __name__ == '__main__':
    main()
