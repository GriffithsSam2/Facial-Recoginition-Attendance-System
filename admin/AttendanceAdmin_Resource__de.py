import math
from PySide6.QtWidgets import QFrame, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QScroller, QPushButton
from PySide6.QtGui import QImage, QPalette, QBrush
from PySide6.QtCore import Qt, QSize, Signal

from AttendanceAdmin_Resource__wd import (
    AddButton,
    MenuButton,
    PaginationButton,
    SideFrame,
    SlidingStackedWidget, 
    QScrollArea, 
    IconButton, 
    HomeButton
)

from BlurWindow.blurWindow import blur


class Label(QLabel):
    def __init__(self, text: str):
        super().__init__(text)

        self.setContentsMargins(20, 0, 0, 0)
        self.setObjectName('label')


class TopFrame(QFrame):
    __qss__ = """
    #titleLabel {
        font-size: 32px;
        font-weight: 300;
        color: #f8fafb;
    }
    """ # This style will only be available to TopFrame object. 

    def __init__(self):
        super().__init__()

        self.menu_button = MenuButton()
        
        menu_lay = QHBoxLayout()
        menu_lay.addWidget(self.menu_button)
        menu_lay.setContentsMargins(0, 3, 0, 0)

        self.title_label = QLabel('Admin Panel')
        self.title_label.setObjectName('titleLabel')
        
        layout__1 = QHBoxLayout()
        layout__1.addLayout(menu_lay)
        layout__1.addWidget(self.title_label)
        layout__1.setSpacing(5)
        layout__1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.logout_button = IconButton(':/images/logout_rounded_left_24px.png', 24)
        self.logout_button.setCursor(Qt.CursorShape.PointingHandCursor)

        main_layout = QHBoxLayout(self)
        main_layout.addLayout(layout__1)
        main_layout.addStretch(1)
        main_layout.addWidget(self.logout_button)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.setContentsMargins(20, 10, 10, 10)

        self.setStyleSheet(self.__qss__)


class HomeUI(QFrame):
    __qss__ = """
        #label {
            color: #fff;
            font-weight: 600;
            font-size: 13px;
        }

        QScrollArea,
        #widget {
            background: none;
            border: none;
        }
    """

    def __init__(self):
        super().__init__()

        self.last_time_move = 0

        label__1 = Label('Quick Access')
        label__2 = Label('Main')
        label__3 = Label('Control Center')

        self.add_semester_button = HomeButton('Add Semester', ':/images/Plus_48px.png')
        self.lecturers_button = HomeButton('Lecturers', ':/images/training_48px.png')
        self.students_button = HomeButton('Students', ':/images/mortarboard_48px.png')
        self.semesters_button = HomeButton('Semesters', ':/images/calendar_48px.png')
        self.users_button = HomeButton('Users', ':/images/user_account_48px.png')
        self.settings_button = HomeButton('Settings', ':/images/settings_48px.png')

        layout__1 = QHBoxLayout()
        layout__1.addWidget(self.add_semester_button)
        layout__1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout__1.setContentsMargins(20, 0, 0, 5)

        widget = QWidget()
        widget.setObjectName('widget')
        widget.setStyleSheet('background: rgba(0, 0, 0, 0);')
        blur(widget.winId())

        self.drag_scrollarea = QScrollArea()
        self.drag_scrollarea.setWidget(widget)
        self.drag_scrollarea.setWidgetResizable(True)
        self.drag_scrollarea.setFrameShape(QFrame.NoFrame)
        self.drag_scrollarea.installEventFilter(self)
        self.drag_scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.drag_scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.drag_scrollarea.setContentsMargins(0, 0, 0, 0)
        self.drag_scrollarea.setStyleSheet('background: rgba(0, 0, 0, 0); ')
        blur(self.drag_scrollarea.winId())

        QScroller.grabGesture(self.drag_scrollarea.viewport(),QScroller.LeftMouseButtonGesture)

        layout__2 = QHBoxLayout(widget)
        layout__2.addWidget(self.semesters_button)
        layout__2.addWidget(self.lecturers_button)
        layout__2.addWidget(self.students_button)
        layout__2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout__2.setContentsMargins(20, 0, 20, 5)

        layout__3 = QHBoxLayout()
        layout__3.addWidget(self.users_button)
        layout__3.addWidget(self.settings_button)
        layout__3.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout__3.setContentsMargins(20, 0, 0, 0)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        main_layout.addWidget(label__1)
        main_layout.addLayout(layout__1)

        main_layout.addWidget(label__2)
        main_layout.addWidget(self.drag_scrollarea)

        main_layout.addWidget(label__3)
        main_layout.addLayout(layout__3)
        main_layout.setContentsMargins(0, 0, 0, 20)

        self.setStyleSheet(self.__qss__)


