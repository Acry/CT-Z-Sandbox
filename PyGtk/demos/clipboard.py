#!/usr/bin/env python2
'''Clipboard

A Clipboard provides a storage area for sharing data between processes or between different widgets in the same process.
Each Clipboard is identified by a string name encoded as a `gdk.Atom`.
You can use any name you want to identify a Clipboard and a new one will be created if it doesn't exist.
If you want to share a Clipboard with other processes each process will need to know the Clipboard's name.

Clipboards are built on the SelectionData and selection interfaces.
The default Clipboard used by the TextView, Label and Entry widgets is "CLIPBOARD".
Other common clipboards are "PRIMARY" and "SECONDARY" that correspond to the primary and secondary selections (Win32 ignores these).

These can also be specified using the gtk.gdk.Atom objects:
 `gtk.gdk.SELECTION_CLIPBOARD`, `gtk.gdk.SELECTION_PRIMARY` and `gtk.gdk.SELECTION_SECONDARY`.

See the gtk.gdk.Atom reference documentation for more information:
https://developer.gnome.org/pygtk/stable/class-gdkatom.html
'''

import pygtk
pygtk.require('2.0')
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'apple-red.png')
import gtk, gobject

class ClipboardInfo:
    pass

class ClipboardDemo(gtk.Window):
    # update button label and tooltips
    def update_buttons(self):
        for i in range(len(self.clipboard_history)):
            info = self.clipboard_history[i]
            if info:
                button = self.buttons[i]
                if info.text:
                    button.set_label(' '.join(info.text[:16].split('\n')))
                if info.targets:
                    # put target info in button tootip
                    self.button_tips.set_tip(button, info.targets)
        return

    # singal handler called when clipboard returns target data
    def clipboard_targets_received(self, clipboard, targets, info):
        if targets:
            # have to remove dups since Netscape is broken
            targ = {}
            for t in targets:
                targ[str(t)] = 0
            targ = targ.keys()
            targ.sort()
            info.targets = '\n'.join(targ)
        else:
            info.targets = None
            print 'No targets for:', info.text
        self.update_buttons()
        return

    # signal handler called when the clipboard returns text data
    def clipboard_text_received(self, clipboard, text, data):
        if not text or text == '':
            return
        cbi = ClipboardInfo()
        cbi.text = text
        # prepend and remove duplicate
        history = [info for info in self.clipboard_history
                   if info and info.text<>text]
        self.clipboard_history = ([cbi] + history)[:self.num_buttons]
        self.clipboard.request_targets(self.clipboard_targets_received, cbi)
        return

    # display the clipboard history text associated with the button
    def clicked_cb(self, button):
        i = self.buttons.index(button)
        if self.clipboard_history[i]:
            self.textbuffer.set_text(self.clipboard_history[i].text)
        else:
            self.textbuffer.set_text('')
        return

    # get the clipboard text
    def fetch_clipboard_info(self):
        self.clipboard.request_text(self.clipboard_text_received)
        return True

    def set_clipboard(self, button):
        text = self.textbuffer.get_text(*self.textbuffer.get_bounds())
        self.clipboard.set_text(text)
        return


    def __init__(self, parent=None):

        # Create the toplevel window
        gtk.Window.__init__(self)

        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.num_buttons = 10
        self.buttons = self.num_buttons * [None]
        self.clipboard_history = self.num_buttons * [None]
        self.set_title(self.__class__.__name__)
        self.set_default_size(200, 200)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)
        self.set_border_width(0)
        vbbox = gtk.VButtonBox()
        vbbox.show()
        vbbox.set_layout(gtk.BUTTONBOX_START)
        hbox = gtk.HBox()
        hbox.pack_start(vbbox, False)
        hbox.show()
        self.button_tips = gtk.Tooltips()

        for i in range(self.num_buttons):
            self.buttons[i] = gtk.Button("---")
            self.buttons[i].set_use_underline(False)
            vbbox.pack_start(self.buttons[i])
            self.buttons[i].show()
            self.buttons[i].connect("clicked", self.clicked_cb)

        vbox = gtk.VBox()

        scrolledwin = gtk.ScrolledWindow()

        self.textview = gtk.TextView()

        self.textview.set_size_request(200,100)
        self.textview.set_wrap_mode(gtk.WRAP_CHAR)
        self.textbuffer = self.textview.get_buffer()
        scrolledwin.add(self.textview)
        vbox.pack_start(scrolledwin)
        button = gtk.Button('Copy to Clipboard')

        button.connect('clicked', self.set_clipboard)
        vbox.pack_start(button, False)
        hbox.pack_start(vbox)
        self.add(hbox)

        self.clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
        self.clipboard.request_text(self.clipboard_text_received)
        gobject.timeout_add(1500, self.fetch_clipboard_info)
        self.show_all()


def main():
    ClipboardDemo()
    gtk.main()


if __name__ == '__main__':
    main()
