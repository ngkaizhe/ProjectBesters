from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QSizePolicy)
import sys
import os


class UI(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        okButton = QPushButton("open")
        okButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        setButton = QPushButton("set")
        setButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        clearButton = QPushButton("clear")
        clearButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        hbox = QHBoxLayout()

        hbox.addWidget(okButton)
        hbox.addWidget(setButton)
        hbox.addWidget(clearButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())