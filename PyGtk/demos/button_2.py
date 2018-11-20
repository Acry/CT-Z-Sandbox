#!/usr/bin/env python2
'''Buttons/Button 2

Creates:
 a Toplevel Window.
 a button

Methods used on Window:
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


class Button2Demo(gtk.Window):
    # This is a callback function.
    # The data arguments are ignored
    # in this example.
    def hello(self, widget, data):
        print "Printing Message"

    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        print "close button pressed, delete event occurred"
        print "Not finishing in method delete_event"
        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred, destroy was called"
        lambda *w: gtk.main_quit()
        # gtk.main_quit(self)

    def __init__(self, parent=None):

        # Create the toplevel window
        gtk.Window.__init__(self)

        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect("destroy", self.destroy)

        # When the window is given the "delete_event" signal (this is given
        # by the window manager, usually by the "close" option, or on the
        # titlebar), we ask it to call the delete_event () function
        # as defined above. The data passed to the callback
        # function is NULL and is ignored in the callback function.
        self.connect("delete_event", self.delete_event)
    
        # Here we connect the "destroy" event to a signal handler.  
        # This event occurs when we call gtk_widget_destroy() on the window,
        # or if we return FALSE in the "delete_event" callback.
        self.connect("destroy", self.destroy)
    
        # Sets the border width of the window.
        self.set_border_width(10)
    
        # Creates a new button with the label "Button 1".
        button = gtk.Button("Button 1")
    
        # When the button receives the "clicked" signal, it will call the
        # function hello() passing it None as its argument.  The hello()
        # function is defined above.
        button.connect("clicked", self.hello, button)

        # This packs the button into the window (a GTK container).
        self.add(button)

        # and the window
        self.show_all()

def main():
    Button2Demo()
    gtk.main()
# If the program is run directly or passed as an argument to the python
# interpreter then create a instance and show it
if __name__ == '__main__':
    main()
