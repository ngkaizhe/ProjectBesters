from PyQt5.QtWidgets import *
from UI.UI import UI
import sys

# main function

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())
