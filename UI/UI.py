from PyQt5.QtWidgets import (QWidget, QPushButton, QGridLayout, QLabel,
                             QPlainTextEdit, QHBoxLayout, QVBoxLayout,
                             QApplication, QSizePolicy, QComboBox, QLineEdit,
                             QFileDialog, QListWidget)
from PyQt5.QtGui import (QResizeEvent, QFont)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import os
from Manager import Manager, Methods
import re
from typing import List
import numpy as np
from arrai.arrai import Arrai
from Equation import Equation
from method.golden_section import build_var_dict


class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.width: any = None
        self.height: any = None

        self.input_open_button: QPushButton = None
        self.input_clear_button: QPushButton = None
        self.input_list: QListWidget = None
        self.input_input_label: QLabel = None

        self.method_calculate_button: QPushButton = None
        self.method_reset_button: QPushButton = None
        self.method_combobox: QComboBox = None
        self.method_method_used_label: QLabel = None
        self.method_intial_interval_textbox: QPlainTextEdit = None

        self.output_save_button: QPushButton = None
        self.output_clear_button: QPushButton = None
        self.output_textbox: QPlainTextEdit = None
        self.output_output_label: QLabel = None

        # 3d
        self.figure1 = plt.figure()
        self.canvas1 = FigureCanvas(self.figure1)

        # 2d
        self.figure2 = plt.figure()
        self.canvas2 = FigureCanvas(self.figure2)

        # graph error message box
        self.graph_error_texbox: QPlainTextEdit = None

        self.grid_layout: QGridLayout = None

        self.hbox1: QHBoxLayout = None
        self.hbox2: QHBoxLayout = None
        self.hbox: QHBoxLayout = None
        self.vbox: QVBoxLayout = None

        self.open_file_location: str = os.path.dirname(os.path.abspath(__file__))
        self.save_file_location: str = os.path.dirname(os.path.abspath(__file__))

        self.methods = list(Methods.keys())

        self.initUI()

    def initUI(self):
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.grid_layout.setHorizontalSpacing(50)

        # create 5 blocks
        self.create_input_block()
        self.create_method_used_block()
        self.create_output_block()
        self.create_graph_block()

        self.setGeometry(170, 100, 1600, 75E0)
        #self.setMinimumSize(1600, 500)
        self.setWindowTitle('Project2-Optimization')

        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()
        self.show()

    def create_input_block(self):

        self.input_open_button = QPushButton("open")
        self.input_open_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.input_open_button.clicked.connect(self.open_file_dialog)

        self.input_clear_button = QPushButton("clear")
        self.input_clear_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.input_clear_button.clicked.connect(self.input_clear)

        self.input_input_label = QLabel('Input:')

        input_h_box = QHBoxLayout()
        input_h_box.addWidget(self.input_open_button)
        input_h_box.addSpacing(50)
        input_h_box.addWidget(self.input_clear_button)

        self.input_list = QListWidget()

        input_v_box = QVBoxLayout()
        input_v_box.addWidget(self.input_input_label)
        input_v_box.addWidget(self.input_list)

        input_v_box.addLayout(input_h_box)
        self.grid_layout.addLayout(input_v_box, 0, 0)

    def create_method_used_block(self):
        # Combo Box to be used
        self.method_combobox = QComboBox(self)
        self.method_combobox.addItems(self.methods)

        # Buttons to be used
        self.method_reset_button = QPushButton("reset")
        self.method_reset_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.method_reset_button.clicked.connect(self.method_reset)

        self.method_calculate_button = QPushButton("calculate")
        self.method_calculate_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.method_calculate_button.clicked.connect(self.method_calculate)

        # Qlabel to be used
        self.method_method_used_label = QLabel('Method Used:')
        self.method_intial_interval_textbox = QPlainTextEdit()

        method_h2_box = QHBoxLayout()
        method_h2_box.addWidget(self.method_reset_button)
        method_h2_box.addWidget(self.method_calculate_button)

        method_v_box = QVBoxLayout()
        method_v_box.addWidget(self.method_method_used_label)
        method_v_box.addWidget(self.method_combobox)
        method_v_box.addWidget(self.method_intial_interval_textbox)

        method_v_box.addLayout(method_h2_box)
        self.grid_layout.addLayout(method_v_box, 0, 1)

    def create_output_block(self):
        self.output_textbox = QPlainTextEdit(QWidget().resize(640, 480))
        self.output_textbox.setReadOnly(True)

        self.output_save_button = QPushButton("save")
        self.output_save_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.output_save_button.clicked.connect(self.save_file_dialog)

        self.output_clear_button = QPushButton("clear")
        self.output_clear_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.output_clear_button.clicked.connect(self.output_clear)

        self.output_output_label = QLabel('Output:')

        output_h_box = QHBoxLayout()
        output_h_box.addWidget(self.output_save_button)
        output_h_box.addWidget(self.output_clear_button)

        output_v_box = QVBoxLayout()
        output_v_box.addWidget(self.output_output_label)
        output_v_box.addWidget(self.output_textbox)

        output_v_box.addLayout(output_h_box)
        self.grid_layout.addLayout(output_v_box, 1, 0, 1, 2)

    def create_graph_block(self):
        ''' plot some random stuff '''
        self.figure1.suptitle('3d')
        self.figure2.suptitle('2d')

        self.canvas1.draw()
        self.canvas2.draw()
        # self.figure2.legend()

        self.graph_error_texbox = QPlainTextEdit('Default graph(NULL)')
        self.graph_error_texbox.setReadOnly(True)
        self.graph_error_texbox.setMinimumSize(640, 110)

        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()

        self.hbox1.addWidget(self.canvas1)
        self.hbox2.addWidget(self.canvas2)
        self.hbox.addLayout(self.hbox1)
        self.hbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.graph_error_texbox)

        self.grid_layout.addLayout(self.vbox, 0, 2, 2, 2)

    def open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", self.open_file_location, "Text Files (*.txt)")
        temp_pos = filename.rfind('/')
        if temp_pos:
            self.open_file_location = filename[: temp_pos + 1]

        if filename:
            with open(filename, 'rb') as file:
                read_data = file.read()
                udatabtype = read_data.decode("utf-8")
                asciidatabtype = udatabtype.encode("ascii", "ignore")
                asciidata =asciidatabtype.decode("ascii")
                read_data_list = asciidata.splitlines()
                self.input_list.addItems(read_data_list)

    def save_file_dialog(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", self.save_file_location,
                                                  "Text Files (*.txt)")
        temp_pos = filename.rfind('/')
        self.save_file_location = filename[: temp_pos + 1]

        if filename:
            with open(filename, 'w') as file:
                file.write(self.output_textbox.toPlainText())
            self.output_clear()

    def input_clear(self):
        self.input_list.clear()

    def output_clear(self):
        # clear textbox
        self.output_textbox.clear()
        # clear graph
        ''' clear windows '''
        plt.figure(1)
        plt.clf()
        plt.figure(2)
        plt.clf()
        plt.close('all')

        ''' plot some random stuff '''
        self.figure1 = plt.figure()
        self.figure2 = plt.figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.canvas2 = FigureCanvas(self.figure2)

        self.figure1.suptitle('3d')
        self.figure2.suptitle('2d')

        self.canvas1.draw()
        self.canvas2.draw()

        self.grid_layout.removeItem(self.hbox1)
        self.grid_layout.removeItem(self.hbox2)
        self.grid_layout.removeItem(self.hbox)
        self.grid_layout.removeItem(self.vbox)

        self.graph_error_texbox.setPlainText('Default graph(NULL)')

        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()

        self.hbox1.addWidget(self.canvas1)
        self.hbox2.addWidget(self.canvas2)
        self.hbox.addLayout(self.hbox1)
        self.hbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.graph_error_texbox)

        self.grid_layout.addLayout(self.vbox, 0, 2, 2, 2)

    def method_reset(self):
        self.method_intial_interval_textbox.setPlainText('')
        self.method_combobox.setCurrentIndex(0)

    def method_calculate(self):
        initial_interval = self.method_intial_interval_textbox.toPlainText()
        method = self.method_combobox.currentText()
        equation_item = self.input_list.currentItem()

        if equation_item is None:
            self.output_textbox.setPlainText('No equation string detected!\n')
            return

        elif method == 'None----':
            self.output_textbox.setPlainText('Method couldnt be None\n')
            return

        elif initial_interval == '':
            self.output_textbox.setPlainText('No initial point\n')
            return

        # global variables
        equation_str: str = None
        initial_point: List[float] = None
        intervals: List[List[float]] = None
        answer : str = None
        Xs: List[Arrai] = None
        vars_form : List[str] = None

        # exception added
        try:
            equation_str = equation_item.text()
            # get initial point and intervals
            initial_point, vars_form, intervals = get_ip_intervals(initial_interval)

            # manager = Manager(equation_str, vars_form, method, initial_point, intervals)
            manager = Manager(equation_str=equation_str, vars_form=vars_form, method_name=method,
                              initial_point=initial_point, intervals=intervals)
            answer, Xs = manager.run()

            # write answer to output
            self.output_textbox.setPlainText(answer)

        except Exception as explosion:
            answer = explosion.args[0]
            self.output_textbox.setPlainText(answer)

        try:
            # draw out graph
            draw_graph(self, equation_str, vars_form, Xs, intervals)

        # catch graph drawing exception
        except:
            self.graph_error_texbox.setPlainText('Error while building graph!\n Current Equation: %s' % equation_str)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        HeightIncreasement = self.frameGeometry().height() - self.height
        temp_size = 30

        if abs(HeightIncreasement) - temp_size >= 0:
            # no pointer could be used in python
            self.change_font(self.input_input_label, HeightIncreasement / temp_size)
            self.change_font(self.method_method_used_label, HeightIncreasement / temp_size)
            self.change_font(self.output_output_label, HeightIncreasement / temp_size)
            self.change_font(self.input_open_button, HeightIncreasement / temp_size)
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


