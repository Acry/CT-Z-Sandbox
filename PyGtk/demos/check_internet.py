#!/usr/bin/env python2
"""Check Git

Checks internet connection and repository head.
`CHECK_TIME` is every `10` minutes.
You get green light if remote and local head are equal.
Red if you aren't online and a yellowisch color if you are connected but heads differ.
If you press the git button it calls a `git pull`.
"""

# TODO: Probably I should just switch the "image" not the whole widget.
#       But then I have to update the tooltip either.

import gtk
import socket
import gobject
import datetime
import pygtk
import subprocess
import os

pygtk.require('2.0')
IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')

ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
GIT_IMAGE = os.path.join(IMAGEDIR, 'Git-Logo-Black.svg')
BUTTON_RED = os.path.join(IMAGEDIR, 'Button-Red.svg')
BUTTON_ORANGE = os.path.join(IMAGEDIR, 'Button-Yellow.svg')
BUTTON_GREEN = os.path.join(IMAGEDIR, 'Button-Green.svg')

REMOTE_SERVER = "www.google.com"
CHECK_TIME = 1000 * 60 * 10  # 1000 ms * 60 seconds * 10 minutes


class CheckGitDemo(gtk.Window):
    def is_connected(self):
        gobject.source_remove(self.timer)
        try:
            host = socket.gethostbyname(REMOTE_SERVER)
            s = socket.create_connection((host, 80), 2)
            connected = True
            self.tbbox.remove(self.image3)
            self.tbbox.remove(self.toolbar)
            self.tbbox.pack_end(self.image2, False, False)
            self.tbbox.pack_end(self.toolbar, False, False)
            self.image2.show()
        except:
            connected = False
            self.git_button.set_sensitive(False)
        print datetime.datetime.now().time()
        if connected:
            try:
                local_head = subprocess.check_output(['git', 'rev-parse', '@'])
                local_head = local_head.rstrip()
                # FIXME: find a solution for shh/git
                remote_head = subprocess.check_output(['git', 'ls-remote', 'https://github.com/Acry/CT-Z-Sandbox.git'])
                remote_head = remote_head.split()
                remote_head = remote_head[0]
                if remote_head == local_head:
                    self.tbbox.remove(self.image2)
                    self.tbbox.remove(self.toolbar)
                    self.tbbox.pack_end(self.image, False, False)
                    self.tbbox.pack_end(self.toolbar, False, False)
                    self.image.show()
                    self.git_button.set_sensitive(False)
            except:
                self.git_button.set_sensitive(True)
        self.timer = gobject.timeout_add(CHECK_TIME, self.is_connected)

    def git(self, something):
        try:
            status = subprocess.check_output("git pull", shell=True, stderr=subprocess.STDOUT)
            dialog = gtk.MessageDialog(self, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                                       gtk.BUTTONS_CLOSE, status)
            dialog.run()
            dialog.destroy()
        except subprocess.CalledProcessError as e:
            dialog = gtk.MessageDialog(self, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR,
                                       gtk.BUTTONS_CLOSE, e.output)
            dialog.run()
            dialog.destroy()
            raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_icon_from_file(ICON_IMAGE)
        self.tbbox = gtk.HBox(False)
        self.tbbox.set_border_width(12)
        self.add(self.tbbox)

        self.toolbar = gtk.Toolbar()
        self.toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        self.toolbar.set_style(gtk.TOOLBAR_ICONS)

        # git button
        iconw = gtk.Image()  # icon widget
        iconw.set_from_file(GIT_IMAGE)
        self.git_button = self.toolbar.append_item(
            "git pull",
            "get latest version",
            "Private",
            iconw,
            self.git)
        self.git_button.set_size_request(80, 34)
        self.image = gtk.Image()
        self.image.set_from_file(BUTTON_GREEN)
        self.image.set_tooltip_text("Connected and up to date.")

        self.image2 = gtk.Image()
        self.image2.set_from_file(BUTTON_ORANGE)
        self.image2.set_tooltip_text("Connected and not up to date.")

        self.image3 = gtk.Image()
        self.image3.set_from_file(BUTTON_RED)
        self.image3.set_tooltip_text("Not connected.")

        self.tbbox.pack_end(self.image3, False, False)
        self.tbbox.pack_end(self.toolbar, False, False)

        self.timer = gobject.timeout_add(1000, self.is_connected)
        self.show_all()


if __name__ == '__main__':
        CheckGitDemo()
        gtk.main()
