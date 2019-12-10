# -*- coding:utf-8 -*-
"""
Author: Edgar
Version: 1.0.0
Create time: 2019 11
Modified time: 2019 12-10
Function: 该模块控制登录事件,同时也是各个模块的集合
"""
import os
import sys
from Sign_Up import SignWindow  # 注册所需要的自定义库
from Admin import AdminWindow
from Database import Database
from Main import Main

try:
    import PyQt5
except ModuleNotFoundError:
    os.system("pip install PyQt5")
    from PyQt5.Qt import *
else:
    from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QFrame, QMessageBox, QComboBox
    from PyQt5.QtGui import QIcon, QFont
    from PyQt5.QtCore import Qt


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.icon = QIcon("./python-logo.png")
        self.database = Database('./data.db')
        self.sign_up_win = SignWindow()  # 创建的注册窗口
        self.admin_win = AdminWindow()  # 创建的用户管理窗口
        self.main_win = Main()  # 登录后的主页面
        self.admin_win.set_main_window(self.main_win)
        self.setWindowTitle("  Login in")
        self.setFixedSize(1000, 800)
        self.set_ui()

    def change_icon(self):
        """用来修改图像的图标"""
        self.setWindowIcon(self.icon)

    def set_ui(self):
        """设置界面"""
        self.set_background_image()  # 设置背景的图片
        self.change_icon()
        self.add_label()
        self.add_line_edit()
        self.add_button()

    def add_label(self):
        """添加相应的标签"""
        # 设置字体
        label_font = QFont()
        label_font.setFamily('Consolas')
        label_font.setPixelSize(30)

        # 创建文本标签
        self.username_label = QLabel(self)
        self.password_label = QLabel(self)

        # 设置标签中的文本
        self.username_label.setText("username")
        self.password_label.setText("password")

        # 设置标签的大小
        self.username_label.setFixedSize(240, 40)
        self.password_label.setFixedSize(240, 40)

        # 设置标签的位置
        self.username_label.move(120, 530)
        self.password_label.move(120, 600)

        self.username_label.setFont(label_font)
        self.password_label.setFont(label_font)

    def add_line_edit(self):
        """添加输入框"""
        line_edit_font = QFont()
        line_edit_font.setFamily('Consolas')
        line_edit_font.setPixelSize(30)

        # 创建
        self.username_edit = QLineEdit(self)
        self.password_edit = QLineEdit(self)

        # 设置密码格式
        self.password_edit.setEchoMode(QLineEdit.Password)

        # 设置字体
        self.username_edit.setFont(line_edit_font)
        self.password_edit.setFont(line_edit_font)

        # 设置占位符
        self.username_edit.setPlaceholderText("username")
        self.password_edit.setPlaceholderText("password")

        # 设置大小
        self.username_edit.setFixedSize(350, 40)
        self.password_edit.setFixedSize(350, 40)

        # 设置位置
        self.username_edit.move(320, 530)
        self.password_edit.move(320, 600)

    def add_button(self):
        """添加按钮"""
        button_font = QFont()
        button_font.setFamily('Consolas')
        button_font.setPixelSize(30)

        # 创建按钮对象
        self.login_button = QPushButton("Login", self)
        self.sign_button = QPushButton(self)

        # 修改大小且不可变
        self.login_button.setFixedSize(160, 50)
        self.sign_button.setFixedSize(160, 50)

        # 设置字体
        self.login_button.setFont(button_font)
        self.sign_button.setFont(button_font)

        # 设置位置
        self.login_button.move(750, 530)
        self.sign_button.move(750, 600)

        # 设置文本提示内容
        self.login_button.setText("Login in")
        self.sign_button.setText("Sign up")
        self.login_button.setToolTip('If you are the admin, please login in with the specific account')

        # 实现功能，按钮点击之后执行的动作
        self.login_button.clicked.connect(self.login)
        self.sign_button.clicked.connect(self.sign_up_window)

        self.login_button.setShortcut("Return")  # 设置快捷键

    def set_background_image(self):
        """添加背景图片"""
        self.frame = QFrame(self)  # 这里采用 QFrame, 如果直接对self进行背景设置，似乎没有那么简单容易控制
        self.frame.resize(1000, 520)
        self.frame.move(40, 150)
        self.frame.setStyleSheet(
            'background-image: url("./python.png"); background-repeat: no-repeat; text-align:center;')

    def login(self):
        """登录功能实现"""
        username = self.username_edit.text()
        password = self.password_edit.text()
        data = self.database.find_password_by_username(username)  # 在数据库中查找数据
        if username and password:  # 如果两个输入框都不为空
            if data:
                if str(data[0][0]) == password:
                    QMessageBox.information(self, 'Successfully', 'Login in successful \n Welcome {}'.format(username),
                                            QMessageBox.Yes | QMessageBox.No)
                    self.password_edit.setText('') # 登录成功，将之前的用户信息清除
                    self.username_edit.setText('')
                    self.close()
                    if username == 'admin':  # 如果是管理员，进入管理界面
                        self.admin_win.show()
                    else:
                        self.main_win.show()

                else:
                    QMessageBox.information(self, 'Failed', 'Password is wrong, try again',
                                            QMessageBox.Yes | QMessageBox.No)
            else:
                QMessageBox.information(self, 'Error', 'No such username', QMessageBox.Yes | QMessageBox.No)
        elif username:  # 如果用户名写了
            QMessageBox.information(self, 'Error', 'Input your password', QMessageBox.Yes | QMessageBox.No)
        else:
            QMessageBox.information(self, 'Error', 'Fill in the blank', QMessageBox.Yes | QMessageBox.No)

    def sign_up_window(self):
        self.sign_up_win.setWindowIcon(self.icon)
        self.sign_up_win.move(self.x() + 100, self.y() + 100)  # 移动一下注册窗口，以免和之前的重复
        frame = QFrame(self.sign_up_win)
        self.sign_up_win.setWindowFlag(Qt.Dialog)
        frame.resize(1000, 300)
        frame.setStyleSheet('background-image: url("./python.png"); background-repeat: no-repeat;')
        frame.move(40, 150)
        # 打开注册窗口时，清除原来的信息
        self.password_edit.setText('')
        self.username_edit.setText('')
        self.sign_up_win.show()

    def closeEvent(self, event):
        self.sign_up_win.close()  # 关闭登录窗口的时候，注册窗口也应该关闭


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()

    sys.exit(app.exec_())
