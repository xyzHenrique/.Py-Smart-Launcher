from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor, QPalette 

class Color(QtWidgets.QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        
        self.setAutoFillBackground(True)

        palette = self.palette()

        palette.setColor(QPalette.Window, QColor(color))
        
        self.setPalette(palette)

class Application(QtWidgets.QMainWindow): 
    def __init__(self):
        super(Application, self).__init__()
        
        self.setFixedSize(600, 400)
        self.setWindowTitle("application settings")

        """
        layout

        0,0 | 0,1 | 0,2 | 0,3
        1,0 | 1,1 | 1,2 | 1,3
        2,0 | 2,1 | 2,2 | 2,3
        3,0 | 3,1 | 3,2 | 3,3
        """
        self.layout = QtWidgets.QGridLayout()

        self.handle_checkbox()
        self.handle_button()

        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def handle_checkbox(self):
        self.checkbox_m1 = QtWidgets.QCheckBox("monitor-1", self)
        self.checkbox_m2 = QtWidgets.QCheckBox("monitor-2", self)
        self.checkbox_m3 = QtWidgets.QCheckBox("monitor-3", self)
        self.checkbox_m4 = QtWidgets.QCheckBox("monitor-4", self)
        self.checkbox_m5 = QtWidgets.QCheckBox("monitor-5", self)

        self.layout.addWidget(QtWidgets.QLineEdit(self), 0, 1)
        self.layout.addWidget(self.checkbox_m1, 0, 0)
        self.layout.addWidget(QtWidgets.QLineEdit(self))
        self.layout.addWidget(self.checkbox_m2, 1, 0)
        self.layout.addWidget(QtWidgets.QLineEdit(self))
        self.layout.addWidget(self.checkbox_m3, 1, 0)
        self.layout.addWidget(self.checkbox_m4, 2, 0)
        self.layout.addWidget(self.checkbox_m5)

    def handle_button(self):
        pass

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = Application()
    gui.show()
    
    sys.exit(app.exec_())