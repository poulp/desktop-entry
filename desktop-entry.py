# coding: utf-8

import sys
import signal

from desktop_entry.app import DesktopEntryApp

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = DesktopEntryApp()
    app.run(sys.argv)
