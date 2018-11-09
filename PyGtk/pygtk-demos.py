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

# TODO:
# Trying to connect Demos with the PyGTK Tutorial and RefMan
# for a Cherrytree and Zim-Wiki Developer-Sandbox
# implement hyperlinks
# implement code-fork and save changes
# implement bracket matching and autocomplete
# implement code folding
# implement a tutorial assistent where demos are in a pedagogical order
# add exercises

# add cherrytree and zim demos

# Check if fallback font is needed.

import string
import re
import pygtk
pygtk.require('2.0')
import gobject
import gtk
import pango
import gtksourceview2

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

    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title("PyGTK and Friends")
        self.connect('destroy', lambda w: gtk.main_quit())
        self.set_default_size(800, 400)

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
        # scrolled_window, self.info_buffer = self.__create_text(False)

        # INFO BUFFER
        scrolled_window, self.info_buffer = self.__create_text(False)
        self._new_notebook_page(scrolled_window, '_Info')
        tag = self.info_buffer.create_tag('title')
        tag.set_property('font', 'Inconsolata 18')

        # SOURCE BUFFER
        scrolled_window, self.source_buffer = self.__create_text(True)
        self._new_notebook_page(scrolled_window, '_Source')
        tag = self.source_buffer.create_tag('source')
        tag.set_property('font', 'Inconsolata 18')
        # tag = self.source_buffer.create_tag('source')
        # tag.set_property('font', 'monospace')
        # tag.set_property('pixels_above_lines', 0)
        # tag.set_property('pixels_below_lines', 0)
        # tag = self.source_buffer.create_tag('keyword', foreground='#00007F',\
        #     weight=pango.WEIGHT_BOLD)
        # tag = self.source_buffer.create_tag('string', foreground='#7F007F')
        # tag = self.source_buffer.create_tag('comment', foreground='#007F00',
        #     style=pango.STYLE_ITALIC)

        self.show_all()

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
        # scrolled window
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.set_shadow_type(gtk.SHADOW_IN)

        # sourceview
        buffer = gtksourceview2.Buffer(None)
        text_view = gtksourceview2.View(buffer)
        scrolled_window.add(text_view)

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

    def window_closed_cb (self, window, model, path):
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
    print "PyGTK Demos",
    print "(gtk: v%d.%d.%d, " % gtk.gtk_version,
    print "pygtk: v%d.%d.%d)" % gtk.pygtk_version
    PyGtkDemo().run()
