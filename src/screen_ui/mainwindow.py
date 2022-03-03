from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize, QThreadPool, pyqtSlot
from alphacopy.devicesutil import DevicesUtil
from alphacopy.copyworker import CopyWorker
from alphacopy.copywaiter import CopyWaiter


class MainWindow(QMainWindow):
    devices = DevicesUtil()
    sd_label = ''
    hdd_label = ''

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('screen_ui/mainwindow.ui', self)
        logo = QPixmap('assets/logos/alphaletter.png')
        self.logoLabel.setPixmap(logo.scaled(QSize(110, 70)))
        hddIcon = QPixmap('assets/devices/usb-black.png')
        self.hddIconLb.setPixmap(hddIcon.scaled(QSize(64, 64)))
        sdIcon = QPixmap('assets/devices/Sycamoreent-Storage-Sd.png')
        self.sdIconLb.setPixmap(sdIcon.scaled(QSize(64, 64)))
        self.stackedWidget.setCurrentIndex(0)

    @pyqtSlot()
    def scan(self):
        disks = self.devices.list_disks()
        if len(disks) > 0:
            self.stackedWidget.setCurrentIndex(2)
            self.set_sd_hdd(disks)
        else:
            self.stackedWidget.setCurrentIndex(1)

    def set_sd_hdd(self, disks):
        sd_found = False
        for disk in disks:
            size = self.devices.disk_size(disk)
            if size < 65:
                sd_found = True
                self.sd_label = disk
            else:
                self.hdd_label = disk

        if sd_found:
            self.hddLE.setText(self.hdd_label)
            self.sdLE.setText(self.sd_label)
        else:
            errorMessage = "A suitable SD card could not be found."
            self.notFoundDescriptionLb.setText(errorMessage)
            self.stackedWidget.setCurrentIndex(1)

    def incrementProgressBar(self):
        currentValue = self.copyProgrB.value()
        self.copyProgrB.setValue(currentValue + 1)

    @pyqtSlot()
    def setProgressBar(self, value):
        print("setProgressBar", value)
        self.copyProgrB.setValue(value)

    @pyqtSlot()
    def copy(self):
        devices = DevicesUtil()

        self.stackedWidget.setCurrentIndex(3)
        sd_path = self.devices.volumes_path + '/' + self.sd_label
        hdd_path = self.devices.volumes_path + '/' + self.hdd_label
        try:
            total_files = len(self.devices.list_files(sd_path))
        except Exception:
            self.stackedWidget.setCurrentIndex(5)

        self.copyProgrB.setMaximum(total_files)

        self.worker = CopyWorker()
        self.waiter = CopyWaiter()
        self.waiter.src = "/media/nicolas/SD32"
        self.waiter.dest = devices.make_dir(hdd_path)
        self.waiter.signal.copied_changed.connect(lambda val: self.copyProgrB.setValue(val))
#        self.threadpool = QThreadPool()
#        self.threadpool.start(self.worker)
#        self.threadpool.start(self.waiter)
        self.worker.start()
        self.waiter.start()

    @pyqtSlot()
    def done(self):
        self.stackedWidget.setCurrentIndex(6)

    @pyqtSlot()
    def eject(self):
        self.devices.eject_disk(self.sd_label)
        self.stackedWidget.setCurrentIndex(0)

    @pyqtSlot()
    def abort_copy(self):
        pass
