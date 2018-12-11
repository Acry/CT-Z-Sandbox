#!/usr/bin/env python2
#region Description
'''Text Widget/TextViewBasic

Creates a TextView in a scrolled Window.

Given a text (a lore ipsum) we find the occurrence of the string " et " (latin for and),
and style it.
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


class TextViewBasicDemo(gtk.Window):
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

        #region TextView
        textview = gtk.TextView()
        textbuffer = textview.get_buffer()
        textbuffer.set_text(text)
        textview.set_wrap_mode(gtk.WRAP_WORD)

        sw1 = gtk.ScrolledWindow()
        sw1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        self.add(sw1)
        sw1.add(textview)
        #endregion

        #region Search and Style
        search_string = " et "
        start, end = textbuffer.get_bounds()
        # here are some different styling methods to try out
        # tag = textbuffer.create_tag(None, foreground="blue", underline=pango.UNDERLINE_SINGLE)
        # tag = textbuffer.create_tag(None, foreground="red")
        # tag = textbuffer.create_tag(None, foreground="red", style=pango.STYLE_OBLIQUE)
        tag = textbuffer.create_tag(None, foreground="red", strikethrough=True)
        #   textbuffer.insert_with_tags(match_end, "foo", tag)

        searching = True
        count = 0
        while searching:
            try:
                match_start, match_end = start.forward_search(search_string, gtk.TEXT_SEARCH_TEXT_ONLY, limit=None)
                match_start.forward_char()
                match_end.backward_char()
                textbuffer.apply_tag(tag, match_start, match_end)
                match_end.forward_char()
                start = match_end
                count = count + 1
            except:
                searching = False
        print "Found the String:" + search_string, count, "times"
        #endregion
        self.show_all()

def main():
    TextViewBasicDemo()
    gtk.main()

if __name__ == '__main__':
    main()
