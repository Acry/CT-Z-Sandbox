#!/usr/bin/env python2
'''Images/Images2

used relevant Methods:
`gtk.Image`
`image.set_from_file`

`gtk.gdk.PixbufAnimation`
`set_from_animation`

'''

import os

import pygtk
pygtk.require('2.0')
import gobject
import gtk

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
GOALIE_IMAGE = os.path.join(IMAGEDIR, "goalie.gif")
REDAPPLE_IMAGE = os.path.join(IMAGEDIR, "apple-red.png")
CHAOS_IMAGE = os.path.join(IMAGEDIR, "chaos.jpg")
IMPORTANT_IMAGE = os.path.join(IMAGEDIR, "important.tif")
SOCCERBALL_IMAGE = os.path.join(IMAGEDIR, "soccerball.gif")

import pygtk
pygtk.require('2.0')
import gtk

class Images2Demo(gtk.Window):
    # is invoked when the button is clicked.  It just prints a message.
    def button_clicked(self, widget, data=None):
        print "button %s clicked" % data

    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_border_width(8)
        self.set_border_width(10)

        # a horizontal box to hold the buttons
        hbox = gtk.HBox()

        self.add(hbox)

        # button 1
        pixbufanim = gtk.gdk.PixbufAnimation(GOALIE_IMAGE)
        image = gtk.Image()
        image.set_from_animation(pixbufanim)
        button = gtk.Button()
        button.add(image)
        hbox.pack_start(button)
        button.connect("clicked", self.button_clicked, "1")

        # button 2
        image = gtk.Image()
        image.set_from_file(REDAPPLE_IMAGE)
        button = gtk.Button()
        button.add(image)
        hbox.pack_start(button)
        button.connect("clicked", self.button_clicked, "2")

        # button 3
        image = gtk.Image()
        image.set_from_file(CHAOS_IMAGE)
        button = gtk.Button()
        button.add(image)
        hbox.pack_start(button)
        button.connect("clicked", self.button_clicked, "3")

        # button 4
        image = gtk.Image()
        image.set_from_file(IMPORTANT_IMAGE)
        button = gtk.Button()
        button.add(image)
        hbox.pack_start(button)
        button.connect("clicked", self.button_clicked, "4")

        # button 5
        image = gtk.Image()
        image.set_from_file(SOCCERBALL_IMAGE)
        button = gtk.Button()
        button.add(image)
        hbox.pack_start(button)
        button.connect("clicked", self.button_clicked, "5")
        self.show_all()

def main():
    Images2Demo()
    gtk.main()

if __name__ == '__main__':
    main()