class SemestersUI(QFrame):
    __qss__ = """
        QLineEdit {
            border-radius: 5px;
            border: 2px solid #fafafa;
            padding: 7px;
            background: rgba(255, 255, 255, 0.3);
            color: #fafafa;
            font-weight: 600;
            font-size: 13px;
        }

        QLineEdit:focus {
            border: 2px solid rgba(66, 133, 244, 1);
        }
    """ 

    countChanged = Signal(int)

    def __init__(self):
        super().__init__()

        self.semester_page = 1
        self.semester_count = 0

        self.menu_button = MenuButton()

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText('Search semester')
        blur(self.search_field.winId())
        
        self.search_button = QPushButton('Search')
        self.search_button.setObjectName('searchButton')
        self.search_button.setMinimumSize(75, 35)
        blur(self.search_button.winId())

        self.add_semester_button = AddButton()
        self.add_semester_button.setMinimumSize(34, 34)
        blur(self.add_semester_button.winId())

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.menu_button)
        search_layout.addWidget(self.search_field)
        search_layout.addWidget(self.search_button)
        search_layout.addStretch(1)
        search_layout.addWidget(self.add_semester_button)
        search_layout.setContentsMargins(5, 10, 10, 10)

        self.central_widget = SlidingStackedWidget()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(search_layout)
        self.main_layout.addWidget(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setStyleSheet(self.__qss__)


class MembersUI(QFrame):
    __qss__ = """
        QLineEdit {
            border-radius: 5px;
            border: 2px solid #fafafa;
            padding: 7px;
            background: rgba(255, 255, 255, 0.3);
            color: #fafafa;
            font-weight: 600;
            font-size: 13px;
        }

        QLineEdit:focus {
            border: 2px solid rgba(66, 133, 244, 1);
        }
    """ 

    countChanged = Signal(int)

    def __init__(self):
        super().__init__()

        self.members_page = 1
        self.members_count = 0

        self.menu_button = MenuButton()

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText('Search student')
        blur(self.search_field.winId())
        
        self.search_button = QPushButton('Search')
        self.search_button.setObjectName('searchButton')
        self.search_button.setMinimumSize(75, 35)
        blur(self.search_button.winId())

        self.add_member_button = AddButton()
        self.add_member_button.setMinimumSize(34, 34)
        blur(self.add_member_button.winId())

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.menu_button)
        search_layout.addWidget(self.search_field)
        search_layout.addWidget(self.search_button)
        search_layout.addStretch(1)
        search_layout.addWidget(self.add_member_button)
        search_layout.setContentsMargins(5, 10, 10, 10)

        self.central_widget = SlidingStackedWidget()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(search_layout)
        self.main_layout.addWidget(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setStyleSheet(self.__qss__)


class CentralWidget(SlidingStackedWidget):
    def __init__(self):
        super().__init__()

        self.switched_idx = 0
        
        self.home_ui = HomeUI()
        self.semesters_ui = SemestersUI()
        self.lecturers_ui = MembersUI()
        self.students_ui = MembersUI()
        self.users_ui = MembersUI()

        self.addWidget(self.home_ui)
        self.addWidget(self.semesters_ui)
        self.addWidget(self.lecturers_ui)
        self.addWidget(self.students_ui)
        self.addWidget(self.users_ui)


class BottomFrame(QFrame):
    active_button: PaginationButton

    def __init__(self):
        super().__init__()
        self._pagination_callback_func = None
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setContentsMargins(15, 0, 15, 10)

    def set_pagination_callback_func(self, callback_func):
        self._pagination_callback_func = callback_func

    def _callback(self, button: PaginationButton):
        self.active_button.apply_inactive_style()
        self.active_button = button
        
        button.apply_active_style()

        self._pagination_callback_func(int(button.text()))

    def update_buttons(self, page_size):
        buttons = self.findChildren(PaginationButton, 'button')

        if buttons:
            for button in buttons:
                button.deleteLater()

            self.update()

        for i in range(1, math.ceil(page_size/6)+1):
            button = PaginationButton(str(i))
            button.clicked.connect(lambda f=self._callback, x=button: f(x))

            if i == 1:
                self.active_button = button
                button.apply_active_style()

            self.main_layout.addWidget(button)
    

class AttendanceAdminUI(QFrame):
    __qss__ = """
        #innerFrame {
            background: rgba(0, 0, 0, 0.5);
        }

        #searchButton {
            border-radius: 5px;
            border: 2px solid rgba(66, 133, 244, 1);
            padding: 8px;
            background: rgba(66, 133, 244, 0.7);
            color: #fafafa;
            font-weight: 600;
            font-size: 13px;
        }
    """

    def __init__(self, callback=None):
        super().__init__() 

        self.callback = callback
        
        self.top_frame = TopFrame()
        self.central_widget = CentralWidget()
        self.bottom_frame = BottomFrame()

        self.side_frame: SideFrame

        self.central_widget.semesters_ui.countChanged.connect(self.bottom_frame.update_buttons)
        self.central_widget.lecturers_ui.countChanged.connect(self.bottom_frame.update_buttons)
        self.central_widget.students_ui.countChanged.connect(self.bottom_frame.update_buttons)
        self.central_widget.users_ui.countChanged.connect(self.bottom_frame.update_buttons)
        
        self.setup_ui()
    
    def setup_ui(self):
        inner_frame = QFrame(self)
        main_layout = QVBoxLayout(inner_frame)

        main_layout.addWidget(self.top_frame)
        main_layout.addWidget(self.central_widget)
        main_layout.addWidget(self.bottom_frame)
        main_layout.setStretch(1, 1)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        bg = QImage(':/images/bg__3.jpg')
        bg = bg.scaled(QSize(370, 650))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(bg))    

        inner_frame.setObjectName('innerFrame')
        inner_frame.setMinimumSize(370, 650)
        inner_frame.setMaximumSize(370, 650)
        inner_frame.setContentsMargins(0, 0, 0, 0)

        blur(inner_frame.winId())

        self.setWindowFlags(self.windowFlags() & ~ Qt.WindowMaximizeButtonHint & ~ Qt.WindowCloseButtonHint)
        self.setPalette(palette)
        self.setMinimumSize(370, 650)
        self.setMaximumSize(370, 650)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('Home')
        self.setStyleSheet(self.__qss__)

        self.side_frame = SideFrame(self)
        self.side_frame.hide()

    def closeEvent(self, event) -> None:
        self.callback()
        self.close()
        return super().closeEvent(event)
