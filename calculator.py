import os,sys
from PyQt5 import QtWidgets,QtGui,QtCore
from calcGUI import Ui_MainWindow

os.chdir(os.path.split(os.path.realpath(__file__))[0])
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

class MyMainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None) -> None:
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.init()
        self.signals()
        self.display()
        
    def init(self):
        self.showhist = 0
        self.result = 0
        self.expression = "0"
        self.history = []
        if os.path.exists('history.txt'):
            with open('history.txt','r',encoding='UTF-8') as read:
                self.history = read.readlines()
        
    def signals(self):
        self.Button_0.clicked.connect(lambda: self.click_key('0'))
        self.Button_1.clicked.connect(lambda: self.click_key('1'))
        self.Button_2.clicked.connect(lambda: self.click_key('2'))
        self.Button_3.clicked.connect(lambda: self.click_key('3'))
        self.Button_4.clicked.connect(lambda: self.click_key('4'))
        self.Button_5.clicked.connect(lambda: self.click_key('5'))
        self.Button_6.clicked.connect(lambda: self.click_key('6'))
        self.Button_7.clicked.connect(lambda: self.click_key('7'))
        self.Button_8.clicked.connect(lambda: self.click_key('8'))
        self.Button_9.clicked.connect(lambda: self.click_key('9'))
        
        self.Button_Plus.clicked.connect(lambda: self.click_opt('+'))
        self.Button_Minus.clicked.connect(lambda: self.click_opt('-'))
        self.Button_Multi.clicked.connect(lambda: self.click_opt('×'))
        self.Button_Divide.clicked.connect(lambda: self.click_opt('÷'))
        
        self.Button_Dot.clicked.connect(self.click_dot)
        self.Button_Rev.clicked.connect(self.click_rev)
        
        self.Button_C.clicked.connect(lambda: self.cls(1))
        self.Button_Del.clicked.connect(lambda: self.cls(0))
        
        self.Button_Equal.clicked.connect(self.calculation)
        self.Button_his.clicked.connect(self.showHistory)
        
    def click_key(self,key):
        if self.expression=='0':
            self.expression = self.expression[:-1]
        self.expression = self.expression + key
        self.display()
        
    def click_opt(self,key):
        if self.expression=="0" and key=='-':
            self.expression = self.expression[:-1]
        elif self.expression[-1] in ['+','-','×','÷']:
            self.expression = self.expression[:-1]
        self.expression = self.expression + key
        self.display()
    
    def click_dot(self):
        if self.expression[-1] in ['+','-','×','÷']:
            self.expression = self.expression + '0.'
        else:
            self.expression = self.expression + '.'
        self.display()
        
    def click_rev(self):
        self.expression = '-'+str(self.result)
        if self.result<0:
            self.expression = self.expression[2:]
        self.display()
    
    def cls(self,index):
        if index:
            self.expression = "0"
        else:
            self.expression = self.expression[:-1]
            if self.expression=="":
                self.expression = "0"
        self.display()
        
    def calculation(self):
        self.history.append(self.expression+' = '+str(self.result))
        write = open('history.txt','w',encoding='UTF-8')
        for lines in self.history:
            write.write(lines+'\n')
        self.Monitor.clear()
        self.Monitor.append(self.expression+' = '+str(self.result))
        self.expression = str(self.result)
    
    def display(self):
        self.Monitor.clear()
        self.Monitor.append(self.expression)
        if self.expression[-1] not in ['+','-','×','÷']:
            self.expression = self.expression.replace('÷','/').replace('×','*')
            try:
                self.result = eval(self.expression)
            except:
                self.expression = self.expression[:-1]
                self.display()
                return
            self.expression = self.expression.replace('/','÷').replace('*','×')
        self.Monitor.append('=' + str(self.result))
    
    def showHistory(self):
        self.showhist = 1 - self.showhist
        if self.showhist:
            self.Monitor.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.Monitor.clear()
            for lines in self.history:
                self.Monitor.append(lines[:-1])
        else:
            self.Monitor.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.display()
        
        
if __name__=='__main__':
    application = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyMainWindow()
    ui.show()
    sys.exit(application.exec_())