from PyQt5.QtWidgets import (QWidget, QPushButton, QGridLayout, QLabel,
                             QPlainTextEdit, QHBoxLayout, QVBoxLayout,
                             QApplication, QSizePolicy, QComboBox, QLineEdit,
                             QFileDialog)
from PyQt5.QtGui import (QResizeEvent, QFont)
import sys
import os


class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.width: any = None
        self.height: any = None

        self.input_open_button: QPushButton = None
        self.input_clear_button: QPushButton = None
        self.input_set_button: QPushButton = None
        self.input_textbox: QPlainTextEdit = None
        self.input_input_label: QLabel = None

        self.method_calculate_button: QPushButton = None
        self.method_reset_button: QPushButton = None
        self.method_combobox: QComboBox = None
        self.method_min_range: QLineEdit = None
        self.method_max_range: QLineEdit = None
        self.method_method_used_label: QLabel = None
        self.method_range_label: QLabel = None
        self.method_dash_label: QLabel = None

        self.output_save_button: QPushButton = None
        self.output_clear_button: QPushButton = None
        self.output_textbox: QPlainTextEdit = None
        self.output_output_label: QLabel = None

        self.grid_layout: QGridLayout = None

        self.open_file_location: str = os.path.dirname(os.path.abspath(__file__))
        self.save_file_location: str = os.path.dirname(os.path.abspath(__file__))

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

        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()
        self.show()

    def create_input_block(self):

        self.input_open_button = QPushButton("open")
        self.input_open_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.input_open_button.clicked.connect(self.open_file_dialog)

        self.input_set_button = QPushButton("set")
        self.input_set_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.input_clear_button = QPushButton("clear")
        self.input_clear_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.input_input_label = QLabel('Input:')

        input_h_box = QHBoxLayout()
        input_h_box.addWidget(self.input_open_button)
        input_h_box.addWidget(self.input_set_button)
        input_h_box.addWidget(self.input_clear_button)

        self.input_textbox = QPlainTextEdit(QWidget().resize(640, 480))

        input_v_box = QVBoxLayout()
        input_v_box.addWidget(self.input_input_label)
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

        # Qlabel to be used
        self.method_method_used_label = QLabel('Method Used:')
        self.method_range_label = QLabel('Range:')
        self.method_dash_label = QLabel('~')

        method_h1_box = QHBoxLayout()
        method_h1_box.addStretch(1)
        method_h1_box.addWidget(self.method_min_range)
        method_h1_box.addStretch(1)
        method_h1_box.addWidget(self.method_dash_label)
        method_h1_box.addStretch(1)
        method_h1_box.addWidget(self.method_max_range)
        method_h1_box.addStretch(1)

        method_h2_box = QHBoxLayout()
        method_h2_box.addWidget(self.method_reset_button)
        method_h2_box.addWidget(self.method_calculate_button)

        method_v_box = QVBoxLayout()
        method_v_box.addWidget(self.method_method_used_label)
        method_v_box.addWidget(self.method_combobox)
        method_v_box.addWidget(self.method_range_label)

        method_v_box.addLayout(method_h1_box)
        method_v_box.addLayout(method_h2_box)
        self.grid_layout.addLayout(method_v_box, 0, 1)

    def create_output_block(self):

        self.output_save_button = QPushButton("save")
        self.output_save_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.output_save_button.clicked.connect(self.save_file_dialog)

        self.output_clear_button = QPushButton("clear")
        self.output_clear_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.output_output_label = QLabel('Output:')

        output_h_box = QHBoxLayout()
        output_h_box.addWidget(self.output_save_button)
        output_h_box.addWidget(self.output_clear_button)

        self.output_textbox = QPlainTextEdit(QWidget().resize(640, 480))

        output_v_box = QVBoxLayout()
        output_v_box.addWidget(self.output_output_label)
        output_v_box.addWidget(self.output_textbox)

        output_v_box.addLayout(output_h_box)
        self.grid_layout.addLayout(output_v_box, 1, 0, 1, 2)

    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", self.open_file_location, "Text Files (*.txt)")
        temp_pos = filename.rfind('/')
        if temp_pos:
            self.open_file_location = filename[: temp_pos + 1]

        if filename:
            with open(filename, 'r') as file:
                read_data = file.read()
            self.input_textbox.setPlainText(read_data)

    def save_file_dialog(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", self.save_file_location,
                                                  "Text Files (*.txt)")
        temp_pos = filename.rfind('/')
        self.save_file_location = filename[: temp_pos + 1]

        if filename:
            with open(filename, 'w') as file:
                file.write(self.output_textbox.toPlainText())

            self.output_textbox.clear()

    def update(self) -> None:
        self.input_textbox.setPlainText('update called')

    def resizeEvent(self, a0: QResizeEvent) -> None:
        HeightIncreasement = self.frameGeometry().height() - self.height
        temp_size = 30

        if abs(HeightIncreasement) - temp_size >= 0:
            # no pointer could be used in python
            self.change_font(self.input_input_label, HeightIncreasement / temp_size)
            self.change_font(self.method_range_label, HeightIncreasement / temp_size)
            self.change_font(self.method_method_used_label, HeightIncreasement / temp_size)
            self.change_font(self.output_output_label, HeightIncreasement / temp_size)
            self.change_font(self.method_dash_label, HeightIncreasement / temp_size)
            self.change_font(self.input_open_button, HeightIncreasement / temp_size)
            self.change_font(self.input_set_button, HeightIncreasement / temp_size)
            self.change_font(self.input_clear_button, HeightIncreasement / temp_size)
            self.change_font(self.method_calculate_button, HeightIncreasement / temp_size)
            self.change_font(self.method_reset_button, HeightIncreasement / temp_size)
            self.change_font(self.output_save_button, HeightIncreasement / temp_size)
            self.change_font(self.output_clear_button, HeightIncreasement / temp_size)
            self.change_font(self.method_combobox, HeightIncreasement / temp_size)

            self.width = self.frameGeometry().width()
            self.height = self.frameGeometry().height()

    @staticmethod
    def change_font(label: QLabel, increasement: int):
        font = label.font()
        font.setPointSize(font.pointSize() + increasement)
        if font.pointSize() > 8:
            label.setFont(font)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())