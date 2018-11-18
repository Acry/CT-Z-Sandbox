#!/usr/bin/env python2
'''
  $Id$

  pygtk-demo.py
  2004-07-18:   Some enhancements for building the list of demos like in gtk-demos of the
                gtk+ distribution.

  2004-07-22:   Simple syntax highlighting implemented, based on the tokenizer-module.
  2018-10-22:   Switched plain TextView with SourceHighlight.
                Added panning
                Added some educational valuable Demos
                Push to github
                (Carsten Holtkamp)
'''

# Trying to connect Demos from PyGTK Tutorial, FAQ, RefMan and
#   several other resources to have a decent demo/recipe-pool
# for a CherryTree and Zim-Wiki Developer-Sandbox

# TODO:
# Browsing Visual/Usability:
# add index
# add widget list
# tag inline code in Info Buffer
# add screenshots (preview images) to Info Buffer
# add intro/contents page on expander
# switch to treestore and save Node relationship in sqlite
# use closure tables

# Bugs - not intended behaviour:
# distinct clickable tags, since I have 2 now - inline code should't be clickable

# Coding abilities:
# implement code-fork and save changes
# implement bracket matching and autocomplete
# implement code folding
# implement a tutorial assistant where demos are in a pedagogical order
# add exercises

# Content:
# add CherryTree and Zim demos
# add sqlite demos
# add more cairo demos
# add pango demos
# add gdk color examples and value range scaling aka normalization
# demos from http://zetcode.com/gui/pygtk
# demos from https://www.kksou.com/php-gtk2/category/Sample-Codes/
# add widget-factory

import string
import re
import pygtk
pygtk.require('2.0')
import gobject
import gtk
import pango
import gtksourceview2
import webbrowser
import platform
import os
import demos
D_TEMPL = '%sDemo'
# Some programmatic definition for the testgtk_demos list.
#
# This avoids extra maintenance if the demo list grows up.
# The current definition requires # a class or function with
# a swapped case name+'Demo' like in the doc string.

# Swapped case is build from the __doc__-string programatically.

child_demos = {}
testgtk_demos = []
LINKLIST = []
SEARCH_STRINGS = ["https://",  "http://"]
NEWLINE_CHAR = "\n"

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'demos/images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
IMAGE = "squares2.png"
MAIN_IMAGE = os.path.join(IMAGEDIR, IMAGE)

for descr, mod in demos.demo_list:
    # Find some categorized demos
    try:
        main, child = descr.split('/')
    except ValueError:
        # No, only one application
        demo_class = D_TEMPL % re.sub('(\S+) *',
            lambda m:(m.group(1)[0].isupper() and m.group(1) or m.group(1).capitalize()),
            descr)
        testgtk_demos.append((descr, mod, demo_class))
    else:
        # Ok. Some more testing
        demo_class = D_TEMPL % re.sub('(\S+) *',
            lambda m:(m.group(1)[0].isupper() and m.group(1) or m.group(1).capitalize()),
            child)
        try:
            # Applicationgroup already defined?
            child_demos[main.upper()].append((child, mod, demo_class))
        except KeyError:
            # No. Start a new category
            child_demos.setdefault(main.upper(), []).append((child, mod, demo_class))
            testgtk_demos.append((main, None, None, child_demos[main.upper()]))

(
   TITLE_COLUMN,
   MODULE_COLUMN,
   FUNC_COLUMN,
   ITALIC_COLUMN
) = range(4)

CHILDREN_COLUMN = 3

class InputStream(object):
    ''' Simple Wrapper for File-like objects. [c]StringIO doesn't provide
        a readline function for use with generate_tokens.
        Using a iterator-like interface doesn't succeed, because the readline
        function isn't used in such a context. (see <python-lib>/tokenize.py)
    '''

    def __init__(self, data):
        self.__data = [ '%s\n' % x for x in data.splitlines() ]
        self.__lcount = 0

    def readline(self):
        try:
            line = self.__data[self.__lcount]
            self.__lcount += 1
        except IndexError:
            line = ''
            self.__lcount = 0
        return line


class PyGtkDemo(gtk.Window):
    info_buffer = None
    source_buffer = None
    module_cache  = {}

    hovering_over_link = False
    hand_cursor = gtk.gdk.Cursor(gtk.gdk.HAND2)
    regular_cursor = gtk.gdk.Cursor(gtk.gdk.XTERM)
    def key_press_event(self, text_view, event):
        if (event.keyval == gtk.keysyms.Return or
            event.keyval == gtk.keysyms.KP_Enter):
            buffer = text_view.get_buffer()
            iter = buffer.get_iter_at_mark(buffer.get_insert())
            self.follow_if_link(text_view, iter)
        return False

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

    def motion_notify_event(self, text_view, event):
        x, y = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET,
            int(event.x), int(event.y))
        self.set_cursor_if_appropriate(text_view, x, y)
        text_view.window.get_pointer()
        return False

    def visibility_notify_event(self, text_view, event):
        wx, wy, mod = text_view.window.get_pointer()
        bx, by = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET, wx, wy)
        self.set_cursor_if_appropriate (text_view, bx, by)
        return False

    def inlinecode_markup(self):
        buffer = self.info_buffer
        visibility_tag = buffer.create_tag(None, invisible=True)
        tag = buffer.create_tag(None, background="lightgrey", background_full_height=True, style=pango.STYLE_OBLIQUE,\
                                font="Inconsolta", size_points=10)
        tag_string = "`"
        start, end = buffer.get_bounds()
        tag_start = None
        tag_end = None
        searching = True
        count = 0
        while searching:
            try:
                match_start, match_end = start.forward_search(tag_string, gtk.TEXT_SEARCH_TEXT_ONLY, limit=None)
                if not count % 2:
                    # first
                    tag_start = match_start.copy()
                    tag_start.forward_char()
                else:
                    # second
                    tag_end = match_end.copy()
                    tag_end.backward_char()
                    buffer.apply_tag(tag, tag_start, tag_end)
                buffer.apply_tag(visibility_tag, match_start, match_end)
                start = match_end
                count = count + 1
            except:
                searching = False

    def check_links(self, search_string):
        global LINKLIST
        buffer = self.info_buffer
        start, end = buffer.get_bounds()
        tag = buffer.create_tag(None, foreground="blue", underline=pango.UNDERLINE_SINGLE)
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
                LINKLIST.append([(tag_start, match_end), text])
                start = match_end
                match_end.forward_char()
                count = count + 1

    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title("PyGTK and Friends")
        self.connect('destroy', lambda w: gtk.main_quit())
        self.set_default_size(800, 400)
        self.set_icon_from_file(ICON_IMAGE)
        hbox = gtk.HBox(False, 3)
        self.add(hbox)
        
        hpaned = gtk.HPaned()
        hpaned.set_border_width(5)
        hbox.pack_start(hpaned, True, True)

        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        hpaned.add1(sw)
        treeview = self.__create_treeview()
        sw.add(treeview)
        self.notebook = gtk.Notebook()

        hpaned.add2(self.notebook)
        self.notebook.realize()

        # INFO BUFFER
        scrolled_window, self.info_buffer = self.__create_text(False)
        self._new_notebook_page(scrolled_window, '_Info')
        tag = self.info_buffer.create_tag('title')
        tag.set_property('font', 'Indie Flower 18')

        # SOURCE BUFFER
        scrolled_window, self.source_buffer = self.__create_text(True)
        self._new_notebook_page(scrolled_window, '_Source')
        tag = self.source_buffer.create_tag('source')
        tag.set_property('font', 'Inconsolata 18')

        self.show_all()
        nb_childs = self.notebook.get_children()
        sw_childs = nb_childs[0].get_children()
        sw_childs[0].realize()
        pixbuf = gtk.gdk.pixbuf_new_from_file(MAIN_IMAGE)
        pixmap, mask = pixbuf.render_pixmap_and_mask()
        tvwindow = sw_childs[0].get_window(gtk.TEXT_WINDOW_TEXT)
        tvwindow.set_back_pixmap(pixmap, gtk.FALSE)

    def run(self):
        gtk.main()

    def _new_notebook_page(self, widget, label):
        l = gtk.Label('')
        l.set_text_with_mnemonic(label)
        self.notebook.append_page(widget, l)

    def __create_treeview(self):
        model = gtk.TreeStore(
            gobject.TYPE_STRING,
            gobject.TYPE_STRING,
            gobject.TYPE_STRING,
            gobject.TYPE_BOOLEAN
        )

        treeview = gtk.TreeView(model)
        selection = treeview.get_selection()
        selection.set_mode(gtk.SELECTION_BROWSE)
        treeview.set_size_request(200, -1)

        for module in testgtk_demos:
            iter = model.append(None)
            model.set(iter,
                TITLE_COLUMN, module[TITLE_COLUMN],
                MODULE_COLUMN, module[MODULE_COLUMN],
                FUNC_COLUMN, module[FUNC_COLUMN],
                ITALIC_COLUMN, False
            )

            try:
                children = module[CHILDREN_COLUMN]
                for child_module in children:
                    child_iter = model.append(iter)
                    model.set(child_iter,
                        TITLE_COLUMN, child_module[TITLE_COLUMN],
                        MODULE_COLUMN, child_module[MODULE_COLUMN],
                        FUNC_COLUMN, child_module[FUNC_COLUMN],
                        ITALIC_COLUMN, False
                    )
            except IndexError:
                pass

        cell = gtk.CellRendererText()
        cell.set_property('style', pango.STYLE_ITALIC)

        column = gtk.TreeViewColumn("Double click for demo.", cell,
            text=TITLE_COLUMN, style_set=ITALIC_COLUMN)

        treeview.append_column(column)

        selection.connect('changed', self.selection_changed_cb)
        treeview.connect('row-activated', self.row_activated_cb)

        # treeview.expand_all()

        return treeview

    def __create_text(self, is_source=False):
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.set_shadow_type(gtk.SHADOW_IN)

        buffer = gtksourceview2.Buffer(None)
        text_view = gtksourceview2.View(buffer)
        scrolled_window.add(text_view)
        if not is_source:
            # context = text_view.get_pango_context()
            # fonts = context.list_families()
            # for font in fonts:
            #     print font.get_name()
            font = pango.FontDescription('Indie Flower 14')
            text_view.modify_font(font)
            text_view.connect("key-press-event", self.key_press_event)
            text_view.connect("event-after", self.event_after)
            text_view.connect("motion-notify-event", self.motion_notify_event)
            text_view.connect("visibility-notify-event", self.visibility_notify_event)

        return scrolled_window, buffer

    def row_activated_cb(self, treeview, path, column):
        model = treeview.get_model()
        iter  = model.get_iter(path)
        module_name  = model.get_value(iter, MODULE_COLUMN)
        func_name    = model.get_value(iter, FUNC_COLUMN)
        italic_value = model.get_value(iter, ITALIC_COLUMN)
        if module_name is None:  # a "category" row is activated
            return True
        print "%s.py" % module_name
        try:
            self.module_cache[module_name].present()
        except KeyError:
            module = getattr(demos, module_name)
            model.set(iter, ITALIC_COLUMN, not italic_value)
            cmd = 'demos.%s.%s' % (module_name, func_name)
            window = eval(cmd)(self)
            if window:
                window.connect('destroy', self.window_closed_cb, model, path)
                self.module_cache[module_name] = window

    def selection_changed_cb(self, selection):
        model, iter = selection.get_selected()
        if not iter:
            return False

        name = model.get_value(iter, MODULE_COLUMN)
        if name is not None:
            self.load_module(name)

    def window_closed_cb(self, window, model, path):
        iter = model.get_iter(path)
        module_name  = model.get_value(iter, MODULE_COLUMN)
        del self.module_cache[module_name]
        italic_value = model.get_value(iter, ITALIC_COLUMN)
        if italic_value:
            model.set(iter, ITALIC_COLUMN, not italic_value)

    def read_module(self, module):
        filename = module.__file__
        if filename[-4:] == '.pyc':
            filename = filename[:-1]
        fd = open(filename)
        return fd.read()

    def insert_documentation(self, module):
        path = module.__file__
        basename = os.path.basename(path)
        filename = os.path.splitext(basename)[0]
        print filename
        buffer = self.info_buffer
        iter = buffer.get_iter_at_offset(0)

        lines = string.split(module.__doc__ or '', '\n')
        buffer.insert(iter, lines[0])
        start = buffer.get_iter_at_offset(0)
        buffer.apply_tag_by_name('title', start, iter)
        buffer.insert(iter, '\n')
        for line in lines[1:]:
            buffer.insert(iter, line)
            buffer.insert(iter, '\n')
        self.inlinecode_markup()
        global SEARCH_STRINGS
        for entry in SEARCH_STRINGS:
            self.check_links(entry)
        try:
            SCREENSHOT = "demos/" + filename + ".png"
            print SCREENSHOT
            pixbuf = gtk.gdk.pixbuf_new_from_file(SCREENSHOT)
            # pixbuf = pixbuf.scale_simple(200, 200, gtk.gdk.INTERP_BILINEAR)
            enditer = buffer.get_end_iter()
            buffer.insert_pixbuf(enditer, pixbuf)
        except:
            pass

    def clear_buffers(self):
        start, end = self.info_buffer.get_bounds()
        self.info_buffer.delete(start, end)

        start, end = self.source_buffer.get_bounds()
        self.source_buffer.delete(start, end)

    def insert_source(self, data):
        self.source_buffer.set_text(data)
        foo = gtksourceview2.LanguageManager()
        id = foo.get_language('python')
        self.source_buffer.set_language(id)
        self.source_buffer.set_highlight_syntax(True)

    def load_module(self, name):
        self.clear_buffers()
        module = getattr(demos, name)
        if module.__doc__:
            self.insert_documentation(module)

        source = self.read_module(module)
        self.insert_source(source)


if __name__ == '__main__':
    print "PyGTK Demos - ",
    print "Python: V%s, " % platform.python_version(),
    print "GTK+: V%d.%d.%d, " % gtk.gtk_version,
    print "PyGTK: v%d.%d.%d" % gtk.pygtk_version

    PyGtkDemo().run()
