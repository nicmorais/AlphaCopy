# This Python file uses the following encoding: utf-8
from PyQt5.QtCore import QThread
from alphacopy.devicesutil import DevicesUtil


class CopyWorker(QThread):
    src = ''
    dest = ''

    def __init__(self):
        super(CopyWorker, self).__init__()

    def run(self):
        devices = DevicesUtil()
        devices.copytree('/media/nicolas/SD32', '/media/nicolas/3e5d7b5f-1613-4b3f-8afe-9435d0cf55b6')
