#!/usr/bin/env python2
'''Buttons/Button 0a

Button with pixmap and label
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'apple-red.png')

class Button0aDemo(gtk.Window):

    def pixmap_label_box(self, parent, filename, label_text):
        """Create a new hbox with an image and a label packed into it and return the box."""
        # Create box for xpm and label
        box1 = gtk.HBox(False, 0)
        box1.set_border_width(2)

        # Now on to the image stuff
        image = gtk.Image()
        image.set_from_file(filename)

        # Create a label for the button
        label = gtk.Label(label_text)

        # Pack the pixmap and label into the box
        box1.pack_start(image, False, False, 3)
        box1.pack_start(label, False, False, 3)

        image.show()
        label.show()
        return box1

    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_border_width(10)
        self.set_icon_from_file(ICON_IMAGE)
        button = gtk.Button()
        box1 = self.pixmap_label_box(self.window, ICON_IMAGE, "Eat more Apples!")
        button.add(box1)
        self.add(button)
        self.show_all()


def main():
    gtk.main()


def main():
    Button0aDemo()
    gtk.main()
if __name__ == '__main__':
    main()
