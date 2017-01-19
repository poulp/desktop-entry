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


DESKTOP_FILES_PATH = os.path.expanduser('~') + '/.local/share/applications/'


class Handler:

    def __init__(self, application):
        self.application = application

    #############
    # UTILS
    ############
    def _get_field(self, field_name):
        return self.application.builder.get_object(field_name)

    def init_fields_from_file(self, filename):
        # Config file parser
        config = configparser.ConfigParser()
        config.read(filename)
            
        # Name
        desktop_entry = config['Desktop Entry']
        if not desktop_entry:
            return
        name = desktop_entry.get('Name')
        if name:
            name_entry = self.application.builder.get_object('entry_name')
            name_entry.set_text(name)

    ###############
    # SIGNALS
    ##############
    def on_create_file(self, button):
        self.application.activate_create_window()

    def on_edit_file(self, button):
        dialog = Gtk.FileChooserDialog("Please choose a file", self.application.get_active_window(),
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        dialog.hide()
        filename = dialog.get_filename()
        if filename:
            self.init_fields_from_file(filename) 
            # Show window
            self.application.activate_create_window(filename)

    def on_form_submit(self, button):
        # Get name widget
        name_entry = self.application.builder.get_object('entry_name')
        # Check if name is empty
        name = name_entry.get_text().strip()
        if not name:
            dialog = Gtk.FileChooserDialog(self.application.get_active_window(),
            0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.CLOSE, "The field 'name' is required")
            dialog.run()
            dialog.hide()
            return

        # Get application fields
        application_type_field = self._get_field('combobox_application_type')
        application_type_model = application_type_field.get_model()
        application_type_iter = application_type_field.get_active_iter()
        application_type = application_type_model[application_type_iter][0]
        # Version
        version = self._get_field('entry_version').get_text().strip()
        # Icon
        icon = self._get_field('filechooserbutton_icon').get_filename()
        # Exec
        exec_app = self._get_field('entry_exec').get_text()

        # File creation
        create_file(
            base_path=DESKTOP_FILES_PATH,
            name=name,
            application_type=application_type,
            version=version,
            icon=icon,
            exec_app=exec_app
        )
        # Shutdown application
        self.application.quit()

    def on_form_cancel(self, button):
        print('Bye !')
        self.application.quit()
