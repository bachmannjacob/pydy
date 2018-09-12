import datetime
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio


class Header(Gtk.HBox):

    linker = None

    def __init__(self):

        Gtk.HBox.__init__(self)

        self.now = datetime.datetime.now()

        self.left_header = Gtk.HeaderBar()
        self.right_header = Gtk.HeaderBar()

        self.back_button = Gtk.Button()
        self.forward_button = Gtk.Button()

        # initializing header
        if Gtk.Settings.get_default().props.gtk_decoration_layout.split(",")[0] == "close":
            self.left_header.set_show_close_button(True)
        else:
            self.right_header.set_show_close_button(True)
        self.left_header.set_title('Diary')

        # creating box for back and forward
        back_forward_box = Gtk.Box()
        Gtk.StyleContext.add_class(back_forward_box.get_style_context(), 'linked')

        # initializing back button
        self.back_button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        self.back_button.set_sensitive(False)

        # initializing forward button
        self.forward_button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        self.forward_button.set_sensitive(False)

        # packing buttons to box
        back_forward_box.add(self.back_button)
        back_forward_box.add(self.forward_button)

        # initializing search button
        self.button_search = Gtk.Button()
        icon = Gio.ThemedIcon(name="system-search-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.button_search.add(image)

        # initializing settings button
        button_settings = Gtk.Button()
        icon = Gio.ThemedIcon(name="view-more")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button_settings.add(image)

        # initializing add button
        self.button_add = Gtk.Button()
        icon = Gio.ThemedIcon(name="list-add")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.button_add.add(image)

        # handler_id for edit button, to disconnect signals and reconnect
        # new ones

        self.handler_edit = None

        # initializing edit button
        self.button_edit = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-edit-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.button_edit.add(image)

        # packing all to header
        self.left_header.pack_start(back_forward_box)
        self.left_header.pack_start(self.button_search)
        self.right_header.pack_end(button_settings)
        self.right_header.pack_end(self.button_add)
        self.right_header.pack_end(self.button_edit)

        self.pack_start(self.left_header, False, False, 0)
        self.pack_start(Gtk.VSeparator(), False, False, 0)
        self.pack_start(self.right_header, True, True, 0)

    def set_connection_linker(self, linker):
        self.linker = linker

    def set_size_group(self, size_group):
        size_group.add_widget(self.left_header)

    def set_backbutton(self):
        self.back_button.connect("clicked", self.linker.sidebox.action_back)

    def set_forwardbutton(self):
        self.forward_button.connect("clicked", self.linker.sidebox.action_forward)

    def set_searchbutton(self):
        self.button_search.connect("clicked", self.linker.searchbar.action_reveal)

    def set_addbutton(self):

        def button_add_clicked(self, header):
            header.linker.diary.set_cur_year(header.now.year)
            header.linker.diary.set_cur_month(header.now.month)
            header.linker.diary.set_cur_day(header.now.day)
            header.linker.diary.create_diary()
            header.linker.diary.update_data()
            header.linker.sidebox.update_all()
            header.linker.sidebox.action_forward()
            header.linker.sidebox.action_forward()
            header.linker.sidebox.day_label_select(header.now.day)

        self.button_add.connect("clicked", button_add_clicked, self)

    b_button_sens = None
    f_button_sens = None

    def set_editbutton(self):

        def action_edit_button(self, header):
            header.linker.textview.action_editable()
            header.linker.searchbar.hide_all()
            header.linker.sidebox.hide_all()
            header.b_button_sens, header.f_button_sens = header.set_sens_b_f_button(False, False)
            header.button_search.set_sensitive(False)
            header.button_add.set_sensitive(False)

            self.get_children()[0].destroy()
            icon = Gio.ThemedIcon(name="object-select-symbolic")
            image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
            self.add(image)
            self.show_all()

            self.disconnect(header.handler_edit)
            header.handler_edit = self.connect("clicked", action_save_button, header)

        def action_save_button(self, header):
            header.linker.textview.action_uneditable()
            start_iter = header.linker.textview.text_buffer.get_start_iter()
            end_iter = header.linker.textview.text_buffer.get_end_iter()
            header.linker.diary.save_diary(header.linker.textview.text_buffer.get_text(start_iter, end_iter, False))
            header.linker.textview.text_buffer.set_text("")

            header.linker.sidebox.unhide_all()
            header.linker.searchbar.unhide_all()
            # header.set_sens_b_f_button(header.b_button_sens, header.f_button_sens)
            header.button_search.set_sensitive(True)
            header.button_add.set_sensitive(True)

            self.get_children()[0].destroy()
            icon = Gio.ThemedIcon(name="document-edit-symbolic")
            image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
            self.add(image)
            self.show_all()

            self.disconnect(header.handler_edit)
            header.handler_edit = self.connect("clicked", action_edit_button, header)

        self.handler_edit = self.button_edit.connect("clicked", action_edit_button, self)

    def set_sens_b_f_button(self, b_button, f_button):

        b_button_sens = self.back_button.get_sensitive()
        f_button_sens = self.forward_button.get_sensitive()
        self.back_button.set_sensitive(b_button)
        self.forward_button.set_sensitive(f_button)

        return b_button_sens, f_button_sens

    def restore_sens_b_f_button(self, data, data2):
        self.back_button.set_sensitive(self.b_button_sens)
        self.forward_button.set_sensitive(self.f_button_sens)
