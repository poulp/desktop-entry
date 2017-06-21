# coding: utf-8

import os
import configparser

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gio, GObject, Gtk

DESKTOP_FILES_PATH = os.path.expanduser('~') + '/.local/share/applications/'

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
        config = configparser.RawConfigParser()
        config.read(filename)
            
        # Name
        desktop_entry = config['Desktop Entry']
        if not desktop_entry:
            return

        exec_app = desktop_entry.get('Exec')
        if exec_app:
            exec_app_entry = self.application.builder.get_object('entry_exec')
            exec_app_entry.set_text(exec_app)

        icon = desktop_entry.get('Icon')
        if icon:
            icon_widget = self.application.builder.get_object('filechooserbutton_icon')
            icon_widget.set_filename(icon)

        app_type = desktop_entry.get('Type')
        if app_type:
            app_type_widget = self.application.builder.get_object('combobox_application_type')
            # TODO improve with using Liststore
            app_type_map = {'Application': 0, 'Link': 1, 'Directory': 2}
            app_type_widget.set_active(app_type_map[app_type])
            
        self._init_text_field(desktop_entry, 'Name', 'entry_name')
        self._init_text_field(desktop_entry, 'Comment', 'entry_comment')
        self._init_text_field(desktop_entry, 'Version', 'entry_version')
        self._init_text_field(desktop_entry, 'GenericName', 'entry_generic_name')
        self._init_text_field(desktop_entry, 'StartupWMClass', 'entry_startup_wm_class')
        self._init_text_field(desktop_entry, 'Path', 'entry_path')
        self._init_text_field(desktop_entry, 'Categories', 'entry_categories')

        self._init_boolean_field(desktop_entry, 'NoDisplay', 'switch_no_display')
        self._init_boolean_field(desktop_entry, 'Terminal', 'switch_terminal')
        self._init_boolean_field(desktop_entry, 'StartupNotify', 'switch_startup_notify')
        self._init_boolean_field(desktop_entry, 'DBusActivatable', 'switch_dbus_activatable')
        self._init_boolean_field(desktop_entry, 'Hidden', 'switch_hidden')

    ###############
    # SIGNALS
    ##############
    def on_create_file(self, button):
        self.application.activate_create_window()

    def on_edit_file(self, button):
        dialog = Gtk.FileChooserDialog(
            "Please choose a file",
            self.application.get_active_window(),
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        )
        response = dialog.run()
        dialog.hide()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            if filename:
                try:
                    self.init_fields_from_file(filename) 
                except configparser.Error as e:
                    dialog = Gtk.MessageDialog(
                        self.application.get_active_window(),
                        0,
                        Gtk.MessageType.ERROR,
                        Gtk.ButtonsType.CLOSE,
                        e
                    )
                    dialog.run()
                    dialog.hide()
                    return
                # Show window
                self.application.activate_create_window(filename)

    def on_form_submit(self, button):
        # Get name widget
        name_entry = self.application.builder.get_object('entry_name')
        # Check if name is empty
        name = name_entry.get_text().strip()
        if not name:
            dialog = Gtk.MessageDialog(
                self.application.get_active_window(),
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CLOSE,
                "The field 'name' is required"
            )
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
        self.application.quit()

    def on_entry_categories_button_press_event(self, entry, event):
        # TODO display a choice of categories
        # response = self.application.dialog_list_categories.run()
        # self.application.dialog_list_categories.hide()
        pass
