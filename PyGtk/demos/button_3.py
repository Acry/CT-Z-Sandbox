#!/usr/bin/env python2
'''Buttons/Button 3

Toggle Buttons
Toggle buttons are derived from normal buttons and are very similar, except they will always be in one of two states,
alternated by a click. They may be depressed, and when you click again, they will pop back up.
Click again, and they will pop back down.

Toggle buttons are the basis for check buttons and radio buttons, as such, many of the calls used for toggle buttons
are inherited by radio and check buttons.

__Creating a new toggle button__:

  `toggle_button = gtk.ToggleButton(label=None)`

These work identically to the normal button widget calls. If no label is specified the button will be blank.
The label text will be parsed for '_'-prefixed mnemonic characters.

To retrieve the state of the toggle widget, including radio and check buttons,
use a construct as shown below.

This tests the state of the toggle, by calling the `get_active()` method of the toggle button object.
The signal of interest to us that is emitted by toggle buttons (the toggle button, check button, and radio button
widgets) is the "toggled" signal.

To check the state of these buttons, set up a signal handler to catch the toggled signal, and access the object
attributes to determine its state. The callback will look something like:

  `def toggle_button_callback(widget, data):`
      `if widget.get_active():`
          `# If control reaches here, the toggle button is down`
      `else:`
          `# If control reaches here, the toggle button is up`
To force the state of a toggle button, and its children, the radio and check buttons, use this method:

  `toggle_button.set_active(is_active)`

The above method can be used to set the state of the toggle button, and its children the radio and check buttons.
Specifying a `True` or `False` for the `is_active` argument indicates whether the button should be down (depressed)
or up (released). When the toggle button is created its default is up or `False`.

Note that when you use the `set_active()` method, and the state is actually changed, it causes the `clicked` and
`toggled` signals to be emitted from the button.

`toggle_button.get_active()`
This method returns the current state of the toggle button as a boolean `True` or `False` value.
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'apple-red.png')


def callback(widget, data=None):
    print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])


class Button3Demo(gtk.Window):
    def __init__(self, parent=None):

        # Create the toplevel window
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_default_size(350, 100)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)
        self.set_border_width(10)
        vbox = gtk.VBox(True, 2)
        self.add(vbox)

        # Create first button
        button = gtk.ToggleButton("toggle button 1")
        # When the button is toggled, we call the "callback" method
        # with a pointer to "button" as its argument
        button.connect("toggled", callback, "toggle button 1")
        # Insert button 1
        vbox.pack_start(button, True, True, 2)

        # Create second button
        button = gtk.ToggleButton("toggle button 2")
        # When the button is toggled, we call the "callback" method
        # with a pointer to "button 2" as its argument
        button.connect("toggled", callback, "toggle button 2")
        # Insert button 2
        vbox.pack_start(button, True, True, 2)

        self.show_all()


def main():
    Button3Demo()
    gtk.main()


if __name__ == '__main__':
    main()
