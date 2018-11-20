#!/usr/bin/env python2
'''Buttons/Button 5

Radio Buttons
Radio buttons are similar to check buttons except they are grouped so that only one may be selected/depressed at a time.
This is good for places in your application where you need to select from a short list of options.

Creating a new radio button is done with this call:
`radio_button = gtk.RadioButton(group=None, label=None)`

You'll notice the extra argument to this call. Radio buttons require a group to operate properly.
The first call to `gtk.RadioButton()` should pass None as the first argument and a new radio button group will be
created with the new radio button as its only member.

To add more radio buttons to a group, pass in a reference to a radio button in group in subsequent calls to
`gtk.RadioButton()`.

If a label argument is specified the text will be parsed for '_'-prefixed mnemonic characters.

It is also a good idea to explicitly set which button should be the default depressed button with:
`radio_button.set_active(is_active)`

This is described in at toggle buttons, and works in exactly the same way. Once the radio buttons are grouped together,
only one of the group may be active at a time. If the user clicks on one radio button, and then on
another, the first radio button will first emit a `toggled` signal (to report becoming inactive), and then the second
will emit its 'toggled' signal (to report becoming active).

The example program creates a radio button group with three buttons.
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'apple-red.png')


def callback(widget, data=None):
    print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])


class Button5Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_default_size(150, 120)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)
        self.set_border_width(10)

        box1 = gtk.VBox(False, 0)
        self.add(box1)
        box2 = gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)

        button = gtk.RadioButton(None, "Option 1")
        button.connect("toggled", callback, "Option 1")
        box2.pack_start(button, True, True, 0)


        button = gtk.RadioButton(button, "Option 2")
        button.connect("toggled", callback, "Option 2")
        button.set_active(True)
        box2.pack_start(button, True, True, 0)


        button = gtk.RadioButton(button, "Option 3")
        button.connect("toggled", callback, "Option 3")
        box2.pack_start(button, True, True, 0)

        # separator = gtk.HSeparator()
        # box1.pack_start(separator, False, True, 0)
        # separator.show()
        #
        # box2 = gtk.VBox(False, 10)
        # box2.set_border_width(10)
        # box1.pack_start(box2, False, True, 0)
        # box2.show()
        #
        # button = gtk.Button("close")
        # button.connect_object("clicked", self.close_application, self.window,
        #                       None)
        # box2.pack_start(button, True, True, 0)
        # button.set_flags(gtk.CAN_DEFAULT)
        # button.grab_default()
        # button.show()
        self.show_all()


def main():
    Button5Demo()
    gtk.main()


if __name__ == '__main__':
    main()
