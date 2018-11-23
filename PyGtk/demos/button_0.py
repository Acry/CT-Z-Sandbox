#!/usr/bin/env python2
'''Buttons/Button 0

The Button Widget

There are four different types of default buttons:
Normal buttons, toggle buttons, check buttons, and radio buttons.

__The normal button__:
You can use the `gtk.Button()` function to create a button with a label by passing a string parameter, or to create a blank button by not specifying a label string.

It's then up to you to pack a label or pixmap into this new button.

To do this, create a new box, and then pack your objects into this box using the usual `pack_start()` method, and then use the `add()` method to pack the box into the button.

The function to create a button is:
`button = gtk.Button(label=None, stock=None)`

If the label text is specified it is used as the text on the button.
If stock is specified it is used to select a stock icon and text label for the button.
The stock items are browseable in the [Stock Item and Icon Browser Demo].
'''

import pygtk
pygtk.require('2.0')
import gtk


class Button0Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_border_width(10)
    
        # Creates a new button with the label "Button 1".
        button = gtk.Button("Button 1")

        # This packs the button into the window (a GTK container).
        self.add(button)

        # and the window
        self.show_all()


    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()


def main():
    Button0Demo()
    gtk.main()
# If the program is run directly or passed as an argument to the python
# interpreter then create a instance and show it
if __name__ == '__main__':
    main()
