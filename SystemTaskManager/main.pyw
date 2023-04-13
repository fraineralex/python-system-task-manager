from PyQt5 import QtCore, QtWidgets
import sys
import os
import signal
from PyQt5.QtGui import QPalette, QColor
from time import sleep
from process_thread import ProcessThread


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.pythons = {}
        self.process_timer = QtCore.QTimer()
        self.setObjectName("MainWindow")
        self.resize(1000, 600)
        self.setMinimumSize(400, 200)
        self.setWindowTitle("System Task Manager")
        self.setup_UI()
        self.start_process_thread()

    def start_process_thread(self):
        self.proc_thread = ProcessThread()
        self.proc_thread.change_value.connect(self.set_processes)
        self.proc_thread.start()

    def set_processes(self, python_procs):
        self.pythons = {}
        for i, item in enumerate(python_procs):
            self.pythons[item[1]] = {"process": item[0], "cpu": item[2], "ram": item[3]}
        to_remove = []
        for x in range(self.process_list.rowCount()):
            if self.process_list.item(x, 0) is not None:
                if int(self.process_list.item(x, 0).text()) not in self.pythons.keys():
                    to_remove.append(x)
                    break
        for item in to_remove:
            self.process_list.removeRow(item)
        self.get_processes()

    def setup_UI(self):
        self.setup_central_window()
        self.setup_menu_bar()

        self.retrans_lates_UI()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.setup_UI_actions()

    def setup_UI_actions(self):
        self.delete_selected_item_button.clicked.connect(lambda: self.kill_selected_process())

    def setup_central_window(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("centralwidget")

        self.delete_selected_item_button = QtWidgets.QPushButton(self.central_widget)
        self.delete_selected_item_button.setObjectName("delete_selected_item_button")
        self.delete_selected_item_button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        font = self.delete_selected_item_button.font()
        font.setPointSize(10)
        self.delete_selected_item_button.setFont(font)

        self.process_list = QtWidgets.QTableWidget(self.central_widget)
        self.process_list.setRowCount(0)
        self.process_list.setColumnCount(4)
        self.process_list.setShowGrid(True)
        self.process_list.setFocusPolicy(QtCore.Qt.NoFocus)
        self.process_list.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        stylesheet = "QTableWidget::item{selection-background-color: #4285F4; selection-color: black;}"
        self.process_list.setStyleSheet(stylesheet)
        self.process_list.setHorizontalHeaderLabels(["PID", "CPU %", "Memory (MB)", "Process Name"])
        self.process_list.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.process_list.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.process_list.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.process_list.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.process_list.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.vBox = QtWidgets.QVBoxLayout(self.central_widget)
        self.vBox.addWidget(self.process_list)
        self.vBox.addWidget(self.delete_selected_item_button, alignment=QtCore.Qt.AlignRight)

        self.setCentralWidget(self.central_widget)


    def setup_menu_bar(self):
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

    def retrans_lates_UI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "System Task Manager"))
        self.delete_selected_item_button.setText(_translate("MainWindow", "End Process"))

    def get_processes(self):
        for i, key in enumerate(self.pythons):
            cont_flag = False
            for x in range(self.process_list.rowCount()):
                if self.process_list.item(x, 0) is not None:
                    if int(self.process_list.item(x, 0).text()) == int(key):
                        self.process_list.item(x, 0).setText(f"{key}")
                        self.process_list.item(x, 1).setText(f"{self.pythons[key]['cpu']}")
                        self.process_list.item(x, 2).setText(f"{self.pythons[key]['ram']}")
                        self.process_list.item(x, 3).setText(
                            f"""{self.pythons[key]['process'].split(" ", 1)[1].replace('"', "")}""")
                        cont_flag = True
                        break
            if cont_flag:
                continue
            print(f"inserting row - {i} {self.pythons[key]}")
            self.process_list.insertRow(i)
            self.process_list.setItem(i, 0, QtWidgets.QTableWidgetItem(f"{key}"))
            self.process_list.setItem(i, 1, QtWidgets.QTableWidgetItem(f"{self.pythons[key]['cpu']}"))
            self.process_list.setItem(i, 2, QtWidgets.QTableWidgetItem(f"{self.pythons[key]['ram']}"))
            self.process_list.setItem(i, 3, QtWidgets.QTableWidgetItem(
                f"""{self.pythons[key]['process'].split(" ", 1)[1].replace('"', "")}"""))

    def kill_selected_process(self):
        if self.process_list.currentRow() is not None:
            os.kill(int(self.process_list.item(self.process_list.currentRow(), 0).text()), signal.SIGTERM)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(244, 244, 244))           # Fondo claro
    palette.setColor(QPalette.WindowText, QColor(28, 28, 28))          # Texto oscuro
    palette.setColor(QPalette.Base, QColor(255, 255, 255))             # Fondo de objetos
    palette.setColor(QPalette.AlternateBase, QColor(230, 230, 230))    # Fondo alternativo
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))      # Fondo de herramientas
    palette.setColor(QPalette.ToolTipText, QColor(28, 28, 28))         # Texto de herramientas
    palette.setColor(QPalette.Text, QColor(28, 28, 28))                # Texto normal
    palette.setColor(QPalette.Button, QColor(230, 230, 230))           # Botones
    palette.setColor(QPalette.ButtonText, QColor(28, 28, 28))          # Texto de botones
    palette.setColor(QPalette.BrightText, QColor(230, 230, 230))       # Texto resaltado
    palette.setColor(QPalette.Link, QColor(0, 120, 215))                # Enlaces
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215))           # Resaltado
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))   # Texto resaltado
    app.setPalette(palette)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

