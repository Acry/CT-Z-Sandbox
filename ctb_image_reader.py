#!/usr/bin/env python2

"""Read and show png from from Cherrytree sqlite db (ctb).
call with ctb.
ctb_image_reader example.ctb
navigate with arrow keys:
left/right step for/back
up first entry
down last entry
"""
# TODO
# browse thumbnails
# fix handling if anchor entry
# export

import pygtk

pygtk.require('2.0')
import gtk
import os
import sys

# region Init and DB read
# Cherrytree uses the sqlite3 module, so it's a bit different here as I use apsw
# see: https://github.com/rogerbinns/apsw
# See: http://www.sqlitetutorial.net/sqlite-python/
# for convenience sqlite import usage added

db_handler = None

import apsw
if 'apsw' in sys.modules:
    db_handler = "apsw"
else:
    import sqlite3
    if 'sqlite3' in sys.modules:
        db_handler = "sqlite3"

if not db_handler:
    print "either module apsw sqlite3 needed"
    sys.exit()

print db_handler


try:
    file_name = sys.argv[1]
    if not file_name.lower().endswith('.ctb'):
        raise Exception('file has the wrong extension')
except:
    print "provide a CTB"
    sys.exit()

print "Reading", file_name, "- hang on"
if db_handler == "apsw":
    connection = apsw.Connection(file_name)
else:
    connection = sqlite3.connect(file_name)

cursor = connection.cursor()
SQL_STATEMENT = "SELECT png, node_id, filename FROM image"
cursor.execute(SQL_STATEMENT)
entries = cursor.fetchall()
count = len(entries)
print count
pointer = count
data = entries[0][0]
node = entries[0][1]
filename = entries[0][2]
if db_handler == "apsw":
    cursor.execute("SELECT name FROM node WHERE node_id=?", {node})
else:
    cursor.execute("SELECT name FROM node WHERE node_id=?", (node,))
name = cursor.fetchone()[0]


TITLE = 'CherryTree CTB Image Viewer'
IMAGE_DIR = ""
ICON_IMAGE = os.path.join(IMAGE_DIR, 'cherrytree_icon.png')

# endregion
# not used for export so far
def writeImage(data):
    try:
        fout = open('test.png', 'wb')
        fout.write(data)

    except IOError, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if fout:
            fout.close()

class Base:
    def _key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        keyval = event.keyval
        keyval_name = gtk.gdk.keyval_name(keyval)
        state = event.state
        ctrl = (state & gtk.gdk.CONTROL_MASK)
        global pointer
        global count
        if event.keyval == 65361:  # left
            pointer = pointer - 1
            if pointer < 0:
                pointer = count-1
        if event.keyval == 65362:  # up
            pointer = count-1
        if event.keyval == 65363:  # right
            pointer = pointer + 1
            if pointer > count-1:
                pointer = 0
        if event.keyval == 65364:  # down
            pointer = 0
        print "Entry number:", pointer+1
        self.read_entry()

    def read_entry(self):
        global pointer
        global entries
        global data
        global filename
        data = entries[pointer][0]
        node = entries[pointer][1]
        filename = entries[pointer][2]
        if db_handler == "apsw":
            cursor.execute("SELECT name FROM node WHERE node_id=?", {node})
        else:
            cursor.execute("SELECT name FROM node WHERE node_id=?", (node,))
        name = cursor.fetchone()[0]
        print "In", name, "with Node-ID:", node
        if not data or filename:
            print "it is an anchor or png from file, not supported yet"
            return
        self.readImage()

    def readImage(self):
        pixbuf_loader = gtk.gdk.pixbuf_loader_new_with_mime_type("image/png")
        # fill with data
        global data
        pixbuf_loader.write(data)
        # release loader
        pixbuf_loader.close()
        # define pixbuf
        pixbuf = pixbuf_loader.get_pixbuf()
        # copy of original data for scaling
        self.pixbuf_org = pixbuf.copy()
        self.org_width = pixbuf.get_width()
        self.org_height = pixbuf.get_height()
        # get image ratio
        image_ratio = float(self.org_width) / float(self.org_height)
        # get window ratio
        window_ratio = float(self.old_width) / float(self.old_height)

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
        self.image.set_from_pixbuf(pixbuf)

    def on_exit(self, widget):
        connection.close(True)
        gtk.main_quit()

    def main(self):
        gtk.main()

    def scale(self, window, image, image_ratio, pixbuf):
        allocation = window.get_allocation()
        if self.old_height != allocation.height or self.old_width != allocation.width:
            ww = window.get_allocation().width
            wh = window.get_allocation().height
            window_ratio = float(ww) / float(wh)
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

    def __init__(self):
        self.old_width = 400
        self.old_height = 300

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(TITLE)
        self.window.set_default_size(self.old_width, self.old_height)
        self.window.set_icon_from_file(ICON_IMAGE)
        self.window.set_geometry_hints(min_width=100, min_height=100)
        self.window.connect('destroy', self.on_exit)
        vb = gtk.VBox()
        self.window.add(vb)
        # region IMAGE
        # prepare pixel buffer
        pixbuf_loader = gtk.gdk.pixbuf_loader_new_with_mime_type("image/png")
        # fill with data
        pixbuf_loader.write(data)
        # release loader
        pixbuf_loader.close()
        # define pixbuf
        pixbuf = pixbuf_loader.get_pixbuf()
        # copy of original data for scaling
        self.pixbuf_org = pixbuf.copy()
        self.org_width = pixbuf.get_width()
        self.org_height = pixbuf.get_height()
        self.image = gtk.Image()

        # get image ratio
        image_ratio = float(self.org_width) / float(self.org_height)

        # get window ratio
        window_ratio = float(self.old_width) / float(self.old_height)

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
        self.image.set_from_pixbuf(pixbuf)
        # endregion
        aspect_frame = gtk.AspectFrame(obey_child=True)
        vb.pack_start(aspect_frame, True, False)
        # drawing_area = gtk.DrawingArea()
        aspect_frame.add(self.image)
        self.window.connect('check-resize', self.scale, self.image, image_ratio, pixbuf)
        message = "Node ID:" + str(node) + " \"" + name + "\""
        self.tooltips = gtk.Tooltips()
        self.tooltips.set_tip(self.image, message)
        self.window.connect("key-press-event", self._key_press_event)
        self.window.show_all()


if __name__ == "__main__":
    base = Base()
    base.main()
