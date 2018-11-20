#!/usr/bin/env python2
'''Buttons/Button 4

Check Buttons
Check buttons inherit many properties and methods from the the toggle buttons, but look a little different.
Rather than being buttons with text inside them, they are small squares with the text to the right of them.
These are often used for toggling options on and off in applications.

The creation method is similar to that of the normal button.
`check_button = gtk.CheckButton(label=None)`

If the label argument is specified the method creates a check button with a label beside it.
The label text is parsed for '_'-prefixed mnemonic characters.

Checking and setting the state of the check button are identical to that of the toggle button.

This program provides an example of the use of the check buttons.
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'apple-red.png')


def callback(widget, data=None):
    print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])


class Button4Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_default_size(200, 100)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)
        self.set_border_width(10)
        vbox = gtk.VBox(True, 2)
        self.add(vbox)

        # Create first button
        button = gtk.CheckButton("check button 1")
        button.connect("toggled", callback, "check button 1")
        vbox.pack_start(button, True, True, 2)

        # Create second button
        button = gtk.CheckButton("check button 2")
        button.connect("toggled", callback, "check button 2")
        vbox.pack_start(button, True, True, 2)

        self.show_all()


def main():
    Button4Demo()
    gtk.main()


if __name__ == '__main__':
    main()
