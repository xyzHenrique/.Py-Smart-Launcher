from PyQt5 import QtCore, QtWidgets 

class MyFirstGUI(QtWidgets.QDialog): 

    def __init__(self):
        super(MyFirstGUI, self).__init__()
        self.setFixedSize(600, 400)
        self.setWindowTitle("application settings")

        self.layout = QtWidgets.QHBoxLayout(self)

        self.handle_checkbox()
        self.handle_button()

    def handle_checkbox(self):
        self.checkbox_m1 = QtWidgets.QCheckBox("monitor-1", self)
        self.checkbox_m2 = QtWidgets.QCheckBox("monitor-2", self)
        self.checkbox_m3 = QtWidgets.QCheckBox("monitor-3", self)
        self.checkbox_m4 = QtWidgets.QCheckBox("monitor-4", self)
        self.checkbox_m5 = QtWidgets.QCheckBox("monitor-5", self)

        self.layout.addWidget(self.checkbox_m1)
        self.layout.addWidget(self.checkbox_m2)
        self.layout.addWidget(self.checkbox_m3)
        self.layout.addWidget(self.checkbox_m4)
        self.layout.addWidget(self.checkbox_m5)


    def handle_button(self):
        self.buttonBox = QtWidgets.QDialogButtonBox(self) 
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Apply)

        self.layout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = MyFirstGUI()
    gui.show()
    
    sys.exit(app.exec_())