#!/usr/bin/env python2
'''Buttons/Button 0

Constructs:
 a button

Methods used on Button:
None

Constructed Methods:
None

Functions used:
None

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
