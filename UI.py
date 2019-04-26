from PyQt5.QtWidgets import (QWidget, QPushButton, QGridLayout, QLabel,
                             QPlainTextEdit, QHBoxLayout, QVBoxLayout,
                             QApplication, QSizePolicy)
import sys
import os


class UI(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

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
        vbox.addWidget(QLabel('Input'))
        vbox.addWidget(QPlainTextEdit(QWidget().resize(640, 480)))
        vbox.addLayout(hbox)

        okButton1 = QPushButton("open")
        okButton1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        setButton1 = QPushButton("set")
        setButton1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        clearButton1 = QPushButton("clear")
        clearButton1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        hbox1 = QHBoxLayout()

        hbox1.addWidget(okButton1)
        hbox1.addWidget(setButton1)
        hbox1.addWidget(clearButton1)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(QLabel('Method Used'))
        vbox1.addWidget(QPlainTextEdit(QWidget().resize(640, 480)))
        vbox1.addLayout(hbox1)

        grid_layout.addLayout(vbox, 0, 0)
        grid_layout.addLayout(vbox1, 0, 1)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())