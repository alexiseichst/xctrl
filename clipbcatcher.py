from PySide6 import QtWidgets, QtCore, QtGui
import concurrent.futures
import os
import time
import json
from save import JSonSave

class ClipBCatcher():
    def __init__(self, app, save_dir):
        self.app = app
        self.save_dir = save_dir
        self.last_text = ""
        self.last_html = ""
        self.last_image = ""
        self.image_call_back_list = []
        self.text_call_back_list = []
        self.save = JSonSave(self.save_dir)

    def add_text_call_back(self, function):
        self.text_call_back_list.append(function)
    
    def add_image_call_back(self, function):
        self.image_call_back_list.append(function)

    def run(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.worker = self.executor.submit(self.worker)

    def worker(self):
        self.loop = True
        while self.loop:
            time.sleep(0.01)
            clipboard = self.app.clipboard()
            current_mime_data = clipboard.mimeData()
            self.save_data(current_mime_data)
            time.sleep(0.01)
            
    def save_data(self, mimdata):
        self.data_dir_exists()
        if mimdata.hasImage() :
            self.save_image(QtGui.QImage(mimdata.imageData()))
        if mimdata.hasHtml():
            self.save_html(mimdata.html())
        if mimdata.hasText():
            self.save_text(mimdata.text())

    def data_dir_exists(self):
        if not os.path.isdir(self.save_dir):
            os.makedirs(self.save_dir)

    def save_image(self, image):
        if image != self.last_image:
            self.last_image = image
            [f(image) for f in self.image_call_back_list]
            self.save.save_image(image)
            
    def save_text(self, text):
        if text != self.last_text and text != "":
            self.last_text = text
            [f(text) for f in self.text_call_back_list]
            self.save.save_text(text)
        
    def save_html(self, html):
        if html != self.last_html:
            self.last_html = html
            self.save.save_html(html)