def get_ip_intervals(initial_interval: str):
    initial_interval = initial_interval.split('\n', 1)

    # initial point parts
    initial_point_list = re.split(r'[:=]', initial_interval[0].replace(" ", ""))
    # now initial_point_list contains 3 elements, which is 'initial' , [var..], [initial_point..]
    vars_form = re.findall(r'\w', initial_point_list[1])
    initial_point = list_string_float(re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', initial_point_list[2]))

    # interval parts
    intervals = []
    interval_list = []

    # if interval spotted
    if len(initial_interval) >= 2:
        interval_list = initial_interval[1].splitlines()

    if len(interval_list) >= 2:
        for i in range(len(vars_form)):
            intervals.append(list_string_float(re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', interval_list[i+1])))

    return initial_point, vars_form, intervals


def list_string_float(string_list: List[str]):
    float_list = []
    for i in range(len(string_list)):
        float_list.append(float(string_list[i]))
    return float_list


def draw_graph(ui: UI, equation_str: str, vars_form: List[str], all_points: List[Arrai], intervals: List[List[float]]):
    ''' clear windows '''
    plt.figure(1)
    plt.clf()
    plt.figure(2)
    plt.clf()
    plt.close('all')

    # # 3d test
    # equation_str = 'x^2+y^2'
    # eqn = Equation(equation_str)
    # vars_form = ['x', 'y']
    # intervals = [[-10, 10], [-5, 70]]
    # all_points = [Arrai([1, 2]), Arrai([2, 8]), Arrai([-2, 50]), Arrai([0, 20])]
    #
    # # 2d test
    # equation_str = 'x^2'
    # eqn = Equation(equation_str)
    # vars_form = ['x']
    # intervals = [[-100, 100]]
    # all_points = [Arrai([-75]), Arrai([-50]), Arrai([-25]), Arrai([0])]
    #
    # # exception test
    # equation_str = 'x^2'
    # eqn = Equation(equation_str)
    # vars_form = ['x', 'y'] # wrong
    # intervals = [[-100, 100]]
    # all_points = [Arrai([-75]), Arrai([-50]), Arrai([-25]), Arrai([0])]

    eqn = Equation(equation_str)

    # 3d
    if len(vars_form) == 2:
        # check intervals, if no intervals get it by checking all points and get
        # the smallest x and y, and the largest x and y, the set as intervals
        if len(intervals) == 0:
            smallest_x = float(all_points[0].array[0][0])
            largest_x = float(all_points[0].array[0][0])
            smallest_y = float(all_points[0].array[1][0])
            largest_y = float(all_points[0].array[1][0])

            for i in all_points:
                if i.array[0][0] < smallest_x:
                    smallest_x = float(i.array[0][0])
                if i.array[0][0] > largest_x:
                    largest_x = float(i.array[0][0])
                if i.array[1][0] < smallest_y:
                    smallest_y = float(i.array[1][0])
                if i.array[1][0] > largest_y:
                    largest_y = float(i.array[1][0])

            # get lower bound, upper bound for x
            # get lower bound, upper bound for y
            middle_x = largest_x - ((largest_x - smallest_x) / 2)
            lbx = middle_x - ((middle_x - smallest_x) * 2)
            ubx = middle_x + ((largest_x - middle_x) * 2)

            middle_y = largest_y - ((largest_y - smallest_y) / 2)
            lby = middle_y - ((middle_y - smallest_y) * 2)
            uby = middle_y + ((largest_y - middle_y) * 2)

            intervals = [[lbx, ubx], [lby, uby]]

        # plot1 (3D)
        ui.figure1 = plt.figure()
        ui.canvas1 = FigureCanvas(ui.figure1)

        total_cut = 15.0
        marker_size = 5

        ui.figure1.suptitle('3d')
        ax1 = ui.figure1.add_subplot(111, projection='3d')
        x = np.arange(intervals[0][0], intervals[0][1], (intervals[0][1] - intervals[0][0]) / total_cut)
        y = np.arange(intervals[1][0], intervals[1][1], (intervals[1][1] - intervals[1][0]) / total_cut)
        X, Y = np.meshgrid(x, y)

        # testing with np here
        # z_list2 = X ** 2 + Y ** 2

        z_list = []
        for i in range(X.shape[0]):
            row = []
            for j in range(X.shape[1]):
                vars_dict = build_var_dict(vars_form, [X[i][j], Y[i][j]])
                ans = eqn.eval_normal_form(vars_dict)
                row.append(float(ans))
            z_list.append(row)

        z_list = np.array(z_list)
        zs = np.array(z_list)
        Z = zs.reshape(X.shape)
        ax1.plot_surface(X, Y, Z)
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_zlabel('z')

        # draw our result
        own_x_list = []
        for i in all_points:
            own_x_list.append(float(i.array[0][0]))

        own_y_list = []
        for i in all_points:
            own_y_list.append(float(i.array[1][0]))

        own_z_list = []
        for i in range(len(all_points)):
            vars_dict = build_var_dict(vars_form, [own_x_list[i], own_y_list[i]])
            ans = eqn.eval_normal_form(vars_dict)
            own_z_list.append(float(ans))

        own_x_np = np.array(own_x_list)
        own_y_np = np.array(own_y_list)
        own_z_np = np.array(own_z_list)
        ax1.plot(own_x_np, own_y_np, own_z_np, 'mo-', zorder=100, markersize=marker_size, linewidth=5)

        # plot2 (2d)
        ui.figure2 = plt.figure()
        ui.canvas2 = FigureCanvas(ui.figure2)
        ui.figure2.suptitle('2d')
        ax2 = plt.figure(2).add_subplot(111)
        ax2.contour(X, Y, Z)
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')

        ax2.plot(own_x_np, own_y_np, 'ro-', markersize=3)
        ax2.annotate('initial point', xy=(own_x_np[0], own_y_np[0]))
        ax2.annotate('local minimum point', xy=(own_x_np[len(own_x_np)-1], own_y_np[len(own_y_np)-1]))

        ui.canvas1.draw()
        ui.canvas2.draw()

        ui.grid_layout.removeItem(ui.hbox1)
        ui.grid_layout.removeItem(ui.hbox2)
        ui.grid_layout.removeItem(ui.hbox)
        ui.grid_layout.removeItem(ui.vbox)

        ui.graph_error_texbox.setPlainText('Current Equation: %s\n'
                                           'X interval: %s\nY interval: %s\n'
                                           'Initial point:%s\nMinimum point:%s\n'
                                           'Minimum value:%s\n' %
                                           (equation_str, intervals[0], intervals[1], [own_x_np[0], own_y_np[0]], [own_x_np[len(own_x_np)-1], own_y_np[len(own_y_np)-1]], own_z_np[len(own_z_np)-1]))

        ui.hbox1 = QHBoxLayout()
        ui.hbox2 = QHBoxLayout()
        ui.hbox = QHBoxLayout()
        ui.vbox = QVBoxLayout()

        ui.hbox1.addWidget(ui.canvas1)
        ui.hbox2.addWidget(ui.canvas2)
        ui.hbox.addLayout(ui.hbox1)
        ui.hbox.addLayout(ui.hbox2)
        ui.vbox.addLayout(ui.hbox)
        ui.vbox.addWidget(ui.graph_error_texbox)

        ui.grid_layout.addLayout(ui.vbox, 0, 2, 2, 2)

    # 2d
    elif len(vars_form) == 1:
        # check intervals
        if len(intervals) == 0:
            smallest_x = float(all_points[0].array[0][0])
            largest_x = float(all_points[0].array[0][0])

            for i in all_points:
                if i.array[0][0] < smallest_x:
                    smallest_x = float(i.array[0][0])
                if i.array[0][0] > largest_x:
                    largest_x = float(i.array[0][0])

            # get lower bound, upper bound for x
            # get lower bound, upper bound for y
            middle_x = largest_x - ((largest_x - smallest_x) / 2)
            lbx = middle_x - ((middle_x - smallest_x) * 2)
            ubx = middle_x + ((largest_x - middle_x) * 2)

            intervals = [[lbx, ubx]]

        # plot1 (3D)
        ui.figure1 = plt.figure()
        ui.canvas1 = FigureCanvas(ui.figure1)
        ui.figure1.suptitle('3d')

        total_cut = 100.0
        marker_size = 3

        # plot2 (2d)
        # draw our result
        own_x_list = []
        for i in all_points:
            own_x_list.append(float(i.array[0][0]))
        own_x_np = np.array(own_x_list)

        own_y_list = []
        for i in own_x_list:
            vars_dict = build_var_dict(vars_form, [i])
            ans = eqn.eval_normal_form(vars_dict)
            own_y_list.append(float(ans))
        own_y_np = np.array(own_y_list)

        ui.figure2 = plt.figure()
        ui.canvas2 = FigureCanvas(ui.figure2)
        ui.figure2.suptitle('2d')
        ax2 = plt.figure(2).add_subplot(111)

        X = np.arange(intervals[0][0], intervals[0][1], (intervals[0][1] - intervals[0][0]) / total_cut)

        y_list = []
        for i in range(X.shape[0]):
            vars_dict = build_var_dict(vars_form, [X[i]])
            ans = eqn.eval_normal_form(vars_dict)
            y_list.append(float(ans))

        Y = np.array(y_list)

        ax2.plot(X, Y)
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')

        ax2.plot(own_x_np, own_y_np, 'ro-', markersize=marker_size)
        ax2.annotate('initial point', xy=(own_x_np[0], own_y_np[0]))
        ax2.annotate('local minimum point', xy=(own_x_np[len(own_x_np) - 1], own_y_np[len(own_y_np) - 1]))

        ui.canvas1.draw()
        ui.canvas2.draw()

        ui.grid_layout.removeItem(ui.hbox1)
        ui.grid_layout.removeItem(ui.hbox2)
        ui.grid_layout.removeItem(ui.hbox)
        ui.grid_layout.removeItem(ui.vbox)

        ui.graph_error_texbox.setPlainText('Current Equation: %s\n'
                                           'X interval: %s\n'
                                           'Initial point:%s\nMinimum point:%s\n'
                                           'Minimum value:%s\n' %
                                           (equation_str, intervals[0], [own_x_np[0]], [own_x_np[len(own_x_np)-1]], own_y_np[len(own_y_np)-1]))

        ui.hbox1 = QHBoxLayout()
        ui.hbox2 = QHBoxLayout()
        ui.hbox = QHBoxLayout()
        ui.vbox = QVBoxLayout()

        ui.hbox1.addWidget(ui.canvas1)
        ui.hbox2.addWidget(ui.canvas2)
        ui.hbox.addLayout(ui.hbox1)
        ui.hbox.addLayout(ui.hbox2)
        ui.vbox.addLayout(ui.hbox)
        ui.vbox.addWidget(ui.graph_error_texbox)

        ui.grid_layout.addLayout(ui.vbox, 0, 2, 2, 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())



