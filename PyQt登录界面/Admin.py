# -*- coding:utf-8 -*-
"""
Author: Edgar
Version: 1.0.0
Create time: 2019 12
Modified time: 2019 12-10
Function: 该模块为管理员用来管理所有的用户信息的模块，只有管理员才能进入，且管理员的账号一定为 admin，
数据库中必含有admin这个账号名，如果被删除，会自动生成默认的admin及默认密码 admin123
"""
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidget, QAbstractItemView, QMessageBox, QTableWidgetItem, \
    QLineEdit, QPushButton, QHeaderView, QLabel, QCheckBox, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from Database import Database


class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget(self)  # 添加表格对象
        self.database = Database('./data.db')
        self.check_list = []  # 保存所有的选择框
        self.show_password_flag = False  # 是否显示原密码
        self.select_all_flag = False  # 是否选择全部
        self.main_window = None
        self.set_ui()

    def set_main_window(self, widget):
        self.main_window = widget

    def set_ui(self):
        self.setWindowTitle("Management page")
        self.setFixedSize(1200, 900)
        self.font = QFont("Consolas")
        self.setFont(self.font)
        self.setWindowIcon(QIcon("./python-logo.png"))  # 设置图标
        self.add_table()  # 添加数据表格
        self.get_all_user()  # add table 之后才有show
        self.add_line_edit()  # 添加输入框
        self.add_label()  # 添加标签
        self.add_button()  # 添加按钮并绑定事件

    def add_table(self):
        """添加数据表格"""
        self.table.setFixedWidth(1020)  # 设置宽度
        self.table.setFixedHeight(600)  # 设置高度
        self.table.move(10, 30)  # 设置显示的位置
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自动填充
        self.table.horizontalHeader().setFont(self.font)  # 设置一下字体
        # self.table.setSelectionMode(QAbstractItemView.SingleSelection)  # 只能单选
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 只能选择整行
        self.table.setColumnCount(4)  # 设置列数
        self.table.setHorizontalHeaderLabels(["Choice", "username", "password", 'created_time'])  # 设置首行
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 表格中的内容设置为无法修改
        self.table.verticalHeader().hide()  # 把序号隐藏
        self.table.setSortingEnabled(False)  # 自动排序

    def get_all_user(self):
        """获取所有的用户信息"""
        data = self.database.read_table()  # 从数据库中获取用户信息，用户信息以 username, password, created_time 形式返回
        for user in data:
            self.add_row(user[0], user[1], user[2])

    def add_row(self, username, password, created_time):
        """在表格上添加一行新的内容"""
        row = self.table.rowCount()  # 表格的行数
        self.table.setRowCount(row + 1)  # 添加一行表格
        self.table.setItem(row, 1, QTableWidgetItem(str(username)))  # 将用户信息插入到表格中
        self.table.setItem(row, 2, QTableWidgetItem(str(password)))
        self.table.setItem(row, 3, QTableWidgetItem(str(created_time)))
        # 设置复选框
        widget = QWidget()
        check = QCheckBox()
        self.check_list.append(check)  # 添加到复选框列表中
        check_lay = QHBoxLayout()
        check_lay.addWidget(check)
        check_lay.setAlignment(Qt.AlignCenter)
        widget.setLayout(check_lay)
        self.table.setCellWidget(row, 0, widget)

    def add_line_edit(self):
        self.username_edit = QLineEdit(self)
        self.username_edit.setFixedSize(240, 40)
        self.username_edit.move(760, 700)
        self.username_edit.setPlaceholderText('username')

        self.password_edit = QLineEdit(self)
        self.password_edit.setFixedSize(240, 40)
        self.password_edit.move(760, 760)
        self.password_edit.setPlaceholderText('password')
        self.password_edit.setEchoMode(QLineEdit.Password)

        # 更新密码的输入框
        self.update_username_edit = QLineEdit(self)
        self.update_username_edit.setFixedSize(240, 40)
        self.update_username_edit.move(160, 700)
        self.update_username_edit.setPlaceholderText('username')

        self.update_password_edit = QLineEdit(self)
        self.update_password_edit.setFixedSize(240, 40)
        self.update_password_edit.move(160, 760)
        self.update_password_edit.setPlaceholderText('new password')

    def show_password(self):
        if self.show_password_flag:  # 如果是真，隐藏密码
            self.password_edit.setEchoMode(QLineEdit.Password)
            self.show_password_flag = False
            self.show_password_button.setText('Show')
        else:  # 否则显示密码
            self.password_edit.setEchoMode(QLineEdit.Normal)
            self.show_password_flag = True
            self.show_password_button.setText("Hide")

    def add_label(self):
        """添加界面上的标签控件"""
        self.username_label = QLabel(self)
        self.username_label.setFixedSize(160, 40)
        self.username_label.move(640, 700)
        self.username_label.setText('username')

        self.password_label = QLabel(self)
        self.password_label.setFixedSize(160, 40)
        self.password_label.move(640, 760)
        self.password_label.setText('password')

        # 更新密码的标签
        self.update_username_label = QLabel(self)
        self.update_username_label.setFixedSize(160, 40)
        self.update_username_label.move(40, 700)
        self.update_username_label.setText('username')

        self.update_password_label = QLabel(self)
        self.update_password_label.setFixedSize(160, 40)
        self.update_password_label.move(40, 760)
        self.update_password_label.setText('password')

    def add_button(self):
        """添加界面上的按钮控件"""
        # 创建按钮对象
        self.delete_button = QPushButton(self)
        self.update_button = QPushButton(self)
        self.add_button_ = QPushButton(self)
        self.show_password_button = QPushButton(self)
        self.clear_button = QPushButton(self)
        self.select_all_button = QPushButton(self)
        self.refresh_button = QPushButton(self)
        self.main_window_button = QPushButton(self)

        # 设置按钮上的文本
        self.delete_button.setText("Delete")
        self.update_button.setText("Update")
        self.add_button_.setText("Add")
        self.show_password_button.setText("Show")
        self.clear_button.setText("Clear")
        self.select_all_button.setText("Select All")
        self.refresh_button.setText("Refresh")
        self.main_window_button.setText("Main window")

        # 在按钮上设置提示信息
        self.delete_button.setToolTip("Delete the selected user, you can choose multiple users")
        self.clear_button.setToolTip("Clear all the users, including the super user, but the super user will be "
                                     "created later by default")
        self.select_all_button.setToolTip("Select all the users, including the super user")
        self.show_password_button.setToolTip("Show or hide the password")
        self.add_button_.setToolTip("Add a new user with the username and password in the input box")
        self.update_button.setToolTip("Update the password with the chosen username")
        self.refresh_button.setToolTip("Click here to refresh the table")
        self.main_window_button.setToolTip("Click here and you will go to the user interface")

        # 控制位置
        self.delete_button.move(1040, 340)
        self.select_all_button.move(1040, 280)
        self.clear_button.move(1040, 400)
        self.refresh_button.move(1040, 460)

        self.update_button.move(430, 700)
        self.add_button_.move(1020, 700)
        self.show_password_button.move(1020, 750)

        self.main_window_button.move(500,820)

        # 绑定事件
        self.delete_button.clicked.connect(self.delete_user)
        self.select_all_button.clicked.connect(self.select_all)
        self.clear_button.clicked.connect(self.clear)
        self.show_password_button.clicked.connect(self.show_password)
        self.add_button_.clicked.connect(self.add_user)
        self.update_button.clicked.connect(self.update_password)
        self.refresh_button.clicked.connect(self.refresh)
        self.main_window_button.clicked.connect(self.show_main_window)

        self.main_window_button.setFixedSize(200, 40)

    def show_main_window(self):
        self.main_window.show()

    def delete_user(self):
        choose_list = []
        for i in self.check_list:
            if i.isChecked():
                username = self.table.item(self.check_list.index(i), 1).text()
                if username == 'admin':
                    answer = QMessageBox.critical(self, 'Error', 'You are going to delete the super user, but it will be created later with the default password',
                                                  QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
                    if answer == QMessageBox.Yes:
                        choose_list.append(i)
                    if answer == QMessageBox.Cancel:
                        return
                else:
                    choose_list.append(i)

        for i in choose_list:
            username = self.table.item(self.check_list.index(i), 1).text()
            self.database.delete_table_by_username(username)
            self.table.removeRow(self.check_list.index(i))
            self.check_list.remove(i)
        self.database.create_table()

    def select_all(self):
        """选择是否选择全部"""
        try:
            if not self.select_all_flag:
                for check in self.check_list:
                    check.setCheckState(2)  # 设置为选择状态
                self.select_all_button.setText("Unselect")
                self.select_all_flag = True
            else:
                for check in self.check_list:
                    check.setCheckState(0)  # 设置为未选状态
                self.select_all_button.setText("Select All")
                self.select_all_flag = False
        except:
            # 该错误是由于没有复选框引起
            pass

    def add_user(self):
        """一行一行的添加数据"""
        username = self.username_edit.text()
        password = self.password_edit.text()
        if all((username, password)):
            flag = self.database.insert_table(username, password)
            if flag:
                QMessageBox.critical(self, 'Error', 'Already exists the username {}, please use another username'.format(username))
            else:
                self.add_row(username, password, self.database.get_time())
            self.username_edit.setText('')  # 清空输入的用户信息
            self.password_edit.setText('')
        else:
            QMessageBox.critical(self, 'Error', "Please fill in the blanks")

    def clear(self):
        """清空所有的数据，包括数据库和表格中的数据"""
        self.table.clearContents()  # 清空表格的内容
        self.table.setRowCount(0)  # 将表格的行数重置为0
        self.database.clear()  # 清空数据库数据

    def update_password(self):
        """更新密码"""
        username = self.update_username_edit.text()
        password = self.update_password_edit.text()
        if len(password) >= 6:
            self.database.update_table(username, password)
            self.change_table(username, password)
            self.update_password_edit.setText('')
            self.update_username_edit.setText('')
        else:
            QMessageBox.information(self, 'Error', 'Password is too short, at least 6 words',  QMessageBox.Yes, QMessageBox.Yes)

    def change_table(self, username, password):
        """更新表格"""
        find_flag = False
        for row in range(self.table.rowCount()):
            username_find = self.table.item(row, 1).text()
            if username_find == username:
                self.table.item(row, 2).setText(password)
                find_flag = True
                break
        if not find_flag:  # 如果没有找到对应的用户名
            QMessageBox.information(self, 'prompt', 'Can not find the username {}'.format(username))

    def refresh(self):
        """重新加载数据库并显示"""
        self.table.clearContents()
        self.check_list.clear()
        self.table.setRowCount(0)
        self.database.create_table()
        self.get_all_user()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    admin = AdminWindow()
    admin.show()
    sys.exit(app.exec_())
