# coding: utf-8

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gio, GObject, Gtk

from desktop_entry.handler import Handler


class DesktopEntryApp(Gtk.Application):

    def __init__(self, **kwargs):
        super().__init__(application_id="github.io.desktop-entry", **kwargs)
        # Builder
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/entry.glade")
        self.builder.connect_signals(Handler(self))
        # Dialog categories
        self.dialog_list_categories = self.builder.get_object('dialog1')
        self.dialog_list_categories.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK)

    def do_startup(self):
        Gtk.Application.do_startup(self)
        # Quit action
        action_quit = Gio.SimpleAction.new("quit", None)
        action_quit.connect("activate", self.on_quit)
        self.add_action(action_quit)

    def do_activate(self):
        active_window = self.get_active_window()
        if not active_window:
            # Get the window from glade
            home_window = self.builder.get_object('home_window')
            home_window.show_all()
            # Add window to the app
            self.add_window(home_window)
        else:
            active_window.present()
    
    def activate_create_window(self, filename=None):
        active_window = self.get_active_window()
        active_window.destroy()
        main_window = self.builder.get_object('main_window')
        main_window.show_all()
        self.add_window(main_window)

    def on_quit(self, action, extra):
        self.quit()
