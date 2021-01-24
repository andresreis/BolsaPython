from PyQt5.QtWidgets import  QWidget, QPushButton,  QGridLayout, QTableWidget, QTableWidgetItem, QGroupBox, QLabel, QVBoxLayout, QShortcut
from PyQt5.QtGui import  QBrush, QColor, QFont, QKeySequence, QIcon
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.patches import Rectangle

import matplotlib as plt
import pandas as pd
import numpy as np

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, self2, fig, ax, parent=None, width=5, height=4, dpi=100):

        fig.get_axes()[1].set_zorder(-100)
        super(MplCanvas, self).__init__(fig)

        self.mpl_connect("button_press_event", self2.graph_click)

class Window(QWidget):                      #A classe window herda todos os métodos
                                            #e atributos de QWidget
    def __init__(self, ativos ,parent=None):
        super(Window, self).__init__()      #Com o super, está iniciando Window
                                            #com o inicializador de Qwidget
        self.ativos = ativos
        self.point1 = 0
        self.point2 = 0
        self.init_window()
        self.init_grid()

    def init_window(self):
        self.setWindowTitle("ProfitReis")
        self.setWindowIcon(QIcon('Icon.png'))

    def createTableAcoes(self):

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.ativos))
        self.tableWidget.setColumnCount(1)

        self.tableWidget.setMinimumWidth(150)
        self.tableWidget.setMaximumWidth(150)
        self.tableWidget.setMinimumHeight(500)
        self.tableWidget.setMaximumHeight(500)

        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Ações"))

        i = 0
        for i in range(len(self.ativos)):
            self.tableWidget.setItem(i,0, QTableWidgetItem(self.ativos[i].nome))
            self.tableWidget.item(i,0).setTextAlignment(Qt.AlignCenter)

        self.tableWidget.itemSelectionChanged.connect(self.acao_click)

    def createBtns(self):
        self.min_btn = QPushButton('60 minutos')
        self.min_btn.setMaximumWidth(80)
        self.min_btn.clicked.connect(self.btn_60)

        self.dia_btn = QPushButton('diário')
        self.dia_btn.setMaximumWidth(80)
        self.dia_btn.clicked.connect(self.btn_d)

        self.sem_btn = QPushButton('semanal')
        self.sem_btn.setMaximumWidth(80)
        self.sem_btn.clicked.connect(self.btn_s)

        self.tra_btn = QPushButton('Traçar')
        self.tra_btn.setMaximumWidth(80)
        self.tra_btn.setCheckable(True)
        self.tra_btn.clicked.connect(self.btn_t)

        self.ope_btn = QPushButton('Operando')
        self.ope_btn.setMaximumWidth(80)
        self.ope_btn.setCheckable(True)
        self.ope_btn.clicked.connect(self.btn_o)

    def createGraph60(self, int = 0, first = False):
        plt.pyplot.close('all')

        x = self.ativos[int].candle_60(250)
        x[0].get_axes()[1].set_zorder(-100)
        if (first == True):
            self.graph = MplCanvas(self, x[0], x[1], width=5, height=4, dpi=100)
            self.toolbar = NavigationToolbar(self.graph, self)
        else:
            self.graph.figure = x[0]
            self.graph.draw()

        self.graph.setMinimumHeight(500)
        self.graph.setMinimumWidth(700)

    def createGraphd(self, int = 0):
        plt.pyplot.close('all')
        x = self.ativos[int].candle_d(250)
        x[0].get_axes()[1].set_zorder(-100)
        self.graph.figure = x[0]
        self.graph.draw()
        self.graph.setMinimumHeight(500)
        self.graph.setMinimumWidth(700)

    def createGraphs(self, int = 0):
        plt.pyplot.close('all')
        x = self.ativos[int].candle_s(250)
        x[0].get_axes()[1].set_zorder(-100)
        self.graph.figure = x[0]
        self.graph.draw()
        self.graph.setMinimumHeight(500)
        self.graph.setMinimumWidth(700)

    def init_grid(self):
        grid = QGridLayout()

        self.createTableAcoes()
        self.createBtns()
        self.createGraph60(first = True)
        self.createGroupBoxes()
        self.createShortCut()

        grid.addWidget(self.tableWidget, 0, 0, 10, 1)
        grid.addWidget(self.min_btn, 10, 0, Qt.AlignCenter)
        grid.addWidget(self.dia_btn, 11, 0, Qt.AlignCenter)
        grid.addWidget(self.sem_btn, 12, 0, Qt.AlignCenter)
        grid.addWidget(self.tra_btn, 12, 8, Qt.AlignCenter)
        grid.addWidget(self.ope_btn, 11, 8, Qt.AlignCenter)
        grid.addWidget(self.graph,0,1,13,1)
        grid.addWidget(self.toolbar,13,1)
        grid.addWidget(self.box1, 0, 8)
        grid.addWidget(self.box2, 1, 8)
        grid.addWidget(self.box3, 2, 8)
        grid.addWidget(self.box4, 3, 8)
        grid.addWidget(self.box5, 4, 8)

        self.grid = grid

        self.setLayout(self.grid)

    def createGroupBoxes(self):
        self.box1 = QGroupBox('Nome do Ativo:')
        self.box1.setMaximumHeight(50)
        self.box1.setAlignment(Qt.AlignCenter)

        self.lab1 = QLabel(self.ativos[0].nome)
        self.lab1.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        self.box1.setLayout(vbox)

        vbox.addWidget(self.lab1)
        #
        self.box2 = QGroupBox('Média diária:')
        self.box2.setMaximumHeight(50)
        self.box2.setAlignment(Qt.AlignCenter)

        self.lab2 = QLabel('')
        self.lab2.setAlignment(Qt.AlignCenter)

        vbox2 = QVBoxLayout()
        self.box2.setLayout(vbox2)

        vbox2.addWidget(self.lab2)
        #
        self.box3 = QGroupBox('Média semanal:')
        self.box3.setMaximumHeight(50)
        self.box3.setAlignment(Qt.AlignCenter)

        self.lab3 = QLabel('')
        self.lab3.setAlignment(Qt.AlignCenter)

        vbox3 = QVBoxLayout()
        self.box3.setLayout(vbox3)

        vbox3.addWidget(self.lab3)
        #
        self.box4 = QGroupBox('Topos e Fundos (diário):')
        self.box4.setMaximumHeight(50)
        self.box4.setAlignment(Qt.AlignCenter)

        self.lab4 = QLabel('')
        self.lab4.setAlignment(Qt.AlignCenter)

        vbox4 = QVBoxLayout()
        self.box4.setLayout(vbox4)

        vbox4.addWidget(self.lab4)
        #
        self.box5 = QGroupBox('%')
        self.box5.setMaximumHeight(50)
        self.box5.setAlignment(Qt.AlignCenter)

        self.lab5 = QLabel('Esperando: Ponto 1')
        self.lab5.setAlignment(Qt.AlignCenter)

        vbox5 = QVBoxLayout()
        self.box5.setLayout(vbox5)

        vbox5.addWidget(self.lab5)

    def createShortCut(self):
        self.short_60 = QShortcut(QKeySequence('Ctrl+F'), self)
        self.short_60.activated.connect(self.btn_60)

        self.short_d = QShortcut(QKeySequence('Ctrl+D'), self)
        self.short_d.activated.connect(self.btn_d)

        self.short_60 = QShortcut(QKeySequence('Ctrl+S'), self)
        self.short_60.activated.connect(self.btn_s)

    def acao_click(self):
        self.tra_btn.setEnabled(True)
        self.tra_btn.setChecked(False)

        row = self.tableWidget.currentItem().row()
        self.createGraphd(row)

        situacoes = self.ativos[row].relatorio(formatado = True)

        if(self.ativos[row].operando):
            self.ope_btn.setChecked(True)
        else:
            self.ope_btn.setChecked(False)

        font = QFont()

        self.lab1.setText(situacoes[0])

        self.lab2.setText(situacoes[1])
        if (situacoes[1] == 'Proximo'):
            font.setBold(True)
        else:
            font.setBold(False)
        self.lab2.setFont(font)

        self.lab3.setText(situacoes[2])
        if (situacoes[2] == 'Acima'):
            self.lab3.setStyleSheet("color: green")
        if (situacoes[2] == 'Abaixo'):
            self.lab3.setStyleSheet("color: red")

        self.lab4.setText(situacoes[3])
        self.lab5.setText('Esperando: Ponto 1')

        self.point1 = 0
        self.point2 = 0

    def graph_click(self, self2):

        if(self2.ydata != None):
            if (self.point1 == 0):
                self.point1 = self2.ydata
                self.point1x = self2.xdata
                self.lab5.setText('Esperando: Ponto 2')
            elif(self.point2 == 0):
                self.point2 = self2.ydata
                self.point2x = self2.xdata
                self.lab5.setText(str(round((self.point2 - self.point1)*100/self.point1,2))+' %')
                if self.tra_btn.isChecked():
                    row = self.tableWidget.currentItem().row()

                    tam = len(self.ativos[row].dados_d[0][:])
                    x1 = tam + self.point1x - 250
                    x2 = tam + self.point2x - 250
                    y1 = self.point1
                    y2 = self.point2
                    self.ativos[row].append_risco(x1, x2, y1, y2)
                    np.save('Tracos/' + self.ativos[row].nome, np.array([x1, x2, y1, y2]))

                    self.createGraphd(row)
            else:
                if self.tra_btn.isChecked():
                    self.tra_btn.setChecked(False)
                self.lab5.setText('Esperando: Ponto 1')
                self.point1 = 0
                self.point2 = 0

    def btn_60(self):
        if (self.tableWidget.selectedItems() != []):
            self.tra_btn.setEnabled(False)

            row = self.tableWidget.currentItem().row()
            self.createGraph60(row)

            self.lab5.setText('Esperando: Ponto 1')
            self.point1 = 0
            self.point2 = 0

    def btn_d(self):
        if (self.tableWidget.selectedItems() != []):
            self.tra_btn.setEnabled(True)

            row = self.tableWidget.currentItem().row()
            self.createGraphd(row)

            self.lab5.setText('Esperando: Ponto 1')
            self.point1 = 0
            self.point2 = 0

    def btn_s(self):
        if (self.tableWidget.selectedItems() != []):
            self.tra_btn.setEnabled(False)

            row = self.tableWidget.currentItem().row()
            self.createGraphs(row)

            self.lab5.setText('Esperando: Ponto 1')
            self.point1 = 0
            self.point2 = 0

    def btn_t(self):
        if self.tra_btn.isChecked():
            if self.point2 != 0:
                self.point1 = 0
                self.point2 = 0
                self.lab5.setText('Esperando: Ponto 1')
        else:
            self.point1 = 0
            self.point2 = 0
            self.lab5.setText('Esperando: Ponto 1')

    def btn_o(self):
        font = QFont()
        row = self.tableWidget.currentItem().row()

        if self.ope_btn.isChecked():
            self.ativos[self.tableWidget.currentItem().row()].operando = True
            font.setBold(True)

        else:
            font.setBold(False)
            self.ativos[self.tableWidget.currentItem().row()].operando = False
        self.tableWidget.item(row,0).setFont(font)
