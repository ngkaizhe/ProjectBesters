from PyQt5.QtWidgets import (QWidget, QPushButton, QGridLayout, QLabel,
                             QPlainTextEdit, QHBoxLayout, QVBoxLayout,
                             QApplication, QSizePolicy, QComboBox, QLineEdit)
import sys
import os


class UI(QWidget):
    def __init__(self):
        super().__init__()

        self.input_open_button: QPushButton = None
        self.input_clear_button: QPushButton = None
        self.input_set_button: QPushButton = None
        self.input_textbox: QPlainTextEdit = None

        self.method_calculate_button: QPushButton = None
        self.method_reset_button: QPushButton = None
        self.method_combobox: QComboBox = None
        self.method_min_range: QLineEdit = None
        self.method_max_range: QLineEdit = None

        self.output_save_button: QPushButton = None
        self.output_clear_button: QPushButton = None
        self.output_textbox: QPlainTextEdit = None

        self.grid_layout: QGridLayout = None

        self.methods = ["None----", "Powell's Method", "Newton Method", "Steep Descent Algorithm",
                        "Quasi-Newton Method", "Conjugate Gradient Methods"]

        self.initUI()

    def initUI(self):
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.grid_layout.setHorizontalSpacing(50)

        # create 3 blocks
        self.create_input_block()
        self.create_method_used_block()
        self.create_output_block()

        self.setGeometry(500, 300, 300, 300)
        self.setWindowTitle('Project2-Optimization')
        self.show()

    def create_input_block(self):

        self.input_open_button = QPushButton("open")
        self.input_open_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.input_set_button = QPushButton("set")
        self.input_set_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.input_clear_button = QPushButton("clear")
        self.input_clear_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        input_h_box = QHBoxLayout()
        input_h_box.addWidget(self.input_open_button)
        input_h_box.addWidget(self.input_set_button)
        input_h_box.addWidget(self.input_clear_button)

        self.input_textbox = QPlainTextEdit(QWidget().resize(640, 480))

        input_v_box = QVBoxLayout()
        input_v_box.addWidget(QLabel('Input'))
        input_v_box.addWidget(self.input_textbox)

        input_v_box.addLayout(input_h_box)
        self.grid_layout.addLayout(input_v_box, 0, 0)

    def create_method_used_block(self):
        # Combo Box to be used
        self.method_combobox = QComboBox(self)
        self.method_combobox.addItems(self.methods)

        # Buttons to be used
        self.method_reset_button = QPushButton("reset")
        self.method_reset_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.method_calculate_button = QPushButton("calculate")
        self.method_calculate_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Range textbox to be used
        self.method_min_range = QLineEdit(self)
        self.method_min_range.setFixedSize(70, 20)
        self.method_max_range = QLineEdit(self)
        self.method_max_range.setFixedSize(70, 20)

        method_h1_box = QHBoxLayout()
        method_h1_box.addStretch(1)
        method_h1_box.addWidget(self.method_min_range)
        method_h1_box.addStretch(1)
        method_h1_box.addWidget(QLabel('~'))
        method_h1_box.addStretch(1)
        method_h1_box.addWidget(self.method_max_range)
        method_h1_box.addStretch(1)

        method_h2_box = QHBoxLayout()
        method_h2_box.addWidget(self.method_reset_button)
        method_h2_box.addWidget(self.method_calculate_button)

        method_v_box = QVBoxLayout()
        method_v_box.addWidget(QLabel('Method Used:'))
        method_v_box.addWidget(self.method_combobox)
        method_v_box.addWidget(QLabel('Range:'))

        method_v_box.addLayout(method_h1_box)
        method_v_box.addLayout(method_h2_box)
        self.grid_layout.addLayout(method_v_box, 0, 1)

    def create_output_block(self):

        self.output_save_button = QPushButton("save")
        self.output_save_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.output_clear_button = QPushButton("clear")
        self.output_clear_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        output_h_box = QHBoxLayout()
        output_h_box.addWidget(self.output_save_button)
        output_h_box.addWidget(self.output_clear_button)

        self.output_textbox = QPlainTextEdit(QWidget().resize(640, 480))

        output_v_box = QVBoxLayout()
        output_v_box.addWidget(QLabel('Output'))
        output_v_box.addWidget(self.output_textbox)

        output_v_box.addLayout(output_h_box)
        self.grid_layout.addLayout(output_v_box, 1, 0, 1, 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())