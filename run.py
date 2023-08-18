import os,sys
from PyQt5 import QtWidgets,QtGui,QtCore
from GUI import Ui_MainWindow

os.chdir(os.path.split(os.path.realpath(__file__))[0])
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

class MyMainWindow(QtWidgets.QMainWindow,Ui_MainWindow):    
    def __init__(self,parent=None) -> None:
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.init()
        
        
    def setIcon(self):
        self.slogan.setVisible(True)
        self.model_1.setVisible(True)
        self.model_2.setVisible(True)
        self.goback.setVisible(False)
        self.circuit.setVisible(False)
        self.current.setVisible(False)
        self.frame_IO.setVisible(False)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('1.jpg'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.model_1.setIcon(icon)
        self.model_1.setIconSize(QtCore.QSize(270,180))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('2.jpg'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.model_2.setIcon(icon)
        self.model_2.setIconSize(QtCore.QSize(270,180))
        
    def setPicture(self,index):
        self.slogan.setVisible(False)
        self.model_1.setVisible(False)
        self.model_2.setVisible(False)
        self.goback.setVisible(True)
        self.circuit.setVisible(True)
        self.current.setVisible(True)
        self.frame_IO.setVisible(True)
        
        self.model = index
        jpg = ['1.jpg','2.jpg'][self.model]
        pic = QtGui.QPixmap(jpg)
        self.circuit.setPixmap(pic)
        self.circuit.setScaledContents(True)
        self.current.setText(f'''I=?''')
        
    def init(self):
        self.setIcon()
        self.output_I.setReadOnly(True)
        self.goback.clicked.connect(self.init)
        self.model_1.clicked.connect(lambda: self.setPicture(0))
        self.model_2.clicked.connect(lambda: self.setPicture(1))
        self.calculate.clicked.connect(lambda: self.calculation(self.model))
        self.inputs = [self.input_V,self.input_R_1,self.input_R_2,self.input_R_3,self.input_R_4]
        self.factors = [1,1,1,1,1]
        for i in range(0,5):
            self.inputs[i].setText(f'''{self.factors[i]}''')
        
    
    def calculation(self,index):        
        for i in range(0,5):
            if self.inputs[i].text()!='':
                self.factors[i] = float(self.inputs[i].text())
        V, R1, R2, R3, R4 = self.factors

        if index:
            Req = (R4 * (((R1 * R3) / (R1 + R3)) + R2)) / (R2 + R4 + ((R1 * R3) / (R1 + R3)))
        else:
            ra = R1 * R3 / (R1 + R2 + R3)
            rb = R2 * R3 / (R1 + R2 + R3)
            rc = R1 * R2 / (R1 + R2 + R3)
            Req = ra + (rc + R4) * rb / (rc + R4 + rb)
        I = V / Req
        self.output_I.setText("{:.3f} ".format(I))
        self.current.setText(f'''I={'%-10.3f' % I}''')

if __name__=='__main__':
    application = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyMainWindow()
    ui.show()
    sys.exit(application.exec_())