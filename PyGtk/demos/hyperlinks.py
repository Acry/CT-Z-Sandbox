#!/usr/bin/env python2
'''Text Widget/Hyperlinks

Tag hyperlinks and connect click to browser.

This Code needs feedback if it fails.
Check the code used for newline character detection.
Currently works on "https://" - to do: "http://"
'''

import sys
import os

# Newline characters:
# Windows:          '\r\n'
# Mac (OS -9):      '\r'
# Mac (OS 10+):     '\n'
# Unix/Linux:       '\n'

supported_os = ['posix', 'nt', 'mac']

if os.name not in supported_os:
    sys.exit("Sorry, OS not supported so far, happy hacking!\n")

NEWLINE_CHAR = ""

if os.name == 'nt':
    NEWLINE_CHAR = "\r"
elif os.name == 'posix':
    NEWLINE_CHAR = "\n"
else:   # FIXME, I have no clue if this works
    import platform
    mac_version = platform.mac_ver()
    v, _, _ = platform.mac_ver()
    if mac_version <= 9:
        NEWLINE_CHAR = "\r"
    else:
        NEWLINE_CHAR = "\n"

import pygtk
pygtk.require('2.0')
import gtk
import pango
import webbrowser

TEXT = "Let us see if we can tag some url's,\nhttps://github.com/Acry/CT-Z-Sandbox should work.\n"\
       "https://www.giuspen.com/cherrytree - should work also.\n\n"\
       "Either a newline or space is respected as delimiter.\n" \
       "https://www.kksou.com/php-gtk2/category/sample-codes\n"

# TODO check end of buffer - if the last newline is missing it fails

LINKLIST = []


class HyperlinksDemo(gtk.Window):
    hovering_over_link = False
    hand_cursor = gtk.gdk.Cursor(gtk.gdk.HAND2)
    regular_cursor = gtk.gdk.Cursor(gtk.gdk.XTERM)

    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_default_size(550, 250)
        self.set_border_width(0)

        view = gtk.TextView()
        view.set_wrap_mode(gtk.WRAP_WORD)
        view.connect("key-press-event", self.key_press_event)
        view.connect("event-after", self.event_after)
        view.connect("motion-notify-event", self.motion_notify_event)
        view.connect("visibility-notify-event", self.visibility_notify_event)

        buffer = view.get_buffer()

        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.add(sw)
        sw.add(view)
        self.show_page(buffer, 1)
        self.show_all()

    # Links can be activated by pressing Enter.
    def key_press_event(self, text_view, event):
        if (event.keyval == gtk.keysyms.Return or
            event.keyval == gtk.keysyms.KP_Enter):
            buffer = text_view.get_buffer()
            iter = buffer.get_iter_at_mark(buffer.get_insert())
            self.follow_if_link(text_view, iter)
        return False

    # Links can also be activated by clicking.
    def event_after(self, text_view, event):
        if event.type != gtk.gdk.BUTTON_RELEASE:
            return False
        if event.button != 1:
            return False
        buffer = text_view.get_buffer()

        # we shouldn't follow a link if the user has selected something
        try:
            start, end = buffer.get_selection_bounds()
        except ValueError:
            # If there is nothing selected, None is return
            pass
        else:
            if start.get_offset() != end.get_offset():
                return False

        x, y = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET,
            int(event.x), int(event.y))
        iter = text_view.get_iter_at_location(x, y)

        self.follow_if_link(text_view, iter)
        return False

    # Looks at all tags covering the position (x, y) in the text view,
    # and if one of them is a link, change the cursor to the "hands" cursor
    # typically used by web browsers.
    def set_cursor_if_appropriate(self, text_view, x, y):
        hovering = False

        buffer = text_view.get_buffer()
        iter = text_view.get_iter_at_location(x, y)

        tags = iter.get_tags()
        for tag in tags:
            page = tag.get_data("page")
            if page != 0:
                hovering = True
                break

        if hovering != self.hovering_over_link:
            self.hovering_over_link = hovering

        if self.hovering_over_link:
            text_view.get_window(gtk.TEXT_WINDOW_TEXT).set_cursor(self.hand_cursor)
        else:
            text_view.get_window(gtk.TEXT_WINDOW_TEXT).set_cursor(self.regular_cursor)

    # Update the cursor image if the pointer moved.
    def motion_notify_event(self, text_view, event):
        x, y = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET,
            int(event.x), int(event.y))
        self.set_cursor_if_appropriate(text_view, x, y)
        text_view.window.get_pointer()
        return False

    # Also update the cursor image if the window becomes visible
    # (e.g. when a window covering it got iconified).
    def visibility_notify_event(self, text_view, event):
        wx, wy, mod = text_view.window.get_pointer()
        bx, by = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET, wx, wy)

        self.set_cursor_if_appropriate (text_view, bx, by)
        return False

    def insert_link(self, buffer, iter, text, page):
        ''' Inserts a piece of text into the buffer, giving it the usual
            appearance of a hyperlink in a web browser: blue and underlined.
            Additionally, attaches some data on the tag, to make it recognizable
            as a link.
        '''
        tag = buffer.create_tag(None,
            foreground="blue", underline=pango.UNDERLINE_SINGLE)
        tag.set_data("page", page)
        buffer.insert_with_tags(iter, text, tag)

    def show_page(self, buffer, page):
        ''' Fills the buffer with text and interspersed links. In any real
            hypertext app, this method would parse a file to identify the links.
        '''
        global LINKLIST
        buffer.set_text(TEXT)
        search_string = 'https://'
        start, end = buffer.get_bounds()
        tag = buffer.create_tag(None, foreground="red", underline=pango.UNDERLINE_SINGLE)
        searching = True
        count = 0
        while searching:
            enter_end = False
            space_end = False
            try:
                match_start, match_end = start.forward_search(search_string, gtk.TEXT_SEARCH_VISIBLE_ONLY, limit=None)
                tag_start = match_start
                next_s = match_end
                next_enter = match_end
            except:
                searching = False
            try:
                space_start, space_end = next_s.forward_search(" ", gtk.TEXT_SEARCH_VISIBLE_ONLY, limit=None)
            except:
                space_start = False
            try:
                enter_start, enter_end = next_enter.forward_search(NEWLINE_CHAR, gtk.TEXT_SEARCH_VISIBLE_ONLY, limit=None)
            except:
                enter_start = False
            # print type(space_start)
            # print type(enter_start)
            if space_start and enter_start:
                if enter_end.compare(space_end) == -1:
                    match_end = enter_end
                else:
                    match_end = space_end
            elif space_start:
                match_end = space_end
            else:
                match_end = enter_end

            if searching:
                match_end.backward_char()
                buffer.apply_tag(tag, tag_start, match_end)
                text = tag_start.get_slice(match_end)
                # print text
                LINKLIST.append([(tag_start, match_end), text])
                start = match_end
                match_end.forward_char()
                count = count + 1
                # print "count:", count

    def follow_if_link(self, text_view, iter):
        for x in LINKLIST:
            iter_range = x[0]
            start = iter_range[0]
            end = iter_range[1]
            result = iter.in_range(start, end)
            if result:
                text = x[1]
                print text
                webbrowser.open(text)


def main():
    HyperlinksDemo()
    gtk.main()


if __name__ == '__main__':
    main()
