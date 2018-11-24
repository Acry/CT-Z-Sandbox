#!/usr/bin/env python2
"""Dialogs/D1

A more complex dialog example.

__GTK Response Type Constants__:

gtk.RESPONSE_NONE
gtk.RESPONSE_REJECT
gtk.RESPONSE_ACCEPT
gtk.RESPONSE_DELETE_EVENT
gtk.RESPONSE_OK
gtk.RESPONSE_CANCEL
gtk.RESPONSE_CLOSE
gtk.RESPONSE_YES
gtk.RESPONSE_NO
gtk.RESPONSE_APPLY
gtk.RESPONSE_HELP
"""

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'apple-red.png')

class D1Demo(gtk.Window):
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

        label = gtk.Label("Label")
        dialog = gtk.Dialog("Dialog",
                            None,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                             gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.pack_start(label)
        label.show()
        checkbox = gtk.CheckButton("checkbox")
        dialog.action_area.pack_end(checkbox)
        checkbox.show()
        response = dialog.run()
        dialog.destroy()
        print type(response)
        print response


if __name__ == '__main__':
    D1Demo()
    gtk.main()
