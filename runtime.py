from mainwindow import MainWindow
import sys
import os
import pathlib
import glob
from PySide6.QtCore import QStandardPaths, QTimer
from PySide6.QtWidgets import QApplication, QListWidget
from PySide6.QtGui import QImage
from clipbcatcher import ClipBCatcher

class Runtime():
    
    def __init__(self):
        super().__init__()
        self.app_name = 'QCB'
        self.data_dir = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)
        self.data_dir = os.path.realpath(os.path.join(self.data_dir, self.app_name, 'data'))
        self.ext_map = {'.txt': self.read_text, '.png': self.read_image}

    def run(self):
        return self.main_loop()

    def main_loop(self):
        self.app = QApplication([])
        self.app.setApplicationName(self.app_name)
        QTimer.singleShot(0, self.init_in_loop)
        return self.app.exec()

    def init_in_loop(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.main_window.init_ui()

        self.clipbcatcher = ClipBCatcher(self.app, self.data_dir)
        self.clipbcatcher.run()
        self.clipbcatcher.add_text_call_back(self.upadte_text_cb)
        self.clipbcatcher.add_image_call_back(self.upadte_image_cb)

        self.listWidget = QListWidget(self.main_window)

        self.read_history()

    def upadte_text_cb(self, text, file):
        self.main_window.add_text_widget(text, file)
    
    def upadte_image_cb(self, image, file):
        self.main_window.add_image_widget(image, file)

    @property
    def file_list(self):
        return glob.glob(os.path.join(self.data_dir,'*'))

    def read_history(self):
        file_list = self.file_list
        for f in file_list:
            s = pathlib.Path(f).suffix
            reader = self.ext_map.get(s)
            if reader: reader(f)

    def read_image(self, file):
        self.main_window.add_image_widget(QImage(file), file)

    def read_text(self, file):
        with open(file) as f:
            self.main_window.add_text_widget(f.read(), file)


