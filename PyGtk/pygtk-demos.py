#!/usr/bin/env python2
#region Description
"""
Cherrytree and Zim kinda SDK (work in progress)
Cherrytree & Zim - A Desktop Wiki
Python 2 with GTK+ 2 and friends...

Repository:
https://github.com/Acry/CT-Z-Sandbox

Trying to connect Demos from PyGTK Tutorial, FAQ, RefMan and
several other resources to have a decent demo/recipe-pool
for a CherryTree and Zim-Wiki Developer-Sandbox.

based on pygtk-demo, demos from http://zetcode.com/gui/pygtk
demos from https://www.kksou.com/php-gtk2/category/Sample-Codes/
"""
#endregion

# region Milestones
"""
  $Id$

  pygtk-demo.py
  2004-07-18:   Some enhancements for building the list of demos like in gtk-demos of the
                gtk+ distribution.

  2004-07-22:   Simple syntax highlighting implemented, based on the tokenizer-module.
  2018-10-22:   Switched plain TextView with SourceHighlight - made that simple syntax highlighting obsolete.
                Added panning.
                Added some educational valuable Demos.
                Push to github, view commits for history
                (Carsten Holtkamp)
"""
# endregion

# region OUTLINE / ROADMAP:
# Browsing Visual/Usability:
# save last used page/module
# internal links to different demos.
# add index
# add widget list
# tag inline code in Info Buffer
# switch to treestore and save node relationship in sqlite
#   use closure tables
# remove info from the source buffer (make hidden)?
#   think it is better to seperate description
# l10N/I18N
# implement a tutorial assistant where demos are in a pedagogical order
# add exercises
# show new commits
# allow particular depth of sub-categories
#
# Theming:
# -> gtk-theme-switch2
# rc-files
# https://www.gnome-look.org/browse/cat/136/
# CSS is GTK+3
#
# widget factory:
# https://github.com/valr/awf
# https://www.jasong-designs.com/2015/05/28/how-to-install-a-widget-factory-in-linux/
# https://www.gnome-look.org/p/1115124/

# Long term:
# thinking of clutter integration, but it looks bad.
#   since finding a working version failed for now

# Bugs: - not intended behaviour:
# distinct clickable tags, since I have 2 now - inline code should't be clickable
# FIXME: don't use anonymous tags
# Refactor Notebook/Scrolled window for Notes/sources/cat/intro/toc after SQLite closure table

# Coding abilities:
# implement code-fork and save changes
# implement bracket matching and autocomplete
# implement code folding

# Content:
# add CherryTree and Zim demos
# add cairo demos
# add pango demos
# add gdk color examples and value range scaling aka normalization
# add item-factory (deprecated)
#   gtk.ItemFactory is deprecated in PyGTK 2.4 and above, gtk.UIManager should be used instead.
# add custom widget
# tables - Weighting on a table
# add python 2 category
# have a diff between fork and base
# endregion

# region imports
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
import subprocess
import datetime
import socket
#endregion

# region globals and constants
child_demos = {}
testgtk_demos = []
LINKLIST = []
SEARCH_STRINGS = ["https://", "http://"]
NEWLINE_CHAR = "\n"

