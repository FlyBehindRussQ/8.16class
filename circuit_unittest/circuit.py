import os,sys
from PyQt5 import QtWidgets,QtGui,QtCore
from GUI import Ui_MainWindow # 将设计界面的UiMainWindow导入主程序

# 将当前工作目录设置为脚本所在目录
os.chdir(os.path.split(os.path.realpath(__file__))[0])

# 设置窗口自动适应屏幕分辨率
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

# 定义主窗口类，继承QtWidgets.QMainWindow,Ui_MainWindow
class MyMainWindow(QtWidgets.QMainWindow,Ui_MainWindow):    
    
    # 初始化
    def __init__(self,parent=None) -> None:
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.init()
        
    # 设置控件状态的函数 
    def setIcon(self):
        # 设置以下控件为可见
        self.slogan.setVisible(True)
        self.model_1.setVisible(True)
        self.model_2.setVisible(True)
        self.goback.setVisible(False)
        self.circuit.setVisible(False)
        self.current.setVisible(False)
        self.frame_IO.setVisible(False)
        
        # 设置模型1的图标
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('1.jpg'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.model_1.setIcon(icon)
        self.model_1.setIconSize(QtCore.QSize(270,180))

        # 设置模型2的图标
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('2.jpg'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.model_2.setIcon(icon)
        self.model_2.setIconSize(QtCore.QSize(270,180))
        
    def setPicture(self,index):
        # 设置以下控件为不可见
        self.slogan.setVisible(False)
        self.model_1.setVisible(False)
        self.model_2.setVisible(False)
        self.goback.setVisible(True)
        self.circuit.setVisible(True)
        self.current.setVisible(True)
        self.frame_IO.setVisible(True)
        
        self.model = index # 定义模型为index
        jpg = ['1.jpg','2.jpg'][self.model] # 导入模型图片
        pic = QtGui.QPixmap(jpg) # 加载导入的图片
        self.circuit.setPixmap(pic) # 定义对象
        self.circuit.setScaledContents(True) # 设置图片适应控件大小
        self.current.setText(f'''I=?''') # 标记待计算的电流
    
    # 初始化界面
    def init(self):
        self.setIcon()
        self.output_I.setReadOnly(True)
        self.goback.clicked.connect(self.init) # 点击返回主界面
        self.model_1.clicked.connect(lambda: self.setPicture(0)) # 点击选择模型1
        self.model_2.clicked.connect(lambda: self.setPicture(1)) # 点击选择模型2
        self.calculate.clicked.connect(lambda: self.calculation(self.model)) # 点击进行计算
        self.inputs = [self.input_V,self.input_R_1,self.input_R_2,self.input_R_3,self.input_R_4] 
        self.factors = [0,0,0,0,0] # 初始输入的电压和电阻为0
        for i in range(0,5):
            self.inputs[i].setText(f'''{self.factors[i]}''') # 定义输入标签
        
    # 定义计算电流的函数
    def calculation(self,index):       

        # 定义用户的输入，分别为电压和四个电阻 
        for i in range(0,5):
            if self.inputs[i].text()!='':
                input_text = self.inputs[i].text()
                # 检查是否输入数字
                if not input_text.isdigit():
                    QtWidgets.QMessageBox.warning(self,"error",f"请输入有效数字")
                    return
                
                # 检查输入数字是否为0
                if input_text == "0":
                    QtWidgets.QMessageBox.warning(self,"error",f"输入不能为0")
                    return
                self.factors[i] = float(input_text)
                
        V, R1, R2, R3, R4 = self.factors

        # 选择电路模型，分别计算电流
        if index:
            Req = (R4 * (((R1 * R3) / (R1 + R3)) + R2)) / (R2 + R4 + ((R1 * R3) / (R1 + R3)))
        else:
            ra = R1 * R3 / (R1 + R2 + R3)
            rb = R2 * R3 / (R1 + R2 + R3)
            rc = R1 * R2 / (R1 + R2 + R3)
            Req = ra + (rc + R4) * rb / (rc + R4 + rb)
        I = V / Req
        self.output_I.setText("{:.3f} ".format(I)) # 定义输出保留三位小数
        self.current.setText(f'''I={'%-10.3f' % I}''')

# 进入主程序
if __name__=='__main__':
    application = QtWidgets.QApplication(sys.argv) # 创建应用程序
    MainWindow = QtWidgets.QMainWindow() # 创建窗口
    ui = MyMainWindow() # 定义ui
    ui.show() # 显示ui
    sys.exit(application.exec_())