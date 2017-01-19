# coding: utf-8

import signal
import sys
import os
import configparser

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gio, GObject, Gtk
from handler import Handler

def create_file(base_path, name, 
        application_type, version, icon, exec_app):
    path = base_path + name + '.desktop'
    with open(path, 'w') as f:
        f.write('[Desktop Entry]\n')
        f.write('Name={}\n'.format(name))
        f.write('Type={}\n'.format(application_type))
        if version:
            f.write('Version={}\n'.format(version))
        if icon:
            f.write('Icon={}\n'.format(icon))
        if exec_app:
            f.write('Exec={}\n'.format(exec_app))


class DesktopEntryApp(Gtk.Application):

    def __init__(self, **kwargs):
        super().__init__(application_id="github.io.desktop-entry", **kwargs)

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
            builder = Gtk.Builder()
            builder.add_from_file("entry.glade")
            # Connect to signals
            builder.connect_signals(Handler(self))
            #main_window = builder.get_object('main_window')
            #main_window.show_all()
            home_window = builder.get_object('home_window')
            home_window.show_all()
            # Add window to the app
            #self.add_window(main_window)
            #self.window = main_window
            self.add_window(home_window)
            self.window = home_window
            self.builder = builder
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

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = DesktopEntryApp()
    app.run(sys.argv)
