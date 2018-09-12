import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from diary import Diary
from header import Header
from sidebox import Searchbar, Sidebox
from textview import Textview


class Linker():

    diary = None
    header = None
    sidebox = None
    searchbar = None
    textview = None

    def __init__(self, diary=None,
                 header=None,
                 sidebox=None,
                 searchbar=None,
                 textview=None):
        if diary is not None:
            self.diary = diary
        if header is not None:
            self.header = header
        if sidebox is not None:
            self.sidebox = sidebox
        if searchbar is not None:
            self.searchbar = searchbar
        if textview is not None:
            self.textview = textview


class MainWindow(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title='Diary')
        self.set_default_size(800, 600)
        self.connect('destroy', Gtk.main_quit)

        main_box = Gtk.Box()
        size_group = Gtk.SizeGroup(Gtk.SizeGroupMode.HORIZONTAL)

        # initializing all relevant classes
        diary = Diary("Test User")
        textview = Textview()
        header = Header()
        searchbar = Searchbar()
        sidebox = Sidebox()

        # transfer classes to linker
        linker = Linker(diary, header, sidebox, searchbar, textview)

        # transfer linker to header and sidebox
        header.set_connection_linker(linker)
        sidebox.set_connection_linker(linker)
        sidebox.update_year()
        searchbar.set_connection_linker(linker)
        searchbar.set_revealer_signal()

        # connect size_group to header and sidebox
        header.set_size_group(size_group)
        sidebox.set_size_group(size_group)

        sidebox.set_revealer_signal()

        # setup relevant buttons in header
        header.set_backbutton()
        header.set_forwardbutton()
        header.set_searchbutton()
        header.set_addbutton()
        header.set_editbutton()
        self.set_titlebar(header)

        # create new side_box to add searchbar and sidebox
        # and add it to beginning of mainbox
        side_box = Gtk.VBox()
        side_box.pack_start(searchbar, False, False, 0)
        side_box.pack_start(sidebox, True, True, 0)
        side_box.set_hexpand(False)
        main_box.pack_start(side_box, False, False, 0)

        # add separator between side_box and textview
        separator = Gtk.HSeparator()
        separator.set_size_request(1, 0)
        main_box.pack_start(separator, False, False, 0)

        # add textview to end of mainbox
        main_box.pack_start(textview, False, True, 0)

        self.add(main_box)


win = MainWindow()
win.show_all()
Gtk.main()
