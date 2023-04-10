from PyQt5 import QtCore
import os
import psutil
import subprocess
from time import sleep


class ProcessThread(QtCore.QThread):
    change_value = QtCore.pyqtSignal(list)

    def run(self):
        while True:
            wmic_cmd = """wmic process where 'name="pythonw.exe" or name="python.exe"' get commandline,processid"""
            wmic_prc = subprocess.Popen(wmic_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            wmic_out, wmic_err = wmic_prc.communicate()

            python_procs = [item.rsplit(None, 1) for item in wmic_out.splitlines() if item][1:]
            python_procs = [[cmdline.decode("utf-8"), int(pid), 0, 0] for [cmdline, pid] in python_procs if
                            int(pid) != os.getpid()]
            for i, item in enumerate(python_procs):
                item_pid = psutil.Process(int(item[1]))
                item[2] = f"{item_pid.cpu_percent(interval=0.1) / psutil.cpu_count():.1f}"
                item[3] = f"{item_pid.memory_full_info().uss / 1000000:.1f}"
            self.change_value.emit(python_procs)
            sleep(1)
