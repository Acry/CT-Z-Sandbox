#!/usr/bin/env python2
#region Description
'''Text Widget/Add Widget Button

Insert button to Textview.

A GTK+ widget can be inserted in a TextView at a buffer location specified with a TextChildAnchor.
The TextChildAnchor will be counted as one character and represented as "0xFFFC" similar to a pixbuf.

The TextChildAnchor can be created and inserted in the buffer by using the convenience method:
`anchor = text_buffer.create_child_anchor(iter)`

where iter is the location for the child_anchor.

A TextChildAnchor can also be created and inserted in two operations as:
`anchor = gtk.TextChildAnchor()`

`text_buffer.insert_child_anchor(iter, anchor)`
Then the widget can be added to the TextView at an anchor location using the method:

`text_view.add_child_at_anchor(child, anchor)`
The list of widgets at a particular buffer anchor can be retrieved using the method:

`widget_list = anchor.get_widgets()`

The relevant code for this demo is:
`anchor = textbuffer.create_child_anchor(iter)`
`textview.add_child_at_anchor(button, anchor)`
'''
#endregion

#region Import
import pygtk
pygtk.require('2.0')
import gtk
import os
import pango
#endregion

#region Constants
IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')

text = "Press on this button:" \
       " dolore magna aliquyam erat, sed diam voluptua.\n At vero eos et accusam et justo duo dolores et ea rebum.\n" \
       " Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.\n"
#endregion


class AddWidgetButtonDemo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_default_size(400, 450)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=200, min_height=100)

        box1 = gtk.VBox(False, 0)
        self.add(box1)

        textview = gtk.TextView()
        textbuffer = textview.get_buffer()
        textbuffer.set_text(text)
        textview.set_wrap_mode(gtk.WRAP_WORD)
        sw1 = gtk.ScrolledWindow()
        sw1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw1.add(textview)
        box1.pack_start(sw1, True, True, 0)

        button = gtk.Button(label=None, stock=gtk.STOCK_QUIT)
        button.set_size_request(80, 30)
        button.connect('pressed', lambda a: self.destroy())
        iter = textbuffer.get_iter_at_line(2)
        anchor = textbuffer.create_child_anchor(iter)
        textview.add_child_at_anchor(button, anchor)

        self.show_all()


if __name__ == '__main__':
    AddWidgetButtonDemo()
    gtk.main()
