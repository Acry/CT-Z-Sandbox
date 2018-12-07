#!/usr/bin/env python2
'''NoteBook/NoteBook Complex

The NoteBook Widget is a collection of "pages" that overlap each other; each page contains different information with only one page visible at a time. This widget has become more common lately in GUI programming, and it is a good way to show blocks of similar information that warrant separation in their display.

The first function call you will need to know, as you can probably guess by now, is used to create a new notebook widget.

  `notebook = gtk.Notebook()`
'''
import pygtk

pygtk.require('2.0')
import gtk


class NoteBookComplexDemo(gtk.Window):
    # This method rotates the position of the tabs
    def rotate_book(self, button, notebook):
        notebook.set_tab_pos((notebook.get_tab_pos() + 1) % 4)

    # Add/Remove the page tabs and the borders
    def tabsborder_book(self, button, notebook):
        tval = False
        bval = False
        if self.show_tabs == False:
            tval = True
        if self.show_border == False:
            bval = True

        notebook.set_show_tabs(tval)
        self.show_tabs = tval
        notebook.set_show_border(bval)
        self.show_border = bval

    # Remove a page from the notebook
    def remove_book(self, button, notebook):
        page = notebook.get_current_page()
        notebook.remove_page(page)
        # Need to refresh the widget --
        # This forces the widget to redraw itself.
        notebook.queue_draw_area(0, 0, -1, -1)

    def delete(self, widget, event=None):
        gtk.main_quit()
        return False

    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_border_width(10)
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.connect("delete_event", self.delete)

        table = gtk.Table(3, 6, False)
        window.add(table)

        # Create a new notebook, place the position of the tabs
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        table.attach(notebook, 0, 6, 0, 1)
        notebook.show()
        self.show_tabs = True
        self.show_border = True

        # Let's append a bunch of pages to the notebook
        for i in range(5):
            bufferf = "Append Frame %d" % (i + 1)
            bufferl = "Page %d" % (i + 1)

            frame = gtk.Frame(bufferf)
            frame.set_border_width(10)
            frame.set_size_request(100, 75)
            frame.show()

            label = gtk.Label(bufferf)
            frame.add(label)
            label.show()

            label = gtk.Label(bufferl)
            notebook.append_page(frame, label)

        # Now let's add a page to a specific spot
        checkbutton = gtk.CheckButton("Check me please!")
        checkbutton.set_size_request(100, 75)
        checkbutton.show()

        label = gtk.Label("Add page")
        notebook.insert_page(checkbutton, label, 2)

        # Now finally let's prepend pages to the notebook
        for i in range(5):
            bufferf = "Prepend Frame %d" % (i + 1)
            bufferl = "PPage %d" % (i + 1)

            frame = gtk.Frame(bufferf)
            frame.set_border_width(10)
            frame.set_size_request(100, 75)
            frame.show()

            label = gtk.Label(bufferf)
            frame.add(label)
            label.show()

            label = gtk.Label(bufferl)
            notebook.prepend_page(frame, label)

        # Set what page to start at (page 4)
        notebook.set_current_page(3)

        # Create a bunch of buttons
        button = gtk.Button("close")
        button.connect("clicked", self.delete)
        table.attach(button, 0, 1, 1, 2)
        button.show()

        button = gtk.Button("next page")
        button.connect("clicked", lambda w: notebook.next_page())
        table.attach(button, 1, 2, 1, 2)
        button.show()

        button = gtk.Button("prev page")
        button.connect("clicked", lambda w: notebook.prev_page())
        table.attach(button, 2, 3, 1, 2)
        button.show()

        button = gtk.Button("tab position")
        button.connect("clicked", self.rotate_book, notebook)
        table.attach(button, 3, 4, 1, 2)
        button.show()

        button = gtk.Button("tabs/border on/off")
        button.connect("clicked", self.tabsborder_book, notebook)
        table.attach(button, 4, 5, 1, 2)
        button.show()

        button = gtk.Button("remove page")
        button.connect("clicked", self.remove_book, notebook)
        table.attach(button, 5, 6, 1, 2)
        button.show()

        table.show()
        window.show()

    def main(self):
        gtk.main()


def main():
    NoteBookComplexDemo()
    gtk.main()

if __name__ == '__main__':
    main()