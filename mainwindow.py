from PySide6 import QtWidgets, QtGui, QtCore

class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.resize(400, 300)
        self.__item_size = 50

    def init_ui(self):
        self.__init_widget()
        self.__init_layout()
            
    def __init_widget(self):
        self.__list_widget = QtWidgets.QListWidget(self)

    def __init_layout(self):
        self.__layout = QtWidgets.QHBoxLayout(self)
        self.__layout.addWidget(self.__list_widget)

    @property
    def new_item(self):
        new_item = QtWidgets.QListWidgetItem()
        new_item.setSizeHint(QtCore.QSize(0, self.__item_size))
        return new_item

    def add_text_widget(self, text):
        new_item = self.new_item
        new_item.setText(text)
        self.__list_widget.insertItem(0, new_item)

    def add_image_widget(self, image):
        new_item = self.new_item
        pixmap = QtGui.QPixmap.fromImage(image)
        icon = QtGui.QIcon(pixmap)
        new_item.setIcon(icon)
        self.__list_widget.insertItem(0, new_item)