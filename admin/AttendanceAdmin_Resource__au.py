from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage

from AttendanceAdmin_Resource__wd import FieldFrame, LineEdit, HLine
from AttendanceAdmin_Resource__ut import is_email_address, ModIcon
from AttendanceAdmin_Resource__sr import *


qss = """
LoginUI {
    background: #f8fafb;
}

HLine {
    color: #ddd;
}

#logoLabel {
    font-weight: 700;
    font-size: 14px;
    color: #333;
}

#welcomeTextLabel {
    font-weight: 300;
    font-size: 32px;
    color: #333;
}

#otherTextLabel {
    font-size: 12px;
    color: #333;
}

#label {
    font-size: 12px;
    color: #777;
}

#usernameLineEditFrame {
    background: %s;
    color: #333;
    font-size: 14px;
    border-radius: 5px;
    border: 1px solid #e5e5e5;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 0px;
}

#passwordLineEditFrame {
    background: %s;
    color: #333;
    font-size: 14px;
    border-radius: 5px;
    border: 1px solid #e5e5e5;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
    border-top: None;
}

#label {
    font-size: 12px;
    color: #777
}

LineEdit {
    background: %s;
    font-size: 14px;
}

#loginButton {
    background: rgba(66, 133, 244, 1);
    border-radius: 5px;
    color: #fff;
    font-weight: 700;
}

#createAccountButton {
    background: #fff;
    color: #333;
    font-weight: 700;
    border-radius: 5px;
    border: 1px solid #e5e5e5;
}
"""


def update_username_frame_style(frame: QFrame, focused=False): 
    bg = '#fff' if focused else '#eef2f5'
    frame.setStyleSheet(qss % (bg, bg, bg))


def update_password_frame_style(frame: QFrame, focused=False): 
    bg = '#fff' if focused else '#eef2f5'
    frame.setStyleSheet(qss % (bg, bg, bg))


class LoginUI(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.logo_label = QLabel('ADMIN PANEL')
        self.username_line_edit_frame = FieldFrame()
        self.password_line_edit_frame = FieldFrame()
        self.username_line_edit = LineEdit(self.username_line_edit_frame, update_username_frame_style)
        self.password_line_edit = LineEdit(self.password_line_edit_frame, update_password_frame_style)
        self.username_validation_status_label = QLabel()
        self.login_button = QPushButton('Login Now')
        self.create_account_button = QPushButton('Create Account')

        self.setup_ui()

    def setup_ui(self):
        welcome_text_label = QLabel('Welcome Back!')
        other_text_label = QLabel('Please login with your credentials to \ncontinue.')
        main_layout = QVBoxLayout(self)

        self.logo_label.setObjectName('logoLabel')
        self.logo_label.setContentsMargins(10, 5, 0, 10)

        welcome_text_label.setObjectName('welcomeTextLabel')
        other_text_label.setObjectName('otherTextLabel')

        welcome__layout = QVBoxLayout()
        welcome__layout.addWidget(welcome_text_label)
        welcome__layout.addWidget(other_text_label)
        welcome__layout.setContentsMargins(10, 0, 10, 50)

        self.password_line_edit.setEchoMode(LineEdit.EchoMode.Password)

        self.username_line_edit_frame.set_label_text('Email Address')
        self.username_line_edit_frame.set_line_edit(self.username_line_edit)
        self.username_line_edit_frame.set_validation_status_label(self.username_validation_status_label)
        self.username_line_edit_frame.setup('usernameLineEditFrame')

        self.username_line_edit.textChanged.connect(self.handle_username_text_change)
        self.username_validation_status_label.hide()

        self.password_line_edit_frame.set_label_text('Password')
        self.password_line_edit_frame.set_line_edit(self.password_line_edit)
        self.password_line_edit_frame.setup('passwordLineEditFrame')
    
        fields_layout = QVBoxLayout()
        fields_layout.addWidget(self.username_line_edit_frame)
        fields_layout.addWidget(self.password_line_edit_frame)
        fields_layout.setContentsMargins(10, 0, 10, 0)
        fields_layout.setSpacing(0)

        self.login_button.setMinimumHeight(35)
        self.login_button.setObjectName('loginButton')

        separator__1 = HLine()
        separator_label = QLabel('Or')
        separator__2 = HLine()

        separator_label.setMaximumWidth(20)
        separator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        separator_layout = QHBoxLayout()
        separator_layout.addWidget(separator__1)
        separator_layout.addWidget(separator_label)
        separator_layout.addWidget(separator__2)

        self.create_account_button.setMinimumHeight(35)
        self.create_account_button.setObjectName('createAccountButton')

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.login_button)
        # buttons_layout.addLayout(separator_layout)
        # buttons_layout.addWidget(self.create_account_button)
        buttons_layout.setContentsMargins(10, 53, 10, 0)
        buttons_layout.setSpacing(15)

        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(self.logo_label)
        main_layout.addLayout(welcome__layout)
        main_layout.addLayout(fields_layout)
        main_layout.addLayout(buttons_layout)

        self.setMinimumSize(270, 503)
        self.setMaximumSize(270, 503)
        self.setStyleSheet(qss % ('#eef2f5', '#eef2f5', '#eef2f5'))

    def handle_username_text_change(self, text: str):
        self.username_validation_status_label.show()

        if is_email_address(text):
            self.username_validation_status_label.setPixmap(ModIcon(QImage(':/images/ok_24px.png')).set_color('#198754').set_size(18).get_pixmap())
        else:
            self.username_validation_status_label.setPixmap(ModIcon(QImage(':/images/cancel_24px.png')).set_color('tomato').set_size(18).get_pixmap())
