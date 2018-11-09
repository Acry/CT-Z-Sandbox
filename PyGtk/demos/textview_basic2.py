#!/usr/bin/env python2
#region Description
'''Text Widget/TextViewBasic2

Mark Text and style it.

Creates a TextView in a scrolled Window.

Pango Styles:
https://developer.gnome.org/pygtk/stable/pango-constants.html
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

text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et" \
       " dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum." \
       " Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
#endregion

class TextViewBasic2Demo(gtk.Window):
    def btn_click(self, widget, textbuffer, tag):
        print "Printing Message"
        try:
            start, end = textbuffer.get_selection_bounds()
            textbuffer.apply_tag(tag, start, end)
        except:
            return
    def insert_link(self, buffer, iter, text, page):
        """ Inserts a piece of text into the buffer, giving it the usual
            appearance of a hyperlink in a web browser: blue and underlined.
            Additionally, attaches some data on the tag, to make it recognizable
            as a link.
        """
        tag = buffer.create_tag(None,
                                foreground="blue", underline=pango.UNDERLINE_SINGLE)
        tag.set_data("page", page)
        buffer.insert_with_tags(iter, text, tag)

    def __init__(self, parent=None):

        #region Window init
        gtk.Window.__init__(self)

        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_default_size(400, 210)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=200, min_height=100)
        #endregion

        box1 = gtk.VBox(False, 0)

        self.add(box1)
        # Creates a new button with the label "Button 1".
        button = gtk.Button("Style Selected")

        # This packs the button into the box.
        box1.pack_start(button, False, False, 0)
        #region TextView

        textview = gtk.TextView()
        textbuffer = textview.get_buffer()
        textbuffer.set_text(text)

        textview.set_wrap_mode(gtk.WRAP_WORD)
        sw1 = gtk.ScrolledWindow()
        sw1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw1.add(textview)
        box1.pack_start(sw1, True, True, 0)
        #endregion

        tag = textbuffer.create_tag(None, background="grey", foreground="orange", style=pango.STYLE_OBLIQUE)
        button.connect("clicked", self.btn_click, textbuffer, tag)
        self.show_all()

def main():
    TextViewBasic2Demo()
    gtk.main()

if __name__ == '__main__':
    main()
