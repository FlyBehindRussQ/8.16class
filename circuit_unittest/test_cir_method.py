import unittest
from PyQt5 import QtWidgets
from circuit import MyMainWindow  

# 创建测试类
class TestCalculationLogic(unittest.TestCase):

    def setUp(self):
        self.app = QtWidgets.QApplication([])  # 创建应用实例
        self.window = MyMainWindow()  # 创建窗口实例

    def tearDown(self):
        self.window.close()  # 关闭窗口
        self.app.quit()  # 关闭应用实例

    def test_calculation_model_1(self):
        self.window.model = 0  # 设置模型为 0（模型1）
        self.window.inputs[0].setText("10")  # 设置电压 V
        self.window.inputs[1].setText("4")   # 设置电阻 R1
        self.window.inputs[2].setText("5")   # 设置电阻 R2
        self.window.inputs[3].setText("3")   # 设置电阻 R3
        self.window.inputs[4].setText("2")   # 设置电阻 R4
        self.window.calculation(self.window.model)
        expected_result = 5.175
        self.assertEqual(float(self.window.output_I.text()), expected_result)

    def test_calculation_model_2(self):
        self.window.model = 1  # 设置模型为 1（模型2）
        self.window.inputs[0].setText("15")  # 设置电压
        self.window.inputs[1].setText("8")    # 设置电阻 R1
        self.window.inputs[2].setText("6")    # 设置电阻 R2
        self.window.inputs[3].setText("7")    # 设置电阻 R3
        self.window.inputs[4].setText("9")    # 设置电阻 R4
        self.window.calculation(self.window.model)
        expected_result = 3.208
        self.assertEqual(float(self.window.output_I.text()), expected_result)

if __name__ == '__main__':
    unittest.main()