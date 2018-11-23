#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''Text Widget/Tags

Creating and Applying TextTags
TextTags contain one or more attributes (e.g. foreground and background colors, font, editability) that can be applied to one or more ranges of text in a TextBuffer.

TextTags can be named or anonymous. A TextTag is created using the function:
`tag = gtk.TextTag(name=None)`

The attributes can be set by using the method:
`tag.set_property(name, value)`

Where name is a string containing the name of the property and value is what the property should be set to.
Likewise the attribute value can be retrieved with the method:
`value = tag.get_property(name)`

A TextTag can be created with attributes and installed in the TextTagTable of a TextBuffer by using the convenience method:
`tag = textbuffer.create_tag(name=None, attr1=val1, attr2=val2, ...)`

where name is a string specifying the name of the tag or None if the tag is an anonymous tag and the keyword-value pairs specify the attributes that the tag will have.

A tag can be applied to a range of text in a textbuffer by using the methods:
`textbuffer.apply_tag(tag, start, end)`

`textbuffer.apply_tag_by_name(name, start, end)`

tag is the tag to be applied to the text. name is the name of the tag to be applied.
start and end are textiters that specify the range of text that the tag is to be applied to.

A tag can be removed from a range of text by using the methods:
`textbuffer.remove_tag(tag, start, end)`

`textbuffer.remove_tag_by_name(name, start, end)`

All tags for a range of text can be removed by using the method:

`textbuffer.remove_all_tags(start, end)`

__Text Tag Tables__
A TextTagTable will be created by default when a TextBuffer is created.
`table = textbuffer.get_tag_table()` or `table = textbuffer.props.tag_table`
gets the buffers table.

A TextTagTable can also be created with the function:
`table = TextTagTable()`

A TextTag can be added to a TextTagTable using the method:
`table.add(tag)`

The tag must not be in the table and must not have the same name as another tag in the table.

You can find a TextTag in a TextTagTable using the method:
`tag = table.lookup(name)`

The method returns the tag in the table with the given name or `None` if no tag has that name.

A TextTag can be removed from a TextTagTable with the method:
`table.remove(tag)`

The size of the TextTagTable can be obtained with the method:
`size = table.get_size()`
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')

text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et"\
       "dolore magna aliquyam erat, sed diam voluptua.\n At vero eos et accusam et justo duo dolores et ea rebum.\n"\
       "Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."


class TagsDemo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_default_size(500, 250)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)
        rootbox = gtk.VBox()
        self.add(rootbox)
        #region TextView
        textview = gtk.TextView()
        textbuffer = textview.get_buffer()
        textbuffer.set_text(text)
        textview.set_wrap_mode(gtk.WRAP_WORD)
        #endregion
        line_count = textbuffer.get_line_count()
        char_count = textbuffer.get_char_count()

        iter = textbuffer.get_iter_at_line(2)
        textbuffer.place_cursor(iter)

        table = textbuffer.get_tag_table()
        tag_red = gtk.TextTag(name="red")
        tag_red.set_property("foreground", "red")
        table.add(tag_red)

        tag_blue = gtk.TextTag(name="blue")
        tag_blue.set_property("foreground", "blue")
        table.add(tag_blue)

        tag_green = gtk.TextTag(name="green")
        tag_green.set_property("foreground", "green")
        table.add(tag_green)

        size = table.get_size()

        start, end = textbuffer.get_bounds()
        textbuffer.apply_tag(tag_red, start, end)

        Label_text ="Table contains: " + str(size) + " Tags"
        rootbox.pack_start(textview)
        status_bar = gtk.InfoBar()
        rootbox.pack_start(status_bar, False, False)
        status_bar.set_message_type(gtk.MESSAGE_INFO)
        status_bar.get_content_area().pack_start(
                gtk.Label(Label_text),
                False, False)
        tagtable = textbuffer.props.tag_table

        def foreach_func(tag, data):
            print tag.props.name

        tagtable.foreach(foreach_func, None)

        self.show_all()

def main():
    TagsDemo()
    gtk.main()

if __name__ == '__main__':
    main()
