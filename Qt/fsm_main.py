
import os
import sys
import time


from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QInputDialog, QLineEdit

try:
    from PyQt5 import uic
    ui_dir = os.path.dirname(os.path.realpath(__file__))
    FSMainWindow = uic.loadUiType(os.path.join(ui_dir, 'ui', 'FSMigrationMain.ui'))[0]
except ImportError:
    # uic module is not installed with PyQt library
    # use precompiled ui interface
    from ui.fsm_main_window import Ui_FSMainWindow as FSMainWindow

class App(QMainWindow, FSMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Migration Tool")
        self.show()
        self.btn_migrate.clicked.connect(self.on_click_migrate)
        self.btn_cancel.clicked.connect(self.on_click_cancel)


    def on_click_migrate(self):
        print("Migration started..")
        self.get_text(self.lineEdit_src)
        self.statusBar.setText('Message in statusbar on Migration start')


    def on_click_cancel(self):
        print("On click event")
        self.statusBar.showMessage('Message in statusbar on Cancel')
        pass
        #self.set_text(self.test_log, "Canceled by user")

        # for i in range(100):
        #     self.progressBar_src.value = i
        #     self.progressBar_dest.value = i + 5


    def set_text(self, ui_obj, text):
        self.ui_obj.setText(text)

    def get_text(self, text_obj):
        print(text_obj.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

"""  
Constant	Value	Description
QLineEdit.Normal	            0	Display characters as they are entered. This is the default.
QLineEdit.NoEcho	            1	Do not display anything. This may be appropriate for passwords where even the length of the password should be kept secret.
QLineEdit.Password	            2	Display asterisks instead of the characters actually entered.
QLineEdit.PasswordEchoOnEdit	3	
"""