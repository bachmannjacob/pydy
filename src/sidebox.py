import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


label_height = 50
months_in_words = ['Januar',
          'Februar',
          'März',
          'April',
          'Mai',
          'Juni',
          'Juli',
          'August',
          'September',
          'Oktober',
          'November',
          'Dezember']


class Sidebox(Gtk.Box):

    linker = None

    def __init__(self):

        Gtk.Box.__init__(self)

        self.year_listbox = Gtk.ListBox()
        self.year_revealer = Gtk.Revealer()
        self.month_listbox = Gtk.ListBox()
        self.month_revealer = Gtk.Revealer()
        self.day_listbox = Gtk.ListBox()
        self.day_revealer = Gtk.Revealer()

        self.year_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_RIGHT)
        self.year_revealer.set_reveal_child(True)
        self.year_listbox.set_header_func(self.update_header_func, None)
        self.year_listbox.connect('row-activated', self.year_label_clicked)
        year_scrolled = Gtk.ScrolledWindow()
        year_scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        year_scrolled.add(self.year_listbox)
        self.year_revealer.add(year_scrolled)

        self.month_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_LEFT)
        self.month_listbox.set_header_func(self.update_header_func, None)
        self.month_listbox.connect('row-activated', self.month_label_clicked)
        month_scrolled = Gtk.ScrolledWindow()
        month_scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        month_scrolled.add(self.month_listbox)
        self.month_revealer.add(month_scrolled)

        self.day_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_LEFT)
        self.day_listbox.set_header_func(self.update_header_func, None)
        self.day_listbox.connect("row-activated", self.day_label_clicked)
        day_scrolled = Gtk.ScrolledWindow()
        day_scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        day_scrolled.add(self.day_listbox)
        self.day_revealer.add(day_scrolled)

        self.pack_start(self.year_revealer, False, False, 0)
        self.pack_start(self.month_revealer, False, False, 0)
        self.pack_start(self.day_revealer, False, False, 0)

    def set_connection_linker(self, linker):
        self.linker = linker

    def set_size_group(self, size_group):

        # adds listboxes to sizegroup with left_header
        size_group.add_widget(self.year_listbox)
        size_group.add_widget(self.month_listbox)
        size_group.add_widget(self.day_listbox)

    def set_revealer_signal(self):
        self.year_revealer.connect("notify::child-revealed", self.linker.header.restore_sens_b_f_button)
        self.month_revealer.connect("notify::child-revealed", self.linker.header.restore_sens_b_f_button)
        self.day_revealer.connect("notify::child-revealed", self.linker.header.restore_sens_b_f_button)

    def update_year(self):

        # removes previous children of year_listbox and
        # updates year_listbox
        for child in self.year_listbox.get_children():
            self.year_listbox.remove(child)

        for i in self.linker.diary.get_year():
            new_row = Gtk.ListBoxRow()

            new_label = Gtk.Label()
            new_label.set_markup("<big>" + str(i) + "</big>")
            new_label.set_size_request(0, label_height)

            new_row.add(new_label)
            self.year_listbox.add(new_row)

        self.year_listbox.show_all()

    def update_month(self):

        # removes previous children of month_listbox and
        # updates month_listbox
        for child in self.month_listbox.get_children():
            self.month_listbox.remove(child)

        for i in self.linker.diary.get_month():
            new_row = Gtk.ListBoxRow()

            new_label = Gtk.Label()
            new_label.set_markup("<big>" + months_in_words[i-1] + "</big>")
            new_label.set_size_request(0, label_height)

            new_row.add(new_label)
            self.month_listbox.add(new_row)

        self.month_listbox.show_all()

    def update_day(self):

        # removes previous children of day_listbox and
        # updates day_listbox
        for child in self.day_listbox.get_children():
            self.day_listbox.remove(child)

        for i in self.linker.diary.get_day():
            new_row = Gtk.ListBoxRow()

            new_label = Gtk.Label()
            new_label.set_markup("<big>" + str(i) + "</big>")
            new_label.set_size_request(0, label_height)

            new_row.add(new_label)
            self.day_listbox.add(new_row)

        self.day_listbox.show_all()

    def update_all(self):
        self.update_year()
        self.update_month()
        self.update_day()

    def update_header_func(self, row, before, userdata):

        # method to set a separator between childs of listboxes
        if before is None:
            row.set_header(None)

        elif row.get_header() is None:
            sep = Gtk.HSeparator()
            row.set_header(sep)

    def year_label_clicked(self, widget, row):

        # updates year_listbox with days belonging to clicked year
        self.linker.diary.set_cur_year(int(row.get_child().get_text()))
        self.update_month()
        self.linker.diary.set_cur_month(None)
        self.update_day()
        self.action_forward(None)

    def month_label_clicked(self, widget, row):

        # updates day_listbox with days belonging to clicked month
        self.linker.diary.set_cur_month(months_in_words.index(row.get_child().get_text()) + 1)
        self.update_day()
        self.action_forward(None)

    def day_label_clicked(self, widget, row):

        # load text of clicked day from diary to text_buffer
        self.linker.diary.set_cur_day(int(row.get_child().get_text()))
        text = self.linker.diary.load_diary()
        self.linker.textview.text_buffer.set_text(text)

    def day_label_select(self, day):
        day_str = '0' + str(day) if day < 10 else str(day)
        day_str_label = "<big>" + day_str + "</big>"
        for child in self.day_listbox.get_children():
            if child.get_children()[0].get_label() == day_str_label:
                self.day_listbox.select_row(child)
                break

    def action_back(self, widget=None):

        # switch to year_revealer and update clickability back and forward buttons
        if not self.year_revealer.get_reveal_child() and not self.day_revealer.get_reveal_child():
            self.linker.header.b_button_sens = False
            if not self.linker.header.forward_button.get_sensitive():
                self.linker.header.f_button_sens = True
            self.linker.header.set_sens_b_f_button(False, False)
            self.month_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_LEFT)
            self.month_revealer.set_reveal_child(False)
            self.year_revealer.set_reveal_child(True)
        elif self.year_revealer.get_reveal_child():
            pass
        # switch to month_revealer and update clickability back and forward buttons
        else:
            self.linker.header.f_button_sens = True
            self.linker.header.b_button_sens = True
            self.linker.header.set_sens_b_f_button(False, False)
            self.month_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_RIGHT)
            self.day_revealer.set_reveal_child(False)
            self.month_revealer.set_reveal_child(True)

    def action_forward(self, widget=None):

        # switch to day_revealer and update clickability back and forward buttons
        if not self.year_revealer.get_reveal_child() and not self.day_revealer.get_reveal_child():
            self.linker.header.f_button_sens = False
            self.linker.header.b_button_sens = True
            self.linker.header.set_sens_b_f_button(False, False)
            self.month_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_RIGHT)
            self.month_revealer.set_reveal_child(False)
            self.day_revealer.set_reveal_child(True)
        elif self.day_revealer.get_reveal_child():
            pass
        else:
            # switch to day_revealer and update clickability back and forward buttons
            if len(self.day_listbox.get_children()) == 0:
                self.linker.header.f_button_sens = False
            self.linker.header.b_button_sens = True
            self.linker.header.set_sens_b_f_button(False, False)
            self.month_revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_LEFT)
            self.year_revealer.set_reveal_child(False)
            self.month_revealer.set_reveal_child(True)

    hidden = None

    def hide_all(self):
        if self.year_revealer.get_reveal_child():
            self.hidden = self.year_revealer
            self.year_revealer.set_reveal_child(False)
        elif self.month_revealer.get_reveal_child():
            self.hidden = self.month_revealer
            self.month_revealer.set_reveal_child(False)
        elif self.day_revealer.get_reveal_child():
            self.hidden = self.day_revealer
            self.day_revealer.set_reveal_child(False)

    def unhide_all(self):
        if self.hidden is not None:
            self.hidden.set_reveal_child(True)


class Searchbar(Gtk.Revealer):

    linker = None

    def __init__(self):

        Gtk.Revealer.__init__(self)
        self.set_transition_type(Gtk.RevealerTransitionType.SLIDE_RIGHT)
        self.set_reveal_child(True)

        # setting up search bar
        self.searchbar = Gtk.SearchBar()
        searchentry = Gtk.SearchEntry()
        self.searchbar.connect_entry(searchentry)
        self.searchbar.add(searchentry)

        self.add(self.searchbar)

    def set_connection_linker(self, linker):
        self.linker = linker

    def set_revealer_signal(self):
        self.connect("notify::child-revealed", self.action_revealer_signal)

    def action_revealer_signal(self, widget, boolean):
        self.linker.textview.update_buffer(self.linker.diary.load_diary())

    def action_reveal(self, widget):

        # method to reveal and hide searchbar
        if self.searchbar.get_search_mode():
            self.searchbar.set_search_mode(False)
        else:
            self.searchbar.set_search_mode(True)

    def hide_all(self):
        self.set_reveal_child(False)

    def unhide_all(self):
        self.set_reveal_child(True)