from PyQt5.QtGui import *
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
import pymysql
import sys

class mainwindowshow(QWidget):
    def __init__(self):
        super(mainwindowshow, self).__init__()

        self.setWindowTitle('通用电流计算器')
        self.resize(800, 600)

        V_layerout = QVBoxLayout()
        H_layerout = QHBoxLayout()
        grid = QGridLayout()

        # 创建一个水平布局来容纳图片和输入框
        image_layout = QHBoxLayout()

        # 加载图片
        pixmap = QPixmap("D:\python\作业\电路图.png")  # 用实际图片路径替换 "path_to_image"
        image_label = QLabel()
        image_label.setPixmap(pixmap)

        # 添加图片和占位符文本框到水平布局
        image_layout.addWidget(image_label)
        image_layout.addWidget(QLabel())  # 用作占位符，可根据需要调整大小

        self.edit1 = QLineEdit()
        
        self.edit1.setPlaceholderText('输入电压')

        # 将图片和文本框水平布局添加到网格布局
        grid.addLayout(image_layout, 0, 1, 1, 3)  # 放在第一行，占三列
        grid.addWidget(self.edit1, 1, 6, 1, 1)

        self.edit2 = QLineEdit()
        self.edit2.setPlaceholderText('输入电阻1')
        self.edit3 = QLineEdit()
        self.edit3.setPlaceholderText('输入电阻2')
        self.edit4 = QLineEdit()
        self.edit4.setPlaceholderText('输入电阻3')
        self.edit5 = QLineEdit()
        self.edit5.setPlaceholderText('输入电阻4')

        self.btn1 = QPushButton('输出')
        self.comboBox = QComboBox()
        self.comboBox.addItem('图1')
        self.comboBox.addItem('图2')

        self.tablewidget = QTableWidget()
        self.tablewidget.setRowCount(0)
        self.tablewidget.setColumnCount(6)
        self.tablewidget.setHorizontalHeaderLabels(['电压', '电阻1', '电阻2', '电阻3','电阻4', '输出电流'])
        self.tablewidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        grid.addWidget(self.edit2, 2, 6, 1, 1)
        grid.addWidget(self.edit3, 3, 6, 1, 1)
        grid.addWidget(self.edit4, 4, 6, 1, 1)
        grid.addWidget(self.edit5, 5, 6, 1, 1)

        grid.addWidget(self.btn1, 6, 6, 1, 1)
        grid.addWidget(self.comboBox, 7, 6, 1, 1)
        grid.addWidget(self.tablewidget, 1, 1, 6, 4)
        self.setLayout(grid)
        #self.show()
        self.btn1.clicked.connect(self.btn1_click)
    
    def show_messagebox_0(self):
        message="不能输入数据为0"
        QMessageBox.information(self,'警告',message)
    def show_messagebox_blank(self):
        message="数据格式不正确"
        QMessageBox.information(self,'警告',message)
    def btn1_click(self):
         r1=self.edit2.text()
         r2=self.edit3.text()
         r3=self.edit4.text()
         r4=self.edit5.text()
         u=self.edit1.text()
         print(type(r1))
         try:
            r1 = float(self.edit2.text())
            r2 = float(self.edit3.text())
            r3 = float(self.edit4.text())
            r4 = float(self.edit5.text())
            u = float(self.edit1.text())
         except ValueError:
            self.show_messagebox_blank()
            return
         r1 = float(self.edit2.text())  # 获取输入框中的文本并将其转换为浮点数
         r2 = float(self.edit3.text())
         r3 = float(self.edit4.text())
         r4 = float(self.edit5.text())
         u = float(self.edit1.text())
         
         if r1 == 0 or r2 == 0 or r3 == 0 or r4 == 0 or u == 0:   
            self.show_messagebox_0()
            return
         
         else:
            if self.comboBox.currentText() == '图2':
                ra = r1 * r3 / (r1 + r2 + r3)
                rb = r2 * r3 / (r1 + r2 + r3)
                rc = r1 * r2 / (r1 + r2 + r3)
                r = ra + (rc + r4) * rb / (rc + r4 + rb)
            else: # '图1'
                r = (r4 * (((r1 * r3) / (r1 + r3)) + r2)) / (r2 + r4 + ((r1 * r3) / (r1 + r3)))
         output=u/r
         print(output)
    
         row_position = self.tablewidget.rowCount()  # 获取当前行数
         self.tablewidget.insertRow(row_position)  # 插入新行
         self.tablewidget.setItem(row_position, 0, QTableWidgetItem(str(u)))  # 设置单元格内容
         self.tablewidget.setItem(row_position, 1, QTableWidgetItem(str(r1)))
         self.tablewidget.setItem(row_position, 2, QTableWidgetItem(str(r2)))
         self.tablewidget.setItem(row_position, 3, QTableWidgetItem(str(r3)))
         self.tablewidget.setItem(row_position, 4, QTableWidgetItem(str(r4)))
         self.tablewidget.setItem(row_position, 5, QTableWidgetItem(str(output)))

# ...（其他代码）









if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainwindowshow()
    window.show()
    sys.exit(app.exec_())