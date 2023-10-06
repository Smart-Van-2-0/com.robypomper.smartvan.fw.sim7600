#!/usr/bin/python3

import logging
from typing import Optional

from pydbus import SessionBus
from gi.repository import GLib
from threading import Thread

_dbus = None
_loop: Optional[GLib.MainLoop] = None
_thread: Optional[Thread] = None

logger = logging.getLogger()


def get_dbus():
    global _dbus
    if _dbus is None:
        init_dbus()
    return _dbus


def init_dbus():
    global _dbus, _loop, _thread

    logger.debug("Initialize DBus session...")
    _dbus = SessionBus()
    _loop = None
    _thread = None
    logger.debug("DBus session initialized successfully")


def start_dbus_thread():
    global _dbus, _loop, _thread
    assert _dbus, "DBus not initialized, please call the 'init_dbus()' method"
    assert _loop is None, "DBus internal loop already running, can't start twice"
    assert _thread is None, "DBus thread already running, can't start twice"

    logger.info("DBus Internal Loop starting...")
    _thread = Thread(target=_dbus_thread_method)
    _thread.start()


def stop_dbus_thread():
    global _dbus, _loop, _thread
    assert _dbus, "DBus not initialized, please call the 'init_dbus()' method"
    assert _loop, "DBus internal loop not running, can't stop it"
    assert _thread, "DBus thread not running, can't stop it"

    _loop.quit()
    _loop = None
    _thread.join()
    _thread = None
    logger.info("DBus Internal Loop ended.")


def _dbus_thread_method():
    global _dbus, _loop, _thread

    logger.info("DBus Internal Loop started.")
    _loop = GLib.MainLoop()
    _loop.run()
    logger.debug("DBus Internal Loop ending...")
