#!/usr/bin/env python2
'''Buttons/Button 1

Button with Callback

The Button widget emits following signals:
      `pressed` when pointer button is pressed within Button widget

      `released` when pointer button is released within Button widget

      `clicked` when pointer button is pressed and then released within Button widget

      `enter` when pointer enters Button widget

      `leave` when pointer leaves Button widget

Constructs:
 a button

Methods used on Button:
`connect("clicked", self.hello, button)`

Constructed Methods:
`hello`

Functions used:
None
'''

import pygtk
pygtk.require('2.0')
import gtk


class Button1Demo(gtk.Window):
    # This is a callback function.
    def hello(self, widget, data):
        print data

    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_border_width(10)
    
        # Creates a new button with the label "Button 1".
        button = gtk.Button("Button 1")

        # Calling our Method hello once
        self.hello(self, "JOOOOO")

        # When the button receives the "clicked" signal, it will call the
        # function hello() passing it None as its argument.  The hello()
        # function is defined above.
        button.connect("clicked", self.hello, "hello")

        # This packs the button into the window (a GTK container).
        self.add(button)


        # and the window
        self.show_all()


    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()


def main():
    Button1Demo()
    gtk.main()
# If the program is run directly or passed as an argument to the python
# interpreter then create a instance and show it
if __name__ == '__main__':
    main()
