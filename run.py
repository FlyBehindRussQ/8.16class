import os,sys
from PyQt5 import QtWidgets,QtGui,QtCore
from GUI import Ui_MainWindow

os.chdir(os.path.split(os.path.realpath(__file__))[0])



class MyMainWindow(QtWidgets.QMainWindow,Ui_MainWindow):    
    def __init__(self,parent=None) -> None:
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.init()
        
        
    def setIcon(self):
        self.circuit_1.setVisible(False)
        self.circuit_2.setVisible(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('1.jpg'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.model_1.setIcon(icon)
        self.model_1.setIconSize(QtCore.QSize(360,240))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('2.jpg'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.model_2.setIcon(icon)
        self.model_2.setIconSize(QtCore.QSize(360,240))
        
    def setPicture(self):
        self.model_1.setVisible(False)
        self.model_2.setVisible(False)
        pic = QtGui.QPixmap('1.jpg')
        self.circuit_1.setPixmap(pic)
        self.circuit_1.setScaledContents(True)
        pic = QtGui.QPixmap('2.jpg')
        self.circuit_2.setPixmap(pic)
        self.circuit_2.setScaledContents(True)
        
    def init(self):
        self.setIcon()
        # self.setPicture()
        self.calculate.clicked.connect(self.calculation)
        self.output_I.setReadOnly(True)
        
    
    def calculation(self):
        V,R1,R2,R3,R4 = 1,1,1,1,1
        if self.input_V.text()!='':
            V = float(self.input_V.text())
        if self.input_R_1.text()!='':
            R1 = float(self.input_R_1.text())
        if self.input_R_2.text()!='':
            R2 = float(self.input_R_2.text())
        if self.input_R_3.text()!='':
            R3 = float(self.input_R_3.text())
        if self.input_R_4.text()!='':
            R4 = float(self.input_R_4.text())
        print(V,R1,R2,R3,R4)

        if self.comboBox.currentText()=="电路1":
            Req = (R4 * (((R1 * R3) / (R1 + R3)) + R2)) / (R2 + R4 + ((R1 * R3) / (R1 + R3)))
        else:
            ra=R1*R3/(R1+R2+R3)
            rb=R2*R3/(R1+R2+R3)
            rc=R1*R2/(R1+R2+R3)
            Req=ra+(rc+R4)*rb/(rc+R4+rb)
        I = V / Req

        self.output_I.setText("{:.3f} ".format(I))

if __name__=='__main__':
    application = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyMainWindow()
    ui.show()
    sys.exit(application.exec_())