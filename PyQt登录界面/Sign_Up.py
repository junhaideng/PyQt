# -*- coding=utf-8 -*-
"""
Author: Edgar
Version: 1.0.0
Create time: 2019 11
Modified time: 2019 12-10
Function: 该模块控制注册事件
"""
from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget, QPushButton, \
    QMessageBox, QApplication
from PyQt5.QtGui import QFont
from Database import Database
import sys


class SignWindow(QWidget):
    def __init__(self):
        super(SignWindow, self).__init__()
        self.database = Database('./data.db')
        self.setWindowTitle("Sign up")  # 设置标题
        self.resize(1000, 800)  # 设置窗口的大小
        self.set_ui()  # 调用其他的设计方法

    def set_ui(self):  # 集合所有的设计
        self.add_line_edit()
        self.add_button()
        self.add_label()

    def add_label(self):
        """添加相应的标签"""
        # 设置文本的字体
        label_font = QFont()
        label_font.setFamily('Consolas')
        label_font.setPixelSize(35)

        # 创建三个对应的标签，父窗口为 self
        self.username_label = QLabel(self)
        self.password_label = QLabel(self)
        self.confirm_label = QLabel(self)

        # 相应的标签设置文本
        self.username_label.setText("username")
        self.password_label.setText("password")
        self.confirm_label.setText("confirmed")

        # 控制label的大小  fixedSize表示之后无法修改
        self.username_label.setFixedSize(240, 40)
        self.password_label.setFixedSize(240, 40)
        self.confirm_label.setFixedSize(240, 40)

        # 设置对应的位置，注意move不是移动多少，而是直接移动到
        self.username_label.move(120, 530)
        self.password_label.move(120, 600)
        self.confirm_label.move(120, 670)

        # 设置字体
        self.username_label.setFont(label_font)
        self.password_label.setFont(label_font)
        self.confirm_label.setFont(label_font)

    def add_line_edit(self):
        """添加输入框"""
        line_edit_font = QFont()
        line_edit_font.setFamily('Consolas')
        line_edit_font.setPixelSize(30)

        # 创建三个输入框，父窗口为 self
        self.username_edit = QLineEdit(self)
        self.password_edit = QLineEdit(self)
        self.confirm_edit = QLineEdit(self)

        # 设置密码格式，输入密码的时候不可见密码
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_edit.setEchoMode(QLineEdit.Password)

        # 设置一下字体
        self.username_edit.setFont(line_edit_font)
        self.password_edit.setFont(line_edit_font)
        self.confirm_edit.setFont(line_edit_font)

        # 设置输入框中的占位符
        self.username_edit.setPlaceholderText("username")
        self.password_edit.setPlaceholderText("password")
        self.confirm_edit.setPlaceholderText('password again')

        # 控制大小
        self.username_edit.setFixedSize(350, 40)
        self.password_edit.setFixedSize(350, 40)
        self.confirm_edit.setFixedSize(350, 40)

        # 控制位置
        self.username_edit.move(320, 530)
        self.password_edit.move(320, 600)
        self.confirm_edit.move(320, 670)

    def add_button(self):
        """添加按钮"""
        button_font = QFont()
        button_font.setFamily('Consolas')
        button_font.setPixelSize(30)

        self.sign_button = QPushButton(self)
        self.sign_button.setFixedSize(160, 50)
        self.sign_button.setFont(button_font)
        self.sign_button.move(750, 600)
        self.sign_button.setText("Sign up")

        self.sign_button.setShortcut('Return')

        self.sign_button.clicked.connect(self.sign_up)

    def sign_up(self):
        """实现注册功能"""
        username = self.username_edit.text()
        password = self.password_edit.text()
        confirm = self.confirm_edit.text()

        if not password or not confirm:  # 如果有一个密码或者密码确认框为空
            QMessageBox.information(self, 'Error', 'The password is empty',
                                    QMessageBox.Yes)
        elif self.database.is_has(username):  # 如果用户名已经存在
            QMessageBox.information(self, 'Error',
                                    'The username already exists',
                                    QMessageBox.Yes)
        else:
            if password == confirm and password:  # 如果两次密码一致，并且不为空
                if len(username) < 5:
                    QMessageBox.information(self, 'Error',
                                            'The username is too short, change it for a long one, at least 5 words',
                                            QMessageBox.Yes, QMessageBox.Yes)
                    return
                if len(password) < 6:
                    QMessageBox.information(self, 'Error',
                                            'You password\'s length is less than 6, please input again',
                                            QMessageBox.Yes)
                    return
                else:
                    self.database.insert_table(username, password)  # 将用户信息写入数据库
                    QMessageBox.information(self, 'Successfully',
                                            'Sign up successfully'.format(
                                                username),
                                            QMessageBox.Yes)
                    self.close()  # 注册完毕之后关闭窗口
            else:
                QMessageBox.information(self, 'Error',
                                        'The password is not equal',
                                        QMessageBox.Yes)

    def closeEvent(self, event):
        """关闭之后将输入框清空"""
        self.username_edit.setText('')
        self.confirm_edit.setText('')
        self.password_edit.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SignWindow()
    window.show()

    sys.exit(app.exec_())
