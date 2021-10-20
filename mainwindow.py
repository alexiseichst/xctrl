import PySide6.QtCore as QC
import PySide6.QtWidgets as QW 
import PySide6.QtGui as QG

class MainWindow(QW.QDialog):
    def __init__(self):
        super().__init__()
        self.resize(400, 300)
        self.__item_size = 50
        self.__data = {}
        self.__filter = ''
        self.__ctrl_key_action = {QC.Qt.Key_E: self.open_service}

    def init_ui(self):
        self.__init_widget()
        self.__init_layout()
        self.show()
        self.__list_widget.setFocus()

    @property
    def filter(self):
        return self.__filter

    def set_filter(self, filter):
        self.__filter = filter
        self.apply_filter()
            
    def __init_widget(self):
        self.__search_bar = QW.QLineEdit(self)
        self.__search_bar.textChanged.connect(self.set_filter)
        self.__search_bar.setFocus(QC.Qt.OtherFocusReason)
        self.__list_widget = QW.QListWidget(self)
        self.__list_widget.setFocus(QC.Qt.OtherFocusReason)
        
    def __init_layout(self):
        self.__layout = QW.QVBoxLayout(self)
        self.__layout.addWidget(self.__search_bar)
        self.__layout.addWidget(self.__list_widget)
        self.__sys_icon = QW.QSystemTrayIcon(self)

    def __init_sys_icon(self):
        self.sys_icon = QW.QSystemTrayIcon(self)
        self.__sys_menu = QW.QMenu(self)

    def get_new_item(self, file):
        new_item = QW.QListWidgetItem()
        new_item.setSizeHint(QC.QSize(0, self.__item_size))
        self.__list_widget.insertItem(0, new_item)
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
        self.apply_filter()

    def add_image_widget(self, image, file):
        new_item = self.get_new_item(file)
        pixmap = QG.QSystemTrayIcon.fromImage(image)
        icon = QG.QIcon(pixmap)
        new_item.setIcon(icon)
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
            QW.QDesktopServices.openUrl(QC.QUrl.fromLocalFile(self.current_file))
        
    def keyPressEvent(self, event):
        key = event.key()
        if event.modifiers() == QC.Qt.ControlModifier:
            action = self.__ctrl_key_action.get(key)
            if action : action(event)
        else:
            QW.QDialog.keyPressEvent(self, event)