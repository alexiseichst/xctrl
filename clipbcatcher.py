from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QImage
import concurrent.futures
import os
import time
import json
from save import JSonSave

class ClipBCatcher(QObject):
    update_text = Signal(str, str)
    update_image = Signal(QImage, str)

    def __init__(self, app, save_dir):
        QObject.__init__(self)
        self.app = app
        self.save_dir = save_dir
        self.last_text = ""
        self.last_html = ""
        self.last_image = ""
        self.first_run = True
        self.loop = True
        self.image_call_back_list = []
        self.text_call_back_list = []
        self.save = JSonSave(self.save_dir)

    def add_text_call_back(self, function):
        self.update_text.connect(function)
    
    def add_image_call_back(self, function):
        self.update_image.connect(function)

    def run(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.worker = self.executor.submit(self.worker)

    def worker(self): 
        while self.loop:
            time.sleep(0.01)
            clipboard = self.app.clipboard()
            current_mime_data = clipboard.mimeData()
            self.save_data(current_mime_data)
            self.first_run = False
            time.sleep(0.01)
            
    def save_data(self, mimdata):
        self.data_dir_exists()
        if mimdata.hasImage() :
            self.save_image(QImage(mimdata.imageData()))
        if mimdata.hasHtml():
            self.save_html(mimdata.html())
        if mimdata.hasText():
            self.save_text(mimdata.text())

    def data_dir_exists(self):
        if not os.path.isdir(self.save_dir):
            os.makedirs(self.save_dir)

    def save_image(self, image):
        if image != self.last_image and not self.first_run:      
            self.update_image.emit(image, self.save_image(image))
        self.last_image = image
            
    def save_text(self, text):
        if text != self.last_text and text != "" and not self.first_run:          
            self.update_text.emit(text, self.save.save_text(text))
        self.last_text = text
        
    def save_html(self, html):
        if html != self.last_html and not self.first_run:           
            self.save.save_html(html)
        self.last_html = html