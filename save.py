from abc import abstractmethod
import os
from datetime import datetime

class Save():
    def __init__(self, save_dir):
        self.save_dir = save_dir

    def get_save_file_name(self, ext):
        file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file_path_name = os.path.join(self.save_dir,file_name) + ext
        rt_file_path_name  = file_path_name
        id = 1
        while os.path.isfile(rt_file_path_name):
            rt_file_path_name = file_path_name + "_" + str(id)
            id = id + 1
        return rt_file_path_name

    @abstractmethod
    def save_image(self, image):
        pass
    
    @abstractmethod
    def save_text(self, text):
        pass
        
    @abstractmethod
    def save_html(self, html):
        pass

class JSonSave(Save):
    def __init__(self,save_dir):
        super().__init__(save_dir)
    
    def save_image(self, image):
        file_name = self.get_save_file_name(".png")
        image.save(file_name, "PNG")
        return file_name
    
    def save_text(self, text):
        file_name = self.get_save_file_name(".txt")
        with open(file_name, "w") as file:
            file.write(text)
        return file_name
        
    def save_html(self, html):
        file_name = self.get_save_file_name(".html")
        with open(file_name, "w") as file:
            file.write(html)
        return file_name