DEMODIR = os.path.join(os.path.dirname(__file__), "demos")
IMAGEDIR = os.path.join(DEMODIR, 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')

GIT_IMAGE = os.path.join(IMAGEDIR, "Git-Logo-Black.svg")
REMOTE_SERVER = "www.google.com"  # for checking online status
CHECK_TIME = 1000 * 60 * 60  # checking every hour
BUTTON_RED = os.path.join(IMAGEDIR, 'Button-Red.svg')
BUTTON_ORANGE = os.path.join(IMAGEDIR, 'Button-Yellow.svg')
BUTTON_GREEN = os.path.join(IMAGEDIR, 'Button-Green.svg')

MAIN_IMAGE = os.path.join(IMAGEDIR, "squares2.png")
TITLE = os.path.join(DEMODIR, "title.txt")
TITLE_ACTIVE = False
category = []  # not used right now, even so it is filled
# todo bring fonts here
# endregion

# region Some programmatic definition for the demo list.
D_TEMPL = '%sDemo'

#
# This avoids extra maintenance if the demo list grows up.
# The current definition requires # a class or function with
# a swapped case name+'Demo' like in the doc string.
# Swapped case is build from the __doc__-string programatically.
for descr, mod in demos.demo_list:
    # Find some categorized demos
    try:
        main, child = descr.split('/')
        if main not in category:
            category.append(main)
    except ValueError:
        # No, only one application
        demo_class = D_TEMPL % re.sub('(\S+) *',
                                      lambda m: (m.group(1)[0].isupper() and m.group(1) or m.group(1).capitalize()),
                                      descr)
        testgtk_demos.append((descr, mod, demo_class))
    else:
        # Ok. Some more testing
        demo_class = D_TEMPL % re.sub('(\S+) *',
                                      lambda m: (m.group(1)[0].isupper() and m.group(1) or m.group(1).capitalize()),
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


# print category
# endregion

class InputStream(object):
    """ Simple Wrapper for File-like objects. [c]StringIO doesn't provide
        a readline function for use with generate_tokens.
        Using a iterator-like interface doesn't succeed, because the readline
        function isn't used in such a context. (see <python-lib>/tokenize.py)
    """

    def __init__(self, data):
        self.__data = ['%s\n' % x for x in data.splitlines()]
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
    module_cache = {}
    hovering_over_link = False
    hand_cursor = gtk.gdk.Cursor(gtk.gdk.HAND2)
    regular_cursor = gtk.gdk.Cursor(gtk.gdk.XTERM)

    def is_connected(self):
        gobject.source_remove(self.timer)
        try:
            host = socket.gethostbyname(REMOTE_SERVER)
            s = socket.create_connection((host, 80), 2)
            connected = True
            self.tbbox.remove(self.image3)
            self.tbbox.remove(self.toolbar_r)
            self.tbbox.pack_end(self.image2, False, False)
            self.tbbox.pack_end(self.toolbar_r, False, False)
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
                    self.tbbox.remove(self.toolbar_r)
                    self.tbbox.pack_end(self.image, False, False)
                    self.tbbox.pack_end(self.toolbar_r, False, False)
                    self.image.show()
                    self.git_button.set_sensitive(False)
            except:
                self.git_button.set_sensitive(True)
        self.timer = gobject.timeout_add(CHECK_TIME, self.is_connected)

    def key_press_event(self, text_view, event):
        """method help"""
        if event.keyval == gtk.keysyms.Return or event.keyval == gtk.keysyms.KP_Enter:
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
        self.set_cursor_if_appropriate(text_view, bx, by)
        return False

    def inlinecode_markup(self):
        buffer = self.info_buffer
        visibility_tag = buffer.create_tag(None, invisible=True)
        tag = buffer.create_tag(None, background="lightgrey", background_full_height=True, style=pango.STYLE_OBLIQUE, \
                                font="Inconsolta", size_points=12)
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
                enter_start, enter_end = next_enter.forward_search(NEWLINE_CHAR, gtk.TEXT_SEARCH_VISIBLE_ONLY,
                                                                   limit=None)
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

    def git(self, something):
        status = None
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
        print status

    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title("PyGTK and Friends")
        self.connect('destroy', lambda w: gtk.main_quit())
        self.set_default_size(950, 750)
        self.set_icon_from_file(ICON_IMAGE)

        vbox = gtk.VBox(False, 3)
        self.add(vbox)
        self.tbbox = gtk.HBox(False)
        self.tbbox.set_border_width(12)
        vbox.pack_start(self.tbbox, False, False)

        # toolbar_l
        self.toolbar_l = gtk.Toolbar()
        self.toolbar_l.set_style(gtk.TOOLBAR_ICONS)
        self.toolbar_l.set_border_width(4)
        self.toolbar_l.show()

        self.tbbox.pack_start(self.toolbar_l, False, False)
        iconw = gtk.Image()  # icon widget
        iconw.set_from_file(GIT_IMAGE)
        iconw.set_from_stock(gtk.STOCK_HOME, gtk.ICON_SIZE_LARGE_TOOLBAR)
        self.home_button = self.toolbar_l.append_item(
            "home",
            "direct to title",
            "Private",
            iconw,
            self.show_title)
        self.home_button.set_sensitive(False)
        # toolbar_r
        self.toolbar_r = gtk.Toolbar()
        self.toolbar_r.set_style(gtk.TOOLBAR_ICONS)
        self.toolbar_r.set_border_width(4)
        self.toolbar_r.show()

        # git button
        iconw = gtk.Image()  # icon widget
        iconw.set_from_file(GIT_IMAGE)
        self.git_button = self.toolbar_r.append_item(
            "git pull",
            "get latest version",
            "Private",
            iconw,
            self.git)
        self.git_button.set_size_request(80, 34)
        self.git_button.set_sensitive(False)

        self.hpaned = gtk.HPaned()
        self.hpaned.set_border_width(5)
        vbox.pack_start(self.hpaned, True, True)
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.hpaned.add1(sw)

        treeview = self.__create_treeview()
        sw.add(treeview)
        self.notebook = gtk.Notebook()
        self.hpaned.add2(self.notebook)
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

        # Category toc
        self.scrolled_window_toc = gtk.ScrolledWindow()
        self.scrolled_window_toc.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scrolled_window_toc.set_shadow_type(gtk.SHADOW_IN)
        self.toc_buffer = gtksourceview2.Buffer(None)
        self.toc_view = gtksourceview2.View(self.toc_buffer)
        self.toc_view.set_wrap_mode(gtk.WRAP_WORD)
        self.scrolled_window_toc.add(self.toc_view)
        tag = self.toc_buffer.create_tag('toc')
        tag.set_property('font', 'Inconsolata 18')

        # TITLE
        self.scrolled_window_title = gtk.ScrolledWindow()
        self.scrolled_window_title.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scrolled_window_title.set_shadow_type(gtk.SHADOW_IN)
        self.title_buffer = gtksourceview2.Buffer(None)
        self.title_view = gtksourceview2.View(self.title_buffer)
        self.title_view.set_wrap_mode(gtk.WRAP_WORD)
        self.scrolled_window_title.add(self.title_view)
        tag = self.title_buffer.create_tag('toc')
        tag.set_property('font', 'Inconsolata 18')
        # FUTURE - ALL CONTENT BUFFER | Index etc
        # scrolled_window, self.toc_buffer = self.__create_text(True)
        # self._new_notebook_page(scrolled_window, '_TOC')
        # tag = self.source_buffer.create_tag('toc')
        # tag.set_property('font', 'Inconsolata 18')

        nb_childs = self.notebook.get_children()
        sw_childs = nb_childs[0].get_children()
        sw_childs[0].realize()
        pixbuf = gtk.gdk.pixbuf_new_from_file(MAIN_IMAGE)
        pixmap, mask = pixbuf.render_pixmap_and_mask()
        tvwindow = sw_childs[0].get_window(gtk.TEXT_WINDOW_TEXT)
        tvwindow.set_back_pixmap(pixmap, gtk.FALSE)
        self.show_all()
        self.on_launch()

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
        text_view.set_wrap_mode(gtk.WRAP_WORD)
        scrolled_window.add(text_view)
        if not is_source:
            # context = text_view.get_pango_context()
            # fonts = context.list_families()
            # for font in fonts:
            #     print font.get_name()
            font = pango.FontDescription('Indie Flower 16')
            text_view.modify_font(font)
            text_view.connect("key-press-event", self.key_press_event)
            text_view.connect("event-after", self.event_after)
            text_view.connect("motion-notify-event", self.motion_notify_event)
            text_view.connect("visibility-notify-event", self.visibility_notify_event)
        return scrolled_window, buffer

    def on_launch(self):
        # set timer
        self.image = gtk.Image()
        self.image.set_from_file(BUTTON_GREEN)
        self.image.set_tooltip_text("Connected and up to date.")

        self.image2 = gtk.Image()
        self.image2.set_from_file(BUTTON_ORANGE)
        self.image2.set_tooltip_text("Connected and not up to date.")

        self.image3 = gtk.Image()
        self.image3.set_from_file(BUTTON_RED)
        self.image3.set_tooltip_text("Not connected.")

        # start with a red light
        self.tbbox.pack_end(self.image3, False, False)
        self.tbbox.pack_end(self.toolbar_r, False, False)
        self.image3.show()
        self.timer = gobject.timeout_add(1000, self.is_connected)
        self.insert_title(self)

    def show_title(self, something):
        """shows title.txt"""
        global TITLE_ACTIVE
        if TITLE_ACTIVE:
            return
        else:
            childs = self.hpaned.get_children()
            try:
                if childs[1] is self.scrolled_window_toc:
                    self.hpaned.remove(self.scrolled_window_toc)
            except:
                pass
            try:
                if childs[1] is self.notebook:
                    self.hpaned.remove(self.notebook)
            except:
                pass
            self.hpaned.add2(self.scrolled_window_title)
            self.title_view.show()
            self.scrolled_window_title.show()
            self.home_button.set_sensitive(False)
            TITLE_ACTIVE = True

    def insert_title(self, something):
        """creates title buffer from title.txt"""
        global TITLE_ACTIVE
        if not TITLE_ACTIVE:
            file = open(TITLE, "r")
            text = file.read()
            self.title_view.show()
            self.title_buffer.set_text(text)
            for row in category:
                enditer = self.title_buffer.get_end_iter()
                self.title_buffer.insert(enditer, "\n")
                enditer = self.title_buffer.get_end_iter()
                self.title_buffer.insert(enditer, row)
                enditer = self.title_buffer.get_end_iter()
            self.show_title(self)

    def row_activated_cb(self, treeview, path, column):
        # fixme - is this actually called in the original code?
        model = treeview.get_model()
        iter = model.get_iter(path)
        module_name = model.get_value(iter, MODULE_COLUMN)
        func_name = model.get_value(iter, FUNC_COLUMN)
        italic_value = model.get_value(iter, ITALIC_COLUMN)
        if module_name is None:  # a "category" row is activated
            # print "cat selected"
            cat_name = model.get_value(iter, TITLE_COLUMN)
            # print cat_name
            return True
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
        global TITLE_ACTIVE
        model, iter = selection.get_selected()
        if not iter:
            return False
        name = model.get_value(iter, MODULE_COLUMN)
        if name is not None:
            # show module
            self.load_module(name)
            childs = self.hpaned.get_children()
            if childs[1] is self.scrolled_window_toc:
                self.hpaned.remove(self.scrolled_window_toc)
            if childs[1] is self.scrolled_window_title:
                self.hpaned.remove(self.scrolled_window_title)
                TITLE_ACTIVE = False
                self.home_button.set_sensitive(True)
            self.hpaned.add2(self.notebook)
            self.notebook.show()
        else:
            # show toc
            cat_name = model.get_value(iter, TITLE_COLUMN)
            cat_name = cat_name.lower()
            # self.notebook.hide()
            self.insert_toc(cat_name)

    def insert_toc(self, cat_name):
        global TITLE_ACTIVE
        childs = self.hpaned.get_children()
        try:
            if childs[1] is self.notebook:
                self.hpaned.remove(self.notebook)
        except:
            pass
        try:
            if childs[1] is self.scrolled_window_title:
                self.hpaned.remove(self.scrolled_window_title)
                TITLE_ACTIVE = False
                self.home_button.set_sensitive(True)
        except:
            pass
        try:
            self.hpaned.add2(self.scrolled_window_toc)
        except:
            pass
        self.scrolled_window_toc.show()
        self.toc_view.show()
        try:
            TOCFILE = cat_name + ".toc"
            TOCFILE = os.path.join(DEMODIR, TOCFILE)
            file = open(TOCFILE, "r")
            text = file.read()
            self.toc_buffer.set_text(text)
        except:
            self.scrolled_window_toc.hide()

    def window_closed_cb(self, window, model, path):
        iter = model.get_iter(path)
        module_name = model.get_value(iter, MODULE_COLUMN)
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
        # FIXME REFACTOR
        try:
            SCREENSHOT = "demos/" + filename + ".jpg"
            pixbuf = gtk.gdk.pixbuf_new_from_file(SCREENSHOT)
            # pixbuf = pixbuf.scale_simple(200, 200, gtk.gdk.INTERP_BILINEAR)
            enditer = buffer.get_end_iter()
            buffer.insert_pixbuf(enditer, pixbuf)
        except:
            pass
        try:
            SCREENSHOT = "demos/" + filename + ".png"
            pixbuf = gtk.gdk.pixbuf_new_from_file(SCREENSHOT)
            # pixbuf = pixbuf.scale_simple(200, 200, gtk.gdk.INTERP_BILINEAR)
            enditer = buffer.get_end_iter()
            buffer.insert_pixbuf(enditer, pixbuf)
        except:
            pass
        try:
            SCREENSHOT = "demos/" + filename + ".svg"
            pixbuf = gtk.gdk.pixbuf_new_from_file(SCREENSHOT)
            # pixbuf = pixbuf.scale_simple(200, 200, gtk.gdk.INTERP_BILINEAR)
            enditer = buffer.get_end_iter()
            buffer.insert_pixbuf(enditer, pixbuf)
        except:
            pass
        try:
            SCREENSHOT = "demos/" + filename + ".gif"
            pixbufanim = gtk.gdk.PixbufAnimation(SCREENSHOT)
            image = gtk.Image()
            image.set_from_animation(pixbufanim)
            image.show()
            button = gtk.Button()
            button.add(image)
            button.show()
            enditer = buffer.get_end_iter()
            anchor = buffer.create_child_anchor(enditer)
            nb_childs = self.notebook.get_children()
            sw_childs = nb_childs[0].get_children()
            sw_childs[0].realize()
            sw_childs[0].add_child_at_anchor(button, anchor)
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
