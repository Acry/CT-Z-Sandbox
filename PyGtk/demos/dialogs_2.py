#!/usr/bin/env python2
"""Dialogs/D2
Showing 2 Message Dialogs.
* one with the default info image
* the other with a custom image

class `gtk.MessageDialog(gtk.Dialog)`:
`gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_NONE, message_format=None)`

Properties:
buttons
image
message_area
message_type
secondary_use_markup
text
use_markup

Style
message-border
use-separator

Attributes
"image"	Read	The stock ID image
`MessageDialog.set_image`

"label"	Read	The label widget that contains the message text.

gtk.MESSAGE_INFO, gtk.MESSAGE_WARNING, gtk.MESSAGE_QUESTION or gtk.MESSAGE_ERROR.

Default value: gtk.MESSAGE_INFO
"""
#region prolog
import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'apple-red.png')
#endregion


class D2Demo(gtk.Window):
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

        dialog = gtk.MessageDialog(self, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_OK, "For your information")
        dialog.run()
        dialog.destroy()
        image = gtk.Image()
        image.set_from_file(ICON_IMAGE)
        image.show()
        dialog = gtk.MessageDialog(self, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_CLOSE, "For your information")
        dialog.set_image(image)
        dialog.run()
        dialog.destroy()


if __name__ == '__main__':
    D2Demo()
    gtk.main()
