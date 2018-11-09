#!/usr/bin/env python2
'''Aspect Frames

The aspect frame widget is like a frame widget, except that it also enforces the aspect ratio
(that is, the ratio of the width to the height) of the child widget to have a certain value,
adding extra space if necessary. This is useful, for instance, if you want to preview a larger image.
The size of the preview should vary when the user resizes the window, but the aspect ratio needs
to always match the original image.

To create a new aspect frame use:

aspect_frame = gtk.AspectFrame(label=None, xalign=0.5, yalign=0.5, ratio=1.0, obey_child=TRUE)

label specifies the text to be displayed as the label.
xalign and yalign specify alignment as with gtk.Alignment widgets.
If obey_child is TRUE, the aspect ratio of a child widget will match the aspect ratio
of the ideal size it requests. Otherwise, it is given by ratio.

To change the options of an existing aspect frame, you can use:

  aspect_frame.set(xalign=0.0, yalign=0.0, ratio=1.0, obey_child=TRUE)

This program uses an AspectFrame to present a drawing area whose aspect ratio will always be 2:1,
no matter how the user resizes the top-level window.

'''
import pygtk
pygtk.require('2.0')
import gtk

class AspectFramesDemo(gtk.Window):
    def __init__(self, parent=None):

        # Create the toplevel window
        gtk.Window.__init__(self)

        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self = gtk.Window(gtk.WINDOW_TOPLEVEL);
        self.set_title("Aspect Frame")
        self.set_border_width(10)

        # Create an aspect_frame and add it to our toplevel window
        aspect_frame = gtk.AspectFrame("2x1", # label
                                       0.5, # center x
                                       0.5, # center y
                                       2, # xsize/ysize = 2
                                       False) # ignore child's aspect
        self.add(aspect_frame)
        aspect_frame.show()

        # Now add a child widget to the aspect frame
        drawing_area = gtk.DrawingArea()

        # Ask for a 200x200 window, but the AspectFrame will give us a 200x100
        # window since we are forcing a 2x1 aspect ratio
        drawing_area.set_size_request(200, 200)
        aspect_frame.add(drawing_area)
        drawing_area.show()

        self.show_all()

def main():
    AspectFramesDemo()
    gtk.main()

if __name__ == '__main__':
    main()