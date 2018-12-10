#!/usr/bin/env python2
"""Dialogs/D0

The Dialog widget is a window with a few things pre-packed into it for you.
It creates a window, and then packs a VBox into the top, which contains a separator and then an HBox called the "action_area".

Constructor is `gtk.Dialog`

It can be used for pop-up messages to the user and other similar tasks.
There is only one function for the dialog box:
`dialog = gtk.Dialog(title=None, parent=None, flags=0, buttons=None)`

where title is the text to be used in the titlebar, parent is the main application window and flags set various modes of operation for the dialog:
Flags:
`gtk.DIALOG_MODAL` - the dialog grabs all the keyboard events
`gtk.DIALOG_DESTROY_WITH_PARENT` - the dialog is destroyed when its parent is.
`gtk.DIALOG_NO_SEPARATOR` - there is no separator bar above the buttons.

The buttons argument is a `tuple` of button text and response pairs.
All arguments have defaults and can be specified using keywords.
"""

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')

class D0Demo(gtk.Window):
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
        label = gtk.Label("With label")
        dialog = gtk.Dialog("gtk.Dialog", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.pack_start(label)
        label.show()
        dialog.run()
        dialog.destroy()


if __name__ == '__main__':
    D0Demo()
    gtk.main()
