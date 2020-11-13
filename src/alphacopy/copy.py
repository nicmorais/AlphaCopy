#!/usr/bin/env python3
import os
import shutil
import psutil

def start_copy():
    # Show the Devices connected
    selectedDevice = show_mounted_disks()

    # Check the source and the target selected

    # Check if has enough free space on the target
    #check_free_space()

    # Create new folder on target (with sequential number as name)
    # Start the copy
    # Check if the files are ok

def show_mounted_disks():
    partitions = psutil.disk_partitions()
    listDevices = []

    for p in partitions:
        deviceInfo = []
        usage = psutil.disk_usage(p.mountpoint)
        nome = p.mountpoint
        device = p.device
        tipo = p.fstype
        usado = usage.used / (1024.0 ** 3)
        livre = usage.free / (1024.0 ** 3)
        deviceInfo.append(nome)
        deviceInfo.append(device)
        deviceInfo.append(tipo)
        deviceInfo.append(str(usado))
        deviceInfo.append(str(livre))
        listDevices.append(deviceInfo)
        print("Nome: " + deviceInfo[0] + " Dispositivo: " + deviceInfo[1] + " Tipo: " + deviceInfo[2] + " Usado: " + deviceInfo[3] + " Livre: " + deviceInfo[4])

        return listDevices

def show_devices():
    path = "/media/pi/"
    dirs = os.listdir(path)
    for file in dirs:
        # print('Volume Path: '+ os.path.abspath(os.path.join(dir, file)), sep='\n')
        print(file)

def check_free_space(src, dst):
    """
    Checks whether filesystem on "dst" has enough free space for "src" files
    """
    src_disk_usage = shutil.disk_usage(src)[1]
    destinaton_disk_free = shutil.disk_usage(dst)[2]
    return src_disk_usage <= destinaton_disk_free

def copy_file(src, dst):
    """Copies single file from src to dst"""
    shutil.copy2(src, dst)
    with open(dst, 'a') as f:
        os.fsync(f)


def external_disks(src = '/media/pi/'):
    """
    Find directories that are mounted on the given folder
    Raises a ValueError if the given folder doesn't exists
    Raises a ValueError if the given folder is, actually, a file
    src -> str
        The given folder in which this function should scan
    returns: list[str]
        Each element in the list is a string with the full path of the folder
        A empy list means that no folder was found
    """
    return

start_copy()