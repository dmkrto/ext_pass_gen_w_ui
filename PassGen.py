import string
import secrets
import sys

from PyQt5.QtCore import QTimer, QEventLoop
from PyQt5.Qt import QApplication, QSlider, Qt
from PyQt5.QtWidgets import *

special_characters = '-_!@#$%&*()+'
password_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + special_characters
passwords_list = []
gen_titles_list = ['abc', 'ABC', '123', 'spec']
password_length = 8


class DlgMAin(QDialog):
    def __init__(self, passwords_list):
        super().__init__()
        self.setWindowTitle('PassGen')
        self.resize(400, 450)
        self.passwords_list = passwords_list

        self.ledPass1 = QLineEdit('', self)
        self.ledPass2 = QLineEdit('', self)
        self.ledPass3 = QLineEdit('', self)
        self.ledPass4 = QLineEdit('', self)
        self.ledPass5 = QLineEdit('', self)
        self.ledPass6 = QLineEdit('', self)
        self.ledPass7 = QLineEdit('', self)
        self.ledPass8 = QLineEdit('', self)
        self.ledPass9 = QLineEdit('', self)
        self.ledPass10 = QLineEdit('', self)
        self.btnCopy1 = QPushButton('Copy', self)
        self.btnCopy2 = QPushButton('Copy', self)
        self.btnCopy3 = QPushButton('Copy', self)
        self.btnCopy4 = QPushButton('Copy', self)
        self.btnCopy5 = QPushButton('Copy', self)
        self.btnCopy6 = QPushButton('Copy', self)
        self.btnCopy7 = QPushButton('Copy', self)
        self.btnCopy8 = QPushButton('Copy', self)
        self.btnCopy9 = QPushButton('Copy', self)
        self.btnCopy10 = QPushButton('Copy', self)

        self.btnGenerate = QPushButton('Generate', self)
        self.btnGenerate.resize(70, 50)
        self.btnGenerate.move(315, 180)
        self.btnGenerate.clicked.connect(self.evt_btn_generate_clicked)

        self.chk_abc = QCheckBox('abc', self)
        self.chk_abc.move(330, 30)
        self.chk_abc.setChecked(True)
        self.chk_abc.toggled.connect(self.evt_chk_toggled)

        self.chk_ABC = QCheckBox('ABC', self)
        self.chk_ABC.move(330, 60)
        self.chk_ABC.setChecked(True)
        self.chk_ABC.toggled.connect(self.evt_chk_toggled)

        self.chk_123 = QCheckBox('123', self)
        self.chk_123.move(330, 90)
        self.chk_123.setChecked(True)
        self.chk_123.toggled.connect(self.evt_chk_toggled)

        self.chk_spec = QCheckBox('#$%', self)
        self.chk_spec.move(330, 120)
        self.chk_spec.setChecked(True)
        self.chk_spec.toggled.connect(self.evt_chk_toggled)

        self.sld_pass_length = QSlider(Qt.Horizontal, self)
        self.sld_pass_length.setGeometry(50, 350, 200, 30)
        self.sld_pass_length.setMinimum(1)
        self.sld_pass_length.setMaximum(99)
        self.sld_pass_length.setValue(8)
        self.sld_pass_length.setSingleStep(1)
        self.sld_pass_length.setPageStep(1)
        self.sld_pass_length.valueChanged.connect(self.evt_set_password_length)

        self.ledPasswordLength = QLineEdit('8',self)
        self.ledPasswordLength.setGeometry(270, 350, 20, 20)
        self.ledPasswordLength.setReadOnly(True)

        for i in range(1, 11):
            getattr(self, "ledPass{}".format(i)).move(50, 30 * i)
            getattr(self, "ledPass{}".format(i)).setReadOnly(True)

            getattr(self, "btnCopy{}".format(i)).move(200, 30 * i)
            getattr(self, "btnCopy{}".format(i)).clicked.connect(self.evt_btn_clicked)
            getattr(self, "btnCopy{}".format(i)).setObjectName(str(i))
        self.set_passwords()

    def evt_set_password_length(self, pass_len):
        global password_length
        password_length = pass_len
        self.ledPasswordLength.setText(str(pass_len))

    def evt_chk_toggled(self, is_checked):
        global password_chars
        global gen_titles_list
        if is_checked:
            if self.sender().text() == 'abc':
                password_chars = password_chars + string.ascii_lowercase
                gen_titles_list.append('abc')
            elif self.sender().text() == 'ABC':
                password_chars = password_chars + string.ascii_uppercase
                gen_titles_list.append('ABC')
            elif self.sender().text() == '123':
                password_chars = password_chars + string.digits
                gen_titles_list.append('123')
            elif self.sender().text() == '#$%':
                password_chars = password_chars + special_characters
                gen_titles_list.append('spec')
        else:
            if self.sender().text() == 'abc':
                password_chars = password_chars.replace(string.ascii_lowercase, '')
                gen_titles_list.remove('abc')
            elif self.sender().text() == 'ABC':
                password_chars = password_chars.replace(string.ascii_uppercase, '')
                gen_titles_list.remove('ABC')
            elif self.sender().text() == '123':
                password_chars = password_chars.replace(string.digits, '')
                gen_titles_list.remove('123')
            elif self.sender().text() == '#$%':
                password_chars = password_chars.replace(special_characters, '')
                gen_titles_list.remove('spec')

        if len(gen_titles_list) == 1:
            getattr(self, "chk_{}".format(gen_titles_list[0])).setEnabled(False)
        elif len(gen_titles_list) == 2:
            getattr(self, "chk_{}".format(gen_titles_list[0])).setEnabled(True)

    def set_passwords(self):

        for i in range(1, 11):
            getattr(self, "ledPass{}".format(i)).setText(passwords_list[i - 1])

    def evt_btn_generate_clicked(self):
        passwords_list.clear()
        pass_gen(password_chars)
        self.set_passwords()

    def evt_btn_clicked(self):
        btn_number_pushed = self.sender().objectName()
        password = getattr(self, "ledPass{}".format(btn_number_pushed)).text()
        QApplication.clipboard().setText(password)
        getattr(self, "ledPass{}".format(btn_number_pushed)).setText('---COPIED---')
        getattr(self, "btnCopy{}".format(btn_number_pushed)).setEnabled(False)
        loop = QEventLoop()
        QTimer.singleShot(700, loop.quit)
        loop.exec_()
        getattr(self, "ledPass{}".format(btn_number_pushed)).setText(password)
        getattr(self, "btnCopy{}".format(btn_number_pushed)).setEnabled(True)


def pass_gen(password_chars):
    global password_length
    i = 0
    while i < 10:
        password = ''.join(secrets.choice(password_chars) for i in range(password_length))
        passwords_list.append(password)
        i += 1


if __name__ == '__main__':
    pass_gen(password_chars)
    app = QApplication(sys.argv)  # create application
    dlgMain = DlgMAin(passwords_list)  # create main GUI window
    dlgMain.show()  # show GUI
    sys.exit(app.exec_())  # execute the application
