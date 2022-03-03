# This Python file uses the following encoding: utf-8
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from alphacopy.devicesutil import DevicesUtil
import time


class CopyWaiterSignals(QObject):
    copied_changed = pyqtSignal(int)


class CopyWaiter(QThread):
    src = ''
    dest = ''

    def __init__(self):
        super(CopyWaiter, self).__init__()
        self.signal = CopyWaiterSignals()

    def run(self):
        devices = DevicesUtil()
        src_size = devices.get_size(self.src)
        dest_size = 0
        while dest_size < src_size:
            self.signal.copied_changed.emit(dest_size)
            dest_size = devices.get_size(self.dest)
            time.sleep(1)
