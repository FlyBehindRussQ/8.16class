import sys
import pymysql
from prettytable import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class LibraryManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()

        self.name = 'adm'
        self.logged_in = False  # 添加登录状态变量

        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='123456',
                                  database='TESTDB')
        self.cursor = self.db.cursor()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('图书管理系统')
        self.setGeometry(100, 100, 800, 600)

        # 创建主窗口中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建标签控件
        self.label = QLabel('欢迎来到图书管理系统')
        self.label.setAlignment(Qt.AlignCenter)  # 居中对齐
        self.label.setStyleSheet('font-size: 24px;')  # 设置字体大小为24px
        layout.addWidget(self.label)

        # 创建登录状态标签
        self.label_login_status = QLabel('未登录')  # 默认显示未登录
        layout.addWidget(self.label_login_status)

        # 创建按钮控件
        self.btn_register = QPushButton('注册')
        self.btn_login = QPushButton('登录')
        self.btn_find = QPushButton('查询图书')
        self.btn_add = QPushButton('添加图书')
        self.btn_delete = QPushButton('删除图书')
        self.btn_borrow = QPushButton('借书')
        self.btn_return = QPushButton('还书')
        self.btn_info = QPushButton('个人信息')
        self.btn_logout = QPushButton('退出登录')

        # 为按钮添加点击事件
        self.btn_register.clicked.connect(self.register)
        self.btn_login.clicked.connect(self.login)
        self.btn_add.clicked.connect(self.add)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_borrow.clicked.connect(self.borrow)
        self.btn_return.clicked.connect(self.return_book)
        self.btn_info.clicked.connect(self.person_information)
        self.btn_logout.clicked.connect(self.logout)

        # 将按钮添加到布局
        layout.addWidget(self.btn_register)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_borrow)
        layout.addWidget(self.btn_return)
        layout.addWidget(self.btn_info)
        layout.addWidget(self.btn_logout)

        # 设置布局到中心部件
        self.central_widget.setLayout(layout)
        # 更新登录状态标签的显示内容
        self.operate()

    def register(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('注册')
        dialog.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        label_username = QLabel('请输入用户名：')
        self.input_username = QLineEdit()
        layout.addWidget(label_username)
        layout.addWidget(self.input_username)

        label_password = QLabel('请输入密码：')
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)  # 密码不可见
        layout.addWidget(label_password)
        layout.addWidget(self.input_password)

        label_rpassword = QLabel('请确认密码：')
        self.input_rpassword = QLineEdit()
        self.input_rpassword.setEchoMode(QLineEdit.Password)  # 密码不可见
        layout.addWidget(label_rpassword)
        layout.addWidget(self.input_rpassword)

        btn_register = QPushButton('注册')
        btn_register.clicked.connect(self.on_register_clicked)
        layout.addWidget(btn_register)

        dialog.setLayout(layout)
        dialog.exec_()

    def on_register_clicked(self):
        username = self.input_username.text()
        password_ = self.input_password.text()
        rpassword = self.input_rpassword.text()

        if len(password_) < 8:
            QMessageBox.critical(self, '注册失败', '密码不能少于8位')
        elif password_ == rpassword:
            print("注册成功！")
            sql = "INSERT INTO user(username, password, book) VALUES (%s, %s, %s)"
            param = (username, password_, ' ')
            try:
                self.cursor.execute(sql, param)
                self.db.commit()
                QMessageBox.information(self, '注册成功', '注册成功！')
                self.sender().parent().close()  # 关闭登录窗口
                self.login()
            except Exception as e:
                print("注册失败:", e)
                QMessageBox.critical(self, '注册失败', '注册失败，请稍后再试！')
        else:
            QMessageBox.critical(self, '注册失败', '两次输入的密码不一致，请重新输入！')

    def login(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('登录')
        dialog.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()

        label_username = QLabel('输入用户名：')
        self.input_username = QLineEdit()
        layout.addWidget(label_username)
        layout.addWidget(self.input_username)

        label_password = QLabel('输入密码：')
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)  # 密码不可见
        layout.addWidget(label_password)
        layout.addWidget(self.input_password)

        btn_login = QPushButton('登录')
        btn_login.clicked.connect(self.on_login_clicked)
        layout.addWidget(btn_login)

        dialog.setLayout(layout)
        dialog.exec_()


    def on_login_clicked(self):
        username = self.input_username.text()
        password_ = self.input_password.text()

        sql = "SELECT * FROM user WHERE username = %s"
        try:
            self.cursor.execute(sql, (username,))
            result = self.cursor.fetchone()
            if result and result[1] == password_:
                QMessageBox.information(self, '登录成功', '登录成功！')
                self.logged_in = True
                self.name = username
                self.operate()
                self.sender().parent().close()  # 关闭登录窗口
            else:
                QMessageBox.critical(self, '登录失败', '密码错误')
        except Exception as e:
            print("登录失败:", e)
            QMessageBox.critical(self, '登录失败', '登录失败，请稍后再试！')

    def add(self):
        if not self.logged_in:
            QMessageBox.warning(self, '未登录', '您还未登录！请先登录后再进行操作。')
            return
        # 非管理员用户无权限访问，弹出提示窗口
        if self.name != 'adm':
            QMessageBox.warning(self, '无权限访问', '您无权限进行该操作！')
            return

        book_in, ok = QInputDialog.getText(self, '添加图书', '请输入添加的书籍：')
        if ok and book_in:
            sql = "INSERT INTO book(name) VALUES (%s)"
            try:
                self.cursor.execute(sql, (book_in,))
                self.db.commit()
                QMessageBox.information(self, '添加成功', '添加成功！')
            except Exception as e:
                print("添加失败:", e)
                self.db.rollback()
            finally:
                i, ok = QInputDialog.getText(self, '是否继续添加', '是否继续添加？(yes/no)')
                if ok and i.strip().lower() == 'yes':
                    self.add()

    def delete(self):
        if not self.logged_in:
            QMessageBox.warning(self, '未登录', '您还未登录！请先登录后再进行操作。')
            return
    # 非管理员用户无权限访问，弹出提示窗口
        if self.name != 'adm':
            QMessageBox.warning(self, '无权限访问', '您无权限进行该操作！')
            return
        book_del, ok = QInputDialog.getText(self, '删除图书', '请输入需要删除的图书书名：')
        if ok and book_del:
            # 查询数据库判断书籍是否存在
            sql_select = "SELECT * FROM book WHERE name = %s"
            self.cursor.execute(sql_select, (book_del,))
            result = self.cursor.fetchone()

            if not result:
                # 书籍不存在，弹出提示窗口
                QMessageBox.warning(self, '书籍不存在', '请确认书籍是否正确！')
                return

            # 执行删除操作
            sql_delete = "DELETE FROM book WHERE name = %s"
            try:
                self.cursor.execute(sql_delete, (book_del,))
                self.db.commit()
                QMessageBox.information(self, '删除成功', '删除成功！')
            except Exception as e:
                print("删除失败:", e)
                self.db.rollback()



    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.label_title = QLabel("图书管理系统")
        self.label_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_title)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(['书籍名称'])
        layout.addWidget(self.tableWidget)

        btn_add = QPushButton('添加图书')
        btn_add.clicked.connect(self.add)
        layout.addWidget(btn_add)

        btn_delete = QPushButton('删除图书')
        btn_delete.clicked.connect(self.delete)
        layout.addWidget(btn_delete)

        self.central_widget.setLayout(layout)

    
    def borrow(self):
        if not self.logged_in:
            QMessageBox.warning(self, '未登录', '您还未登录！请先登录后再进行操作。')
            return
        # 检查用户是否已经借了图书
        sql = "SELECT book FROM user WHERE username = %s"
        try:
            self.cursor.execute(sql, (self.name,))
            result = self.cursor.fetchone()
            book = result[0]
            if book != ' ':
                QMessageBox.warning(self, '已借图书', '您已经借书，请先归还图书后再借阅其他书籍。')
                return
        except Exception as e:
            print("查询失败:", e)
        # 查询数据库中所有的书籍
        sql = "SELECT name FROM book"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            book_list = [row[0] for row in results]
            if not book_list:
                QMessageBox.warning(self, '无可借阅图书', '暂无可借阅的图书。')
                return

            # 弹出借书弹窗
            borrow_book, ok = QInputDialog.getItem(self, "借书", "请选择图书：", book_list, editable=False)
            if ok:
                sql = "UPDATE user SET book = %s WHERE username = %s"
                try:
                    self.cursor.execute(sql, (borrow_book, self.name))
                    self.db.commit()
                    QMessageBox.information(self, "借书成功", "借书成功！")
                except Exception as e:
                    print("借书失败:", e)
                    self.db.rollback()
        except Exception as e:
            print("查询失败:", e)

    def return_book(self):
        if not self.logged_in:
            QMessageBox.warning(self, '未登录', '您还未登录！请先登录后再进行操作。')
            return
        sql = "SELECT * FROM user WHERE username = %s"
        try:
            self.cursor.execute(sql, (self.name,))
            result = self.cursor.fetchone()
            book = result[2]
            if book == ' ':
                QMessageBox.information(self, "还书失败", "你未借书！")
            else:
                response = QMessageBox.question(self, "确认还书", f"用户 {self.name} 已借书 {book}\n是否还书？",
                                                 QMessageBox.Yes | QMessageBox.No)
                if response == QMessageBox.Yes:
                    sql = "UPDATE user SET book = %s WHERE username = %s"
                    try:
                        self.cursor.execute(sql, (' ', self.name))
                        self.db.commit()
                        QMessageBox.information(self, "还书成功", "还书成功！")
                    except Exception as e:
                        print("还书失败:", e)
                        self.db.rollback()
        except Exception as e:
            print("操作失败:", e)

    def look(self):
        info = "----个人信息----\n"
        if self.name == 'adm':
            sql = "SELECT * FROM user"
            info += "管理员查看所有用户信息：\n"
        else:
            sql = "SELECT * FROM user WHERE username = %s"
            info += "个人信息：\n"

        try:
            if self.name != 'adm':
                self.cursor.execute(sql, (self.name,))
            else:
                self.cursor.execute(sql)

            results = self.cursor.fetchall()
            if results:
                table = PrettyTable(["用户名", "密码"])
                for row in results:
                    table.add_row([row[0], row[1]])
                info += table.get_string()
            else:
                info += "无信息"
        except Exception as e:
            print("查询失败:", e)

        QMessageBox.information(self, "个人信息", info)

    def update_password(self):
        password, ok = QInputDialog.getText(self, "修改密码", "请输入新密码：", QLineEdit.Password)
        if ok:
            rpassword, ok = QInputDialog.getText(self, "修改密码", "请确认密码：", QLineEdit.Password)
            if ok:
                if password == rpassword:
                    sql = "UPDATE user SET password = %s WHERE username = %s"
                    try:
                        self.cursor.execute(sql, (rpassword, self.name))
                        self.db.commit()
                        QMessageBox.information(self, "修改成功", "密码修改成功！")
                    except Exception as e:
                        print("修改失败:", e)
                        self.db.rollback()
                else:
                    QMessageBox.warning(self, "密码不一致", "前后密码不一致！")

    def person_information(self):
        if not self.logged_in:
            QMessageBox.warning(self, '未登录', '您还未登录！请先登录后再进行操作。')
            return
        items = ["查看个人信息", "修改个人信息", "查看已借阅的书籍"]
        item, ok = QInputDialog.getItem(self, "个人信息", "请选择操作：", items, editable=False)
        if ok:
            if item == "查看个人信息":
                self.look()
            elif item == "修改个人信息":
                self.update_password()
            elif item == "查看已借阅的书籍":
                sql = "SELECT book FROM user WHERE username = %s"
                try:
                    self.cursor.execute(sql, (self.name,))
                    result = self.cursor.fetchone()
                    book = result[0]
                    if book != ' ':
                        QMessageBox.information(self, "已借阅的书籍", f"已借阅的书籍：{book}")
                    else:
                        QMessageBox.information(self, "暂未借阅图书", "暂未借阅图书")
                except Exception as e:
                    print("查询失败:", e)

    # ... 其他方法 ...

    def logout(self):
        if not self.logged_in:
            QMessageBox.warning(self, '未登录', '您还未登录！请先登录后再进行操作。')
            return
        QMessageBox.information(self, "已退出登录", "已退出登录！")
        self.name = 'adm'  # 重置为默认用户adm
        self.logged_in=False
        self.operate()

    def operate(self):
        # 更新登录状态标签的显示内容
        if self.logged_in:
            self.label_login_status.setText("已登录,用户名：%s" % self.name)
        else:
            self.label_login_status.setText("未登录")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    system = LibraryManagementSystem()
    system.show()
    sys.exit(app.exec_())