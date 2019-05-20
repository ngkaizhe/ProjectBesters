from PyQt5.QtWidgets import *
from UI.UI import UI
import sys

# main function

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI('Optimization', 300, 300, 1200, 480)
    sys.exit(app.exec_())
