#!/usr/bin/env python2
'''Images/ImageScaling

Widget hierarchy:   gtk.Window -> gtk.AspectFrame -> gtk.Image
                    from pixbuf

using:              scale_simple
def Method:         scale

Assets: Picture taken from http://www.bigfoto.com/stones-background.jpg
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
IMAGE = "stones-background.jpg"
MAIN_IMAGE = os.path.join(IMAGEDIR, IMAGE)
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')


class ImageScalingDemo(gtk.Window):
    def scale(self, window, image, image_ratio, pixbuf):
        """Checks if window-size changed and scale image"""
        allocation = window.get_allocation()
        if self.old_height != allocation.height or self.old_width != allocation.width:
            ww = window.get_allocation().width
            wh = window.get_allocation().height

            window_ratio = float(ww)/float(wh)
            if window_ratio >= image_ratio:
                image_h = wh
                image_w = int(float(image_h) * image_ratio)
            else:
                image_w = ww
                image_h = int(float(image_w) / image_ratio)

            pixbuf = self.pixbuf_org.scale_simple(image_w, image_h, gtk.gdk.INTERP_BILINEAR)
            image.set_from_pixbuf(pixbuf)
            self.old_height = wh
            self.old_width = ww

    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_title(self.__class__.__name__)

        # initialize last Window Size
        self.old_width = 300
        self.old_height = 300

        self.set_default_size(self.old_width, self.old_height)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)

# region IMAGE

        pixbuf = gtk.gdk.pixbuf_new_from_file(MAIN_IMAGE)
        # copy of original data for scaling
        self.pixbuf_org=pixbuf.copy()

        self.org_width = pixbuf.get_width()
        self.org_height = pixbuf.get_height()

        # get image ratio
        image_ratio = float(self.org_width)/float(self.org_height)
        # get window ratio
        window_ratio = float(self.old_width)/float(self.old_height)

        # fill window respecting aspect
        if window_ratio >= image_ratio:
            image_h = self.old_height
            image_w = int(float(image_h) * image_ratio)
        else:
            image_w = self.old_width
            image_h = int(float(image_w) / image_ratio)
        # scale
        pixbuf = pixbuf.scale_simple(image_w, image_h, gtk.gdk.INTERP_BILINEAR)
        # convert pixbuf to image object
        image = gtk.Image()
        image.set_from_pixbuf(pixbuf)
# endregion

#region FRAME
        # Create an aspect_frame and add it to our toplevel window
        aspect_frame = gtk.AspectFrame(obey_child=True)
        # aspect_frame.draw_border
        self.add(aspect_frame)

        # Now add a child widget to the aspect frame
        aspect_frame.add(image)
#endregion
        # bind callback to check-resize event
        self.connect('check-resize', self.scale, image, image_ratio, pixbuf)
        self.show_all()


def main():
    ImageScalingDemo()
    gtk.main()

if __name__ == '__main__':
    main()
