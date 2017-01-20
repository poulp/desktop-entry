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


    def _init_boolean_field(self, desktop_entry, key, widget_name):
        value = desktop_entry.get(key)
        if value:
            widget = self.application.builder.get_object(widget_name)
            widget.set_active(True)

    def _init_text_field(self, desktop_entry, key, widget_name):
        value = desktop_entry.get(key)
        if value:
            widget = self.application.builder.get_object(widget_name)
            widget.set_text(value)


    def init_fields_from_file(self, filename):
        # Config file parser
        config = configparser.ConfigParser()
        config.read(filename)
            
        # Name
        desktop_entry = config['Desktop Entry']
        if not desktop_entry:
            return

        #exec_app = desktop_entry.get('Exec')
        exec_app = None
        if exec_app:
            exec_app_entry = self.application.builder.get_object('entry_exec')
            exec_app_entry.set_text(exec_app)

        icon = desktop_entry.get('Icon')
        if icon:
            icon_widget = self.application.builder.get_object('filechooserbutton_icon')
            icon_widget.set_filename(icon)
            
        self._init_text_field(desktop_entry, 'Name', 'entry_name')
        self._init_text_field(desktop_entry, 'Comment', 'entry_comment')
        self._init_text_field(desktop_entry, 'Version', 'entry_version')
        self._init_text_field(desktop_entry, 'GenericName', 'entry_generic_name')

        self._init_boolean_field(desktop_entry, 'NoDisplay', 'switch_no_display')
        self._init_boolean_field(desktop_entry, 'Terminal', 'switch_terminal')
        self._init_boolean_field(desktop_entry, 'StartupNotify', 'switch_startup_notify')
        self._init_boolean_field(desktop_entry, 'DBusActivatable', 'switch_dbus_activatable')
            

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
