# coding: utf-8

import signal
import sys
import os

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gio, GObject, Gtk

DESKTOP_FILES_PATH = os.path.expanduser('~') + '/.local/share/applications/'


def create_file(base_path, name, application_type):
    path = base_path + name + '.desktop'
    with open(path, 'w') as f:
        f.write('[Desktop Entry]\n')
        f.write('Name={}\n'.format(name))
        f.write('Type={}\n'.format(application_type))


class Handler:

    def __init__(self, application):
        self.application = application

    def on_form_submit(self, name_entry, application_type):
        import pdb; pdb.set_trace()
        # Check if name is empty
        name = name_entry.get_text()
        if not name:
            print('no name')
            return
        # File creation
        create_file(
            base_path=DESKTOP_FILES_PATH,
            name=name,
            application_type='test'
        )
        # Shutdown application
        self.application.quit()

    def on_form_cancel(self, button):
        print('Bye !')
        self.application.quit()


class DesktopEntryApp(Gtk.Application):

    def __init__(self, **kwargs):
        super().__init__(application_id="github.io.desktop-entry", **kwargs)
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # Quit action
        action_quit = Gio.SimpleAction.new("quit", None)
        action_quit.connect("activate", self.on_quit)
        self.add_action(action_quit)

    def do_activate(self):
        if not self.window:
            # Get the window from glade
            builder = Gtk.Builder()
            builder.add_from_file("entry.glade")
            # Connect to signals
            builder.connect_signals(Handler(self))
            main_window = builder.get_object('main_window')
            main_window.show_all()

            # Signals
            #name_entry = builder.get

            # Add window to the app
            self.add_window(main_window)
            self.window = main_window
        self.window.present()

    def on_quit(self, action, extra):
        self.quit()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = DesktopEntryApp()
    app.run(sys.argv)
