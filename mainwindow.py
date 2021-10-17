from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtWidgets import QLineEdit, QVBoxLayout, QDialog, QListWidgetItem, QListWidget
from PySide6.QtGui import QIcon, QPixmap, QDesktopServices

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(400, 300)
        self.__item_size = 50
        self.__data = {}
        self.__filter = ''
        self.__ctrl_key_action = {Qt.Key_E: self.open_service}

    def init_ui(self):
        self.__init_widget()
        self.__init_layout()

    @property
    def filter(self):
        return self.__filter

    def set_filter(self, filter):
        self.__filter = filter
        self.apply_filter()
            
    def __init_widget(self):
        self.__search_bar = QLineEdit(self)
        self.__search_bar.textChanged.connect(self.set_filter)
        self.__list_widget = QListWidget(self)

    def __init_layout(self):
        self.__layout = QVBoxLayout(self)
        self.__layout.addWidget(self.__search_bar)
        self.__layout.addWidget(self.__list_widget)

    def get_new_item(self, file):
        new_item = QListWidgetItem()
        new_item.setSizeHint(QSize(0, self.__item_size))
        self.__data[file] = new_item
        return new_item

    def apply_filter(self):
        for file, item in self.__data.items():
            text = item.text()
            hide = False if self.filter in text else True
            hide = False if len(self.filter) == 0 else hide
            item.setHidden(hide)

    def add_text_widget(self, text, file):
        new_item = self.get_new_item(file)
        new_item.setText(text)
        self.__list_widget.insertItem(0, new_item)
        self.apply_filter()

    def add_image_widget(self, image, file):
        new_item = self.get_new_item(file)
        pixmap = QPixmap.fromImage(image)
        icon = QIcon(pixmap)
        new_item.setIcon(icon)
        self.__list_widget.insertItem(0, new_item)
        self.apply_filter()

    @property
    def current_file(self):
        if self.current_item:
            for file, item in self.__data.items():
                if item == self.current_item:
                    return file
        return None

    @property
    def current_item(self):
        return self.__list_widget.currentItem()

    def open_service(self, event):
        current_file = self.current_file
        if current_file :
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.current_file))
        
    def keyPressEvent(self, event):
        key = event.key()
        if event.modifiers() == Qt.ControlModifier:
            action = self.__ctrl_key_action.get(key)
            if action :
                action(event)
            else:
                QDialog.keyPressEvent(self, event)
