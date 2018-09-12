import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Textview(Gtk.ScrolledWindow):

    def __init__(self):

        Gtk.ScrolledWindow.__init__(self)

        self.text_view = Gtk.TextView()
        # self.text_view.set_pixels_inside_wrap(0)
        self.text_view.set_top_margin(20)
        self.text_view.set_bottom_margin(20)
        # self.text_view.set_right_margin(20)
        # self.text_view.set_left_margin(20)
        self.text_view.set_margin_left(20)
        self.text_view.set_margin_right(20)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.text_buffer = self.text_view.get_buffer()
        self.text_view.set_editable(False)
        self.text_view.set_cursor_visible(False)

        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.add(self.text_view)

    def action_editable(self):
        self.text_view.set_editable(True)
        self.text_view.set_cursor_visible(True)

    def action_uneditable(self):
        self.text_view.set_editable(False)
        self.text_view.set_cursor_visible(False)

    def update_buffer(self, text):
        self.text_buffer.set_text(text)
