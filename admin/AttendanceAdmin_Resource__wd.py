import urllib.request

from PySide6.QtWidgets import (
    QLineEdit, 
    QFrame, 
    QLabel, 
    QVBoxLayout, 
    QHBoxLayout,
    QStackedWidget, 
    QWidget, 
    QPushButton, 
    QScrollArea,
    QDialog,
    QRadioButton,
    QLayout,
    QSizePolicy,
    QFileDialog,
    QCheckBox
)
from PySide6.QtGui import QImage, QPixmap, QPainter
from PySide6.QtCore import (
    Qt, 
    QTimeLine, 
    QEasingCurve, 
    QPoint, 
    QParallelAnimationGroup, 
    QPropertyAnimation, 
    QAbstractAnimation, 
    QSize,
    QMargins,
    QRect,
    Signal
)

from AttendanceAdmin_Resource__ut import ModIcon, rounded_image, drop_shadow
from AttendanceAdmin_Resource__sr import *

from BlurWindow.blurWindow import blur


class Line(QFrame):
    def __init__(self, orientation):
        super().__init__()
        self.setFrameShape(orientation)
        self.setMinimumHeight(1)
        self.setMaximumHeight(1)


class HLine(Line):
    def __init__(self):
        super().__init__(QFrame.HLine)
    

class VLine(Line):
    def __init__(self):
        super().__init__(QFrame.VLine)


class LineEdit(QLineEdit):
    """Custom QLineEdit with ability to change it parent frame background according to it's focus event.
    
    Parameters
    ----------
    style_func: function
        Style function to use to set new style to LineEdit.

    Returns
    ---
    None: None
    """
    def __init__(self, frame, style_func):
        super().__init__()
        self.frame = frame
        self.style_func = style_func

    def focusInEvent(self, event) -> None:
        super().focusInEvent(event)
        self.style_func(self.frame, focused=True)
        event.accept()

    def focusOutEvent(self, event) -> None:
        super().focusOutEvent(event)
        self.style_func(self.frame, focused=False)
        event.accept()


class FieldFrame(QFrame):
    def __init__(self):
        super().__init__()
        self._label_text = None
        self._line_edit = None
        self._validation_status_label = None

    def set_label_text(self, label_text: str):
        self._label_text = label_text

    def set_line_edit(self, line_edit: LineEdit):
        self._line_edit = line_edit
        self._line_edit.setFrame(QFrame.NoFrame)

    def set_validation_status_label(self, validation_status_label):
        self._validation_status_label = validation_status_label

    def setup(self, object_name: str):
        label = QLabel(self._label_text)
        icon_label = QLabel()

        label.setObjectName('label')
        label.setContentsMargins(1, 0, 0, 0)

        if self._label_text == 'Email Address':
            label_icon = ':/images/mail_24px.png' 
            self._line_edit.setPlaceholderText('user@example.com') 
        else:
            label_icon = ':/images/key_24px.png'
            self._line_edit.setPlaceholderText('Enter password')

        icon_label.setPixmap(ModIcon(QImage(label_icon)).set_color('#959595').set_size(24).get_pixmap())
        icon_label.setContentsMargins(0, 0, 5, 0)
        
        if self._validation_status_label:
            self._validation_status_label.setPixmap(ModIcon(QImage(':/images/ok_24px.png')).set_color('#198754').set_size(18).get_pixmap())

        field_layout_a = QVBoxLayout()
        field_layout_a.addWidget(label)
        field_layout_a.addWidget(self._line_edit)

        field_layout_b = QHBoxLayout(self)
        field_layout_b.addWidget(icon_label)
        field_layout_b.addLayout(field_layout_a)

        if self._validation_status_label:
            field_layout_b.addWidget(self._validation_status_label)

        field_layout_b.setContentsMargins(20, 10, 20, 10)

        self.setObjectName(object_name)
        self.setFrameStyle(QFrame.Panel)

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        self._line_edit.setFocus()
        event.accept()


class SidebarPicFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.pic_label = QLabel()
        self.pic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.pic_label)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setContentsMargins(1, 1, 1, 1)

    def set_pic(self, image: QImage, size: int):
        self.setMinimumSize(size, size)
        self.setMaximumSize(size, size)
        self.pic_label.setPixmap(rounded_image(image, size))

        self.setStyleSheet("""
            SidebarPicFrame {
                background: #fff;
                border-radius: %spx;
            }
        """ % (str(int(size/2))))


class FaderWidget(QWidget):
    def __init__(self, old_widget, new_widget):
        super(QWidget, self).__init__(self, new_widget)

        self.oldPixmap = QPixmap(new_widget.size())
        old_widget.render(self.oldPixmap)
        self.pixmapOpacity = 1.0

        self.timeLine = QTimeLine()
        self.timeLine.valueChanged.connect(self.animate)
        self.timeLine.finished.connect(self.close)
        self.timeLine.setDuration(2000)
        self.timeLine.start()

        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmapOpacity)
        painter.drawPixmap(0, 0, self.oldPixmap)
        painter.end()

    def animate(self, value):
        self.pixmapOpacity = 1.0 - value
        self.repaint()


class SlidingStackedWidget(QStackedWidget):
    def __init__(
            self, parent=None, direction=Qt.Orientation.Horizontal, speed=300,
            animationType=QEasingCurve.Type.OutCubic) -> None:
        super(SlidingStackedWidget, self).__init__(parent)

        self.fadeSlide = False
        self.faderWidget = None
        self.sswDirection = direction
        self.sswSpeed = speed
        self.sswAnimationType = animationType
        self.sswNow = 0
        self.sswNext = 0
        self.sswWrap = False
        self.sswPoint = QPoint(0, 0)
        self.sswActive = False

    def setDirection(self, direction) -> None:
        self.sswDirection = direction

    def setSpeed(self, speed) -> None:
        self.sswSpeed = speed

    def setAnimation(self, animationType) -> None:
        self.sswAnimationType = animationType

    def setWrap(self, wrap) -> None:
        self.sswWrap = wrap

    def slideInPrev(self) -> None:
        now = self.currentIndex()
        if self.sswWrap or now > 0:
            self.slideInIdx(now - 1)

    def slideInNext(self) -> None:
        now = self.currentIndex()
        if self.sswWrap or now < (self.count() - 1):
            self.slideInIdx(now + 1)

    def slideInIdx(self, idx) -> None:
        if idx > (self.count() - 1):
            idx = idx % self.count()
        elif idx < 0:
            idx = (idx + self.count()) % self.count()
        self.slideInWgt(self.widget(idx))

    def slideInWgt(self, newWidget) -> None:
        if self.sswActive:
            return

        self.sswActive = True

        _now = self.currentIndex()
        _next = self.indexOf(newWidget)

        if _now == _next:
            self.sswActive = False
            return

        offsetX, offsetY = self.frameRect().width(), self.frameRect().height()
        self.widget(_next).setGeometry(self.frameRect())

        if not self.sswDirection == Qt.Horizontal:
            if _now < _next:
                offsetX, offsetY = 0, -offsetY
            else:
                offsetX = 0
        else:
            if _now < _next:
                offsetX, offsetY = -offsetX, 0
            else:
                offsetY = 0

        pNext = self.widget(_next).pos()
        pNow = self.widget(_now).pos()
        self.sswPoint = pNow

        offset = QPoint(offsetX, offsetY)
        self.widget(_next).move(pNext - offset)
        self.widget(_next).show()
        self.widget(_next).raise_()

        animationGroup = QParallelAnimationGroup(self, finished=self.animationDoneSlot)

        for index, start, end in zip(
                (_now, _next), (pNow, pNext - offset), (pNow + offset, pNext)):
            animation = QPropertyAnimation(
                self.widget(index),
                b"pos",
                duration=self.sswSpeed,
                easingCurve=self.sswAnimationType,
                startValue=start,
                endValue=end,
            )
            animationGroup.addAnimation(animation)

        self.sswNext = _next
        self.sswNow = _now
        self.sswActive = True
        animationGroup.start(QAbstractAnimation.DeleteWhenStopped)

    def setCurrentIndex(self, index) -> None:
        if self.fadeSlide:
            self.faderWidget = FaderWidget(self.currentWidget(), self.widget(index))
        QStackedWidget.setCurrentIndex(self, index)

    def animationDoneSlot(self) -> None:
        self.setCurrentIndex(self.sswNext)
        self.widget(self.sswNow).hide()
        self.widget(self.sswNow).move(self.sswPoint)
        self.sswActive = False


class HomeButton(QPushButton):
    __qss__ = """
        HomeButton {
            background: rgba(255, 255, 255, 0.75);
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #e5e5e5;
        }

        HomeButton:hover {
            background: rgba(66, 133, 244, 0.8);;
            border: none;
        }
    """

    def __init__(self, text: str, iconfile: str):
        super().__init__()

        self.modicon = ModIcon(QImage(iconfile))

        self.icon_label = QLabel()
        self.icon_label.setPixmap(self.modicon.set_color('#555').set_size(48).get_pixmap())
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setStyleSheet('color: #555; font-size: 14px; font-weight: 600;')

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.icon_label)
        main_layout.addWidget(self.text_label)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setMinimumSize(150, 150)
        self.setMaximumSize(150, 150)
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(self.__qss__)
        blur(self.winId())

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.icon_label.setPixmap(self.modicon.set_color('#fff').set_size(48).get_pixmap())
        self.text_label.setStyleSheet('color: #fff; font-size: 14px; font-weight: 600;')
        event.accept()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.icon_label.setPixmap(self.modicon.set_color('#555').set_size(48).get_pixmap())
        self.text_label.setStyleSheet('color: #555; font-size: 14px; font-weight: 600;')
        event.accept()


class IconButton(QPushButton):
    def __init__(self, filename: str, size, color='#f8fafb', icon_hover_color='#fff'):
        super().__init__()

        self.modicon = ModIcon(QImage(filename))

        self.color = color
        self.icon_focus_color = icon_hover_color

        self.setIcon(self.modicon.set_color(self.color).get_icon())
        self.setIconSize(QSize(size, size))
        self.setFlat(True)
        self.setStyleSheet("""
            IconButton {
                padding: 5px;
                border-radius: 5px;
            }
        """)

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.setIcon(self.modicon.set_color(self.icon_focus_color).get_icon())
        event.accept()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.setIcon(self.modicon.set_color(self.color).get_icon())
        event.accept()


class ScrollArea(QScrollArea):
    def __init__(self, widget: QWidget):
        super().__init__()

        self.setWidget(widget)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.NoFrame)


class FramelessContentFrame(QFrame):
    def __init__(self, parent):
        super(FramelessContentFrame, self).__init__()
        blur(self.winId())
        self.setGraphicsEffect(drop_shadow(parent))


class Frameless(QDialog):

    def __init__(self, parent):
        super(Frameless, self).__init__(parent)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.contentFrame = FramelessContentFrame(self)

        mainLay = QVBoxLayout(self)
        mainLay.addWidget(self.contentFrame)
        mainLay.setContentsMargins(1, 1, 1, 1)

        self.setContentsMargins(20, 0, 0, 0)


class DragScrollArea(QScrollArea):
    def __init__(self, widget: QWidget):
        super().__init__()

        self.setWidgetResizable(True)
        self.setWidget(widget)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet('background: none; border: none;')



class FormField(QFrame):
    def __init__(self, label_text, placeholder):
        super().__init__()

        label = QLabel(label_text)
        label.setObjectName('label')

        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText(placeholder)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.lineEdit)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setMinimumHeight(80)


class SemesterDialog(Frameless):
    class Label(QLabel):
        def __init__(self, text: str):
            super().__init__(text)

    __qss__ = """
    FramelessContentFrame {
        background: rgba(255, 255, 255, 0.97);
        border-radius: 5px;
    }

    #titleLabel {
        color: #444;
        font-weight: 600;
        font-size: 24px;
    }

    #label {
        font-size: 14px;
        color: #333;
    }

    QLineEdit {
        border-radius: 5px;
        border: 2px solid #333;
        padding: 7px;
    }

    QLineEdit:focus {
        border: 2px solid rgba(66, 133, 244, 1);
    }

    #cancelButton,
    #editButton  {
        background: #fff;
        color: #333;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid #d3d3d3;
        border-radius: 5px;
        padding: 7px;
    }

    #deleteButton {
        background: rgba(234, 67, 53, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }

    #saveButton {
        background: rgba(66, 133, 244, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }
    """

    def __init__(self, parent):
        super().__init__(parent)
        
        top_frame = QFrame()

        self.title_label = QLabel('Add Semester')
        self.title_label.setObjectName('titleLabel')

        close_button = IconButton(':/images/close_48px.png', 16, '#333', '#EA4335')
        close_button.clicked.connect(self.close)

        top_frame_layout = QHBoxLayout(top_frame)
        top_frame_layout.addWidget(self.title_label)
        top_frame_layout.addWidget(close_button)
        top_frame_layout.setStretch(0, 1)
        
        member_frame = QFrame()

        label__1 = QLabel('Select member')
        label__1.setObjectName('label')

        self.lecturers_radio_button = QRadioButton('Lecturers', member_frame)
        self.lecturers_radio_button.clicked.connect(lambda: self.handle_radios_buttons(self.lecturers_radio_button))
        self.lecturers_radio_button.setChecked(True)

        self.students_radio_button = QRadioButton('Students', member_frame)
        self.students_radio_button.clicked.connect(lambda: self.handle_radios_buttons(self.students_radio_button))

        radios_layout = QHBoxLayout()
        radios_layout.addWidget(self.lecturers_radio_button)
        radios_layout.addWidget(self.students_radio_button)

        member_frame_layout = QVBoxLayout(member_frame)
        member_frame_layout.addWidget(label__1)
        member_frame_layout.addLayout(radios_layout)

        self.department_form_field = FormField('Department', 'Enter department')
        self.program_form_field = FormField('Program of Study', 'Enter program of study')
        self.semester_year_form_field = FormField('Semester Year', '2022-2023')
        self.semester_form_field = FormField('Semester', 'Enter semester')
        self.expected_attendance_form_field = FormField('Expected Attendance', 'Enter number of attendance expected')

        self.is_current_cb = QCheckBox()
        self.is_current_cb.setText('Current')

        is_current_cb_layout = QHBoxLayout()
        is_current_cb_layout.addWidget(self.is_current_cb)
        is_current_cb_layout.setContentsMargins(10, 10, 10, 10)

        self.program_form_field.hide()

        self.save_button = QPushButton('SAVE')
        self.save_button.setObjectName('saveButton')

        self.edit_button = QPushButton('EDIT')
        self.edit_button.setObjectName('editButton')

        self.cancel_button = QPushButton('CANCEL')
        self.cancel_button.setObjectName('cancelButton')
        self.cancel_button.clicked.connect(self.handle_cancel_button)

        self.delete_button = QPushButton('DELETE')
        self.delete_button.setObjectName('deleteButton')

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.save_button)
        button_layout.setContentsMargins(9, 20, 10, 9)
        button_layout.setSpacing(20)

        content_layout = QVBoxLayout(self.contentFrame)
        content_layout.addWidget(top_frame)
        content_layout.addWidget(member_frame)
        content_layout.addWidget(self.department_form_field)
        content_layout.addWidget(self.program_form_field)
        content_layout.addWidget(self.semester_year_form_field)
        content_layout.addWidget(self.semester_form_field)
        content_layout.addWidget(self.expected_attendance_form_field)
        content_layout.addLayout(is_current_cb_layout)
        content_layout.addLayout(button_layout)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(0)

        self.contentFrame.setMinimumSize(270, 400)
        self.contentFrame.setStyleSheet(self.__qss__)

    def handle_radios_buttons(self, radio_button: QRadioButton):
        if radio_button.text() == 'Lecturers':
            self.department_form_field.show()
            self.program_form_field.hide()
        else:
            self.department_form_field.hide()
            self.program_form_field.show()

    def set_fields_enabled_state(self, state: bool):
        self.students_radio_button.setEnabled(False)
        self.lecturers_radio_button.setEnabled(False)

        self.department_form_field.setEnabled(state)
        self.program_form_field.setEnabled(state)
        self.semester_year_form_field.setEnabled(state)
        self.semester_form_field.setEnabled(state)
        self.expected_attendance_form_field.setEnabled(state)

        self.is_current_cb.setEnabled(state)

    def handle_cancel_button(self):
        self.save_button.hide()
        self.cancel_button.hide()
        self.edit_button.show()
        self.delete_button.show()
        self.title_label.setText('Semester')
        self.set_fields_enabled_state(False)

class FlowLayout(QLayout):
    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(QMargins(0, 0, 0, 0))

        self._item_list = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self._item_list.append(item)

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list[index]

        return None

    def takeAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self._do_layout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())

        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def _do_layout(self, rect, test_only):
        x = rect.x()
        y = rect.y()
        line_height = 0
        spacing = self.spacing()

        for item in self._item_list:
            style = item.widget().style()
            layout_spacing_x = style.layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal
            )
            layout_spacing_y = style.layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical
            )
            space_x = spacing + layout_spacing_x
            space_y = spacing + layout_spacing_y
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()


class SemesterButton(QPushButton):
    __qss__ = """
        SemesterButton {
            background: rgba(255, 255, 255, 0.75);
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #e5e5e5;
        }

        SemesterButton:hover {
            background: rgba(66, 133, 244, 0.8);;
            border: none;
        }
    """

    def __init__(self, data: dict, iconfile=':/images/mortarboard_48px.png'):
        super().__init__()

        self.data = data

        if self.data['member'] == 'Student':
            self.modicon = ModIcon(QImage(iconfile))
        else:
            self.modicon = ModIcon(QImage(':/images/training_48px.png'))

        self.icon_label = QLabel()
        self.icon_label.setPixmap(self.modicon.set_color('#555').set_size(48).get_pixmap())
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.text_label__1 = QLabel(data['semester_year'])
        self.text_label__1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label__1.setStyleSheet('color: #555; font-size: 14px; font-weight: 600;')

        deP = data['department'] if data['department'] else data['programme']
        self.text_label__2 = QLabel(f'Semester {data["semester"]}\n{deP}')
        self.text_label__2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label__2.setStyleSheet('color: #555; font-size: 12px; font-weight: 600;')
        self.text_label__2.setContentsMargins(0, 5, 0, 0)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.icon_label)
        main_layout.addWidget(self.text_label__1)
        main_layout.addWidget(self.text_label__2)
        main_layout.setSpacing(5)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setMinimumSize(150, 150)
        self.setMaximumSize(150, 150)
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(self.__qss__)
        blur(self.winId())

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.icon_label.setPixmap(self.modicon.set_color('#fff').set_size(48).get_pixmap())
        self.text_label__1.setStyleSheet('color: #fff; font-size: 14px; font-weight: 600;')
        self.text_label__2.setStyleSheet('color: #fff; font-size: 12px; font-weight: 600;')
        event.accept()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.icon_label.setPixmap(self.modicon.set_color('#555').set_size(48).get_pixmap())
        self.text_label__1.setStyleSheet('color: #555; font-size: 14px; font-weight: 600;')
        self.text_label__2.setStyleSheet('color: #555; font-size: 12px; font-weight: 600;')
        event.accept()


class MenuButton(IconButton):
    def __init__(self, filename=':/images/menu_48px.png', size=24, color='#f8fafb'):
        super().__init__(filename, size, color)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

class AddButton(IconButton):
    def __init__(self, filename=':/images/plus_math_48px.png', size=24, color='#f8fafb'):
        super().__init__(filename, size, color)

        blur(self.winId())
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            IconButton {
                border-radius: 17px;
                border: 2px solid rgba(52, 168, 83, 1);
                background: rgba(52, 168, 83, 0.7);
            }
        """)


class MenuItemButton(IconButton):
    __qss__ = """
        IconButton {
            padding: 5px;
            border-radius: 5px;
        }

        IconButton:hover {
            background: rgba(66, 133, 244, 1);
        }
    """

    def __init__(self, filename=':/images/menu_48px.png', size=24, color='#333'):
        super().__init__(filename, size, color)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(self.__qss__)


class SideFrame(QFrame):
    __qss__ = """
        SideFrame {
            background: rgba(255, 255, 255, 0);
        }
        
        #innerFrame {
            background: rgba(255, 255, 255, 1);
            border-radius: 5px;
        }
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.menu_button = MenuItemButton()
        self.menu_button.setToolTip('Hide Menu')

        self.home_button = MenuItemButton(filename=':/images/home_48px.png')
        self.add_semester_button = MenuItemButton(filename=':/images/Plus_48px.png')

        menu_items_top_layout = QVBoxLayout()
        menu_items_top_layout.addWidget(self.home_button)
        menu_items_top_layout.addWidget(self.add_semester_button)
        menu_items_top_layout.setContentsMargins(0, 60, 0, 70)

        self.semesters_button = MenuItemButton(filename=':/images/calendar_48px.png')
        self.lecturers_button = MenuItemButton(filename=':/images/training_48px.png')
        self.students_button = MenuItemButton(filename=':/images/mortarboard_48px.png')

        menu_items_mid_layout = QVBoxLayout()
        menu_items_mid_layout.addWidget(self.semesters_button)
        menu_items_mid_layout.addWidget(self.lecturers_button)
        menu_items_mid_layout.addWidget(self.students_button) 
        menu_items_mid_layout.setContentsMargins(0, 30, 0, 80)

        self.users_button = MenuItemButton(filename=':/images/user_account_48px.png')
        self.settings_button = MenuItemButton(filename=':/images/settings_48px.png')
        self.logout_button = MenuItemButton(filename=':/images/logout_rounded_left_24px.png')

        menu_items_btm_layout = QVBoxLayout()
        menu_items_btm_layout.addWidget(self.users_button)
        menu_items_btm_layout.addWidget(self.settings_button)
        menu_items_btm_layout.addWidget(self.logout_button)

        inner_frame = QFrame()
        inner_frame.setObjectName('innerFrame')
        inner_frame.setGraphicsEffect(drop_shadow(self))

        menu_items_layout = QVBoxLayout(inner_frame)
        menu_items_layout.addWidget(self.menu_button)
        menu_items_layout.addLayout(menu_items_top_layout)
        menu_items_layout.addLayout(menu_items_mid_layout)
        menu_items_layout.addLayout(menu_items_btm_layout)
        menu_items_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        fake_frame = QFrame()

        self.slider_widget = SlidingStackedWidget()
        self.slider_widget.addWidget(inner_frame)
        self.slider_widget.addWidget(fake_frame)

        self.slider_widget.setCurrentIndex(1)

        blur(self.winId())

        layout = QVBoxLayout(self)
        layout.addWidget(self.slider_widget)
        layout.setContentsMargins(10, 10, 0, 10)

        inner_frame.setMinimumWidth(50)
        inner_frame.setMaximumWidth(50)

        fake_frame.setMinimumWidth(50)
        fake_frame.setMaximumWidth(50)

        blur(fake_frame.winId())

        self.setMinimumHeight(650)
        self.setStyleSheet(self.__qss__)


class PaginationButton(QPushButton):
    __qss__ = """
        background: {bg};
        color: {color};
        border-radius: 16px;
        font-weight: 600;
    """

    def __init__(self, text: str):
        super().__init__(text)
        
        self.setMinimumSize(32, 32)
        self.setMaximumSize(32, 32)
        self.setObjectName('button')

        self.apply_inactive_style()

        blur(self.winId())

    def apply_active_style(self):
        self.setStyleSheet(self.__qss__.format(bg='rgba(66, 133, 244, 0.8)', color='#fff'))

    def apply_inactive_style(self):
        self.setStyleSheet(self.__qss__.format(bg='rgba(255, 255, 255, 0.8)', color='#333'))


class MemberButton(QPushButton):
    __qss__  = """
    MemberButton {
        border: none;
        background: none;
    }

    #nameLabel {
        color: #fff;
        font-weight: 600;
        font-size: 13px;
    }
    """

    def __init__(self, data: dict):
        super().__init__()
        
        self.data = data

        self.pic_label = QLabel()
        self.pic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if data['photo']:
            self.set_pic(data['photo'])

        self.name_label = QLabel(f"{data['first_name']} {data['last_name']}")
        self.name_label.setObjectName('nameLabel')
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.pic_label)
        layout.addWidget(self.name_label)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setMinimumSize(92, 150)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(self.__qss__)

    def set_pic(self, pic_url=':/images/user_48px.png'):
        if pic_url != ':/images/user_48px.png':
            image_data = urllib.request.urlopen(pic_url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            pixmap = pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.pic_label.setPixmap(pixmap)
        else:
            self.pic_label.setPixmap(ModIcon(QImage(pic_url)).set_size(156).get_pixmap())


class StudentDialog(Frameless):
    class Label(QLabel):
        def __init__(self, text: str):
            super().__init__(text)

    __qss__ = """
    FramelessContentFrame {
        background: rgba(255, 255, 255, 0.97);
        border-radius: 5px;
    }

    #titleLabel {
        color: #444;
        font-weight: 600;
        font-size: 24px;
    }

    #label {
        font-size: 14px;
        color: #333;
    }

    QLineEdit {
        border-radius: 5px;
        border: 2px solid #333;
        padding: 7px;
    }

    QLineEdit:focus {
        border: 2px solid rgba(66, 133, 244, 1);
    }

    #cancelButton,
    #editButton  {
        background: #fff;
        color: #333;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid #d3d3d3;
        border-radius: 5px;
        padding: 7px;
    }

    #deleteButton {
        background: rgba(234, 67, 53, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }

    #saveButton {
        background: rgba(66, 133, 244, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }

    #attendanceLabel {
        font-size: 18px;
        color: #333;
    }

    #deleteButton {
        background: rgba(234, 67, 53, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }

    #editButton {
        background: rgba(66, 133, 244, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }
    """

    def __init__(self, parent):
        super().__init__(parent)
        
        top_frame = QFrame()

        self.title_label = QLabel('Student Name')
        self.title_label.setObjectName('titleLabel')

        close_button = IconButton(':/images/close_48px.png', 16, '#333', '#EA4335')
        close_button.clicked.connect(self.close)

        top_frame_layout = QHBoxLayout(top_frame)
        top_frame_layout.addWidget(self.title_label)
        top_frame_layout.addWidget(close_button)
        top_frame_layout.setStretch(0, 1)

        self.pic_label = QLabel()
        self.member_label = QLabel('Student')
        self.student_id_label = QLabel('1234567890')
        self.programme_label = QLabel('Programme')
        self.entry_date_label = QLabel('2022-01-01')
        self.attendance_label = QLabel('<small>0</small>/<b>60</b>')
        
        self.attendance_label.setObjectName('attendanceLabel')

        self.edit_button = QPushButton('EDIT')
        self.remove_button = QPushButton('DELETE')

        self.edit_button.setMinimumWidth(70)
        self.remove_button.setMinimumWidth(70)

        self.edit_button.setObjectName('editButton')
        self.remove_button.setObjectName('deleteButton')

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.remove_button)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.setSpacing(10)

        layout__1 = QVBoxLayout()
        layout__1.addWidget(self.member_label)
        layout__1.addWidget(self.student_id_label)
        layout__1.addWidget(self.programme_label)
        layout__1.addWidget(self.entry_date_label)
        layout__1.addWidget(self.attendance_label)
        layout__1.addLayout(buttons_layout)
        layout__1.setSpacing(1)
        layout__1.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        layout__2 = QHBoxLayout()
        layout__2.addWidget(self.pic_label)
        layout__2.addLayout(layout__1)
        layout__2.setSpacing(20)
        layout__2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        content_layout = QVBoxLayout(self.contentFrame)
        content_layout.addWidget(top_frame)
        content_layout.addLayout(layout__2)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(0)

        self.contentFrame.setMinimumSize(300, 200)
        self.contentFrame.setStyleSheet(self.__qss__)

    def set_pic(self, pic_url=':/images/user_48px.png'):
        image_data = urllib.request.urlopen(pic_url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        pixmap = pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.pic_label.setPixmap(pixmap)
        

class CreateEditStudentDialog(Frameless):
    __qss__ = """
        FramelessContentFrame {
            background: rgba(255, 255, 255, 0.97);
            border-radius: 5px;
        }

        #titleLabel {
            color: #444;
            font-weight: 600;
            font-size: 24px;
        }

        #label {
            font-size: 14px;
            color: #333;
        }

        QLineEdit {
            border-radius: 5px;
            border: 2px solid #333;
            padding: 7px;
        }

        QLineEdit:focus {
            border: 2px solid rgba(66, 133, 244, 1);
        }

        #uploadButton {
            background: rgba(66, 133, 244, 1);
            color: #fff;
            font-weight: 600;
            font-size: 14px;
            border: none;
            border-radius: 5px;
            padding: 8px;
        }

    #cancelButton  {
        background: #fff;
        color: #333;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid #d3d3d3;
        border-radius: 5px;
        padding: 7px;
    }

    #saveButton {
        background: rgba(66, 133, 244, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.photo_file = None
        top_frame = QFrame()

        self.title_label = QLabel('Add Student')
        self.title_label.setObjectName('titleLabel')

        close_button = IconButton(':/images/close_48px.png', 16, '#333', '#EA4335')
        close_button.clicked.connect(self.close)

        top_frame_layout = QHBoxLayout(top_frame)
        top_frame_layout.addWidget(self.title_label)
        top_frame_layout.addWidget(close_button)
        top_frame_layout.setStretch(0, 1)

        self.file_lineEdit = QLineEdit()
        self.file_lineEdit.setReadOnly(True)

        self.upload_button = QPushButton('Upload Photo')
        self.upload_button.setObjectName('uploadButton')
        self.upload_button.clicked.connect(self.handle_upload_photo_button)

        layout__1 = QHBoxLayout()
        layout__1.addWidget(self.file_lineEdit)
        layout__1.addWidget(self.upload_button)
        layout__1.setSpacing(5)
        layout__1.setContentsMargins(10, 10, 10, 5)

        self.first_name_form_field = FormField('First Name', 'Enter first name')
        self.last_name_form_field = FormField('Last Name', 'Enter last name')
        self.student_id_form_field = FormField('Student ID', 'Enter student ID')
        self.dob_form_field = FormField('Date of Birth', '2022-01-31')
        self.programme_form_field = FormField('Program of Study', 'Program of study')
        self.entry_date_form_field = FormField('Entry date', '2022-01-31')
        
        layout__2 = QVBoxLayout()
        layout__2.addWidget(self.first_name_form_field)
        layout__2.addWidget(self.last_name_form_field)
        layout__2.addWidget(self.student_id_form_field)
        layout__2.addWidget(self.dob_form_field)
        layout__2.addWidget(self.programme_form_field)
        layout__2.addWidget(self.entry_date_form_field)
        layout__2.setSpacing(10)
        layout__2.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.save_button = QPushButton('SAVE')
        self.save_button.setObjectName('saveButton')

        self.cancel_button = QPushButton('CANCEL')
        self.cancel_button.setObjectName('cancelButton')
        self.cancel_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        button_layout.setContentsMargins(9, 20, 10, 9)
        button_layout.setSpacing(20)

        content_layout = QVBoxLayout(self.contentFrame)
        content_layout.addWidget(top_frame)
        content_layout.addLayout(layout__1)
        content_layout.addLayout(layout__2)
        content_layout.addLayout(button_layout)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(0)

        self.contentFrame.setMinimumSize(300, 200)
        self.contentFrame.setStyleSheet(self.__qss__)

    def handle_upload_photo_button(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', 'C://', filter='Image file (*.jpg *.jpeg *.png)')
        self.file_lineEdit.setText(filename)

################

class CreateEditLecturerDialog(Frameless):
    __qss__ = """
        FramelessContentFrame {
            background: rgba(255, 255, 255, 0.97);
            border-radius: 5px;
        }

        #titleLabel {
            color: #444;
            font-weight: 600;
            font-size: 24px;
        }

        #label {
            font-size: 14px;
            color: #333;
        }

        QLineEdit {
            border-radius: 5px;
            border: 2px solid #333;
            padding: 7px;
        }

        QLineEdit:focus {
            border: 2px solid rgba(66, 133, 244, 1);
        }

        #uploadButton {
            background: rgba(66, 133, 244, 1);
            color: #fff;
            font-weight: 600;
            font-size: 14px;
            border: none;
            border-radius: 5px;
            padding: 8px;
        }

    #cancelButton  {
        background: #fff;
        color: #333;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid #d3d3d3;
        border-radius: 5px;
        padding: 7px;
    }

    #saveButton {
        background: rgba(66, 133, 244, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.photo_file = None
        top_frame = QFrame()

        self.title_label = QLabel('Add Lecturer')
        self.title_label.setObjectName('titleLabel')

        close_button = IconButton(':/images/close_48px.png', 16, '#333', '#EA4335')
        close_button.clicked.connect(self.close)

        top_frame_layout = QHBoxLayout(top_frame)
        top_frame_layout.addWidget(self.title_label)
        top_frame_layout.addWidget(close_button)
        top_frame_layout.setStretch(0, 1)

        self.file_lineEdit = QLineEdit()
        self.file_lineEdit.setReadOnly(True)

        self.upload_button = QPushButton('Upload Photo')
        self.upload_button.setObjectName('uploadButton')
        self.upload_button.clicked.connect(self.handle_upload_photo_button)

        layout__1 = QHBoxLayout()
        layout__1.addWidget(self.file_lineEdit)
        layout__1.addWidget(self.upload_button)
        layout__1.setSpacing(5)
        layout__1.setContentsMargins(10, 10, 10, 5)

        self.first_name_form_field = FormField('First Name', 'Enter first name')
        self.last_name_form_field = FormField('Last Name', 'Enter last name')
        self.dob_form_field = FormField('Date of Birth', '2022-01-31')
        self.department_form_field = FormField('Department', 'Department')
        
        layout__2 = QVBoxLayout()
        layout__2.addWidget(self.first_name_form_field)
        layout__2.addWidget(self.last_name_form_field)
        layout__2.addWidget(self.dob_form_field)
        layout__2.addWidget(self.department_form_field)
        layout__2.setSpacing(0)
        layout__2.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.save_button = QPushButton('SAVE')
        self.save_button.setObjectName('saveButton')

        self.cancel_button = QPushButton('CANCEL')
        self.cancel_button.setObjectName('cancelButton')
        self.cancel_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        button_layout.setContentsMargins(9, 20, 10, 9)
        button_layout.setSpacing(20)

        content_layout = QVBoxLayout(self.contentFrame)
        content_layout.addWidget(top_frame)
        content_layout.addLayout(layout__1)
        content_layout.addLayout(layout__2)
        content_layout.addLayout(button_layout)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(0)

        self.contentFrame.setMinimumSize(300, 200)
        self.contentFrame.setStyleSheet(self.__qss__)

    def handle_upload_photo_button(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', 'C://', filter='Image file (*.jpg *.jpeg *.png)')
        self.file_lineEdit.setText(filename)


class LecturerDialog(Frameless):
    class Label(QLabel):
        def __init__(self, text: str):
            super().__init__(text)

    __qss__ = """
    FramelessContentFrame {
        background: rgba(255, 255, 255, 0.97);
        border-radius: 5px;
    }

    #titleLabel {
        color: #444;
        font-weight: 600;
        font-size: 24px;
    }

    #label {
        font-size: 14px;
        color: #333;
    }

    QLineEdit {
        border-radius: 5px;
        border: 2px solid #333;
        padding: 7px;
    }

    QLineEdit:focus {
        border: 2px solid rgba(66, 133, 244, 1);
    }

    #cancelButton,
    #editButton  {
        background: #fff;
        color: #333;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid #d3d3d3;
        border-radius: 5px;
        padding: 7px;
    }

    #deleteButton {
        background: rgba(234, 67, 53, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }

    #saveButton {
        background: rgba(66, 133, 244, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }

    #attendanceLabel {
        font-size: 18px;
        color: #333;
    }

    #deleteButton {
        background: rgba(234, 67, 53, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }

    #editButton {
        background: rgba(66, 133, 244, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }
    """

    def __init__(self, parent):
        super().__init__(parent)
        
        top_frame = QFrame()

        self.title_label = QLabel('Lecturer Name')
        self.title_label.setObjectName('titleLabel')

        close_button = IconButton(':/images/close_48px.png', 16, '#333', '#EA4335')
        close_button.clicked.connect(self.close)

        top_frame_layout = QHBoxLayout(top_frame)
        top_frame_layout.addWidget(self.title_label)
        top_frame_layout.addWidget(close_button)
        top_frame_layout.setStretch(0, 1)

        self.pic_label = QLabel()
        self.member_label = QLabel('Lecturer')
        self.department_label = QLabel('Programme')
        self.attendance_label = QLabel('<small>0</small>/<b>60</b>')
        
        self.attendance_label.setObjectName('attendanceLabel')

        self.edit_button = QPushButton('EDIT')
        self.remove_button = QPushButton('DELETE')

        self.edit_button.setMinimumWidth(70)
        self.remove_button.setMinimumWidth(70)

        self.edit_button.setObjectName('editButton')
        self.remove_button.setObjectName('deleteButton')

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.remove_button)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.setSpacing(10)

        layout__1 = QVBoxLayout()
        layout__1.addWidget(self.member_label)
        layout__1.addWidget(self.department_label)
        layout__1.addWidget(self.attendance_label)
        layout__1.addStretch(1)
        layout__1.addLayout(buttons_layout)
        layout__1.setSpacing(1)
        layout__1.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        layout__2 = QHBoxLayout()
        layout__2.addWidget(self.pic_label)
        layout__2.addLayout(layout__1)
        layout__2.setSpacing(20)
        layout__2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        content_layout = QVBoxLayout(self.contentFrame)
        content_layout.addWidget(top_frame)
        content_layout.addLayout(layout__2)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(0)

        self.contentFrame.setMinimumSize(300, 200)
        self.contentFrame.setStyleSheet(self.__qss__)

    def set_pic(self, pic_url=':/images/user_48px.png'):
        image_data = urllib.request.urlopen(pic_url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        pixmap = pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.pic_label.setPixmap(pixmap)

#####

class CreateEditUserDialog(Frameless):
    __qss__ = """
        FramelessContentFrame {
            background: rgba(255, 255, 255, 0.97);
            border-radius: 5px;
        }

        #titleLabel {
            color: #444;
            font-weight: 600;
            font-size: 24px;
        }

        #label {
            font-size: 14px;
            color: #333;
        }

        QLineEdit {
            border-radius: 5px;
            border: 2px solid #333;
            padding: 7px;
        }

        QLineEdit:focus {
            border: 2px solid rgba(66, 133, 244, 1);
        }

        #uploadButton {
            background: rgba(66, 133, 244, 1);
            color: #fff;
            font-weight: 600;
            font-size: 14px;
            border: none;
            border-radius: 5px;
            padding: 8px;
        }

    #cancelButton  {
        background: #fff;
        color: #333;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid #d3d3d3;
        border-radius: 5px;
        padding: 7px;
    }

    #saveButton {
        background: rgba(66, 133, 244, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.photo_file = None
        top_frame = QFrame()

        self.title_label = QLabel('Add User')
        self.title_label.setObjectName('titleLabel')

        close_button = IconButton(':/images/close_48px.png', 16, '#333', '#EA4335')
        close_button.clicked.connect(self.close)

        top_frame_layout = QHBoxLayout(top_frame)
        top_frame_layout.addWidget(self.title_label)
        top_frame_layout.addWidget(close_button)
        top_frame_layout.setStretch(0, 1)

        self.file_lineEdit = QLineEdit()
        self.file_lineEdit.setReadOnly(True)

        self.upload_button = QPushButton('Upload Photo')
        self.upload_button.setObjectName('uploadButton')
        self.upload_button.clicked.connect(self.handle_upload_photo_button)

        layout__1 = QHBoxLayout()
        layout__1.addWidget(self.file_lineEdit)
        layout__1.addWidget(self.upload_button)
        layout__1.setSpacing(5)
        layout__1.setContentsMargins(10, 10, 10, 5)

        self.first_name_form_field = FormField('First Name', 'Enter first name')
        self.last_name_form_field = FormField('Last Name', 'Enter last name')
        self.email_form_field = FormField('Email', 'example@email.com')
        self.password_form_field = FormField('Password', 'Enter password')

        layout__2 = QVBoxLayout()
        layout__2.addWidget(self.first_name_form_field)
        layout__2.addWidget(self.last_name_form_field)
        layout__2.addWidget(self.email_form_field)
        layout__2.addWidget(self.password_form_field)
        layout__2.setSpacing(0)
        layout__2.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.save_button = QPushButton('SAVE')
        self.save_button.setObjectName('saveButton')

        self.cancel_button = QPushButton('CANCEL')
        self.cancel_button.setObjectName('cancelButton')
        self.cancel_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        button_layout.setContentsMargins(9, 20, 10, 9)
        button_layout.setSpacing(20)

        content_layout = QVBoxLayout(self.contentFrame)
        content_layout.addWidget(top_frame)
        content_layout.addLayout(layout__1)
        content_layout.addLayout(layout__2)
        content_layout.addLayout(button_layout)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(0)

        self.contentFrame.setMinimumSize(300, 200)
        self.contentFrame.setStyleSheet(self.__qss__)

    def handle_upload_photo_button(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', 'C://', filter='Image file (*.jpg *.jpeg *.png)')
        self.file_lineEdit.setText(filename)


class UserDialog(Frameless):
    class Label(QLabel):
        def __init__(self, text: str):
            super().__init__(text)

    __qss__ = """
    FramelessContentFrame {
        background: rgba(255, 255, 255, 0.97);
        border-radius: 5px;
    }

    #titleLabel {
        color: #444;
        font-weight: 600;
        font-size: 24px;
    }

    #label {
        font-size: 14px;
        color: #333;
    }

    QLineEdit {
        border-radius: 5px;
        border: 2px solid #333;
        padding: 7px;
    }

    QLineEdit:focus {
        border: 2px solid rgba(66, 133, 244, 1);
    }

    #cancelButton,
    #editButton  {
        background: #fff;
        color: #333;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid #d3d3d3;
        border-radius: 5px;
        padding: 7px;
    }

    #deleteButton {
        background: rgba(234, 67, 53, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }

    #saveButton {
        background: rgba(66, 133, 244, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }

    #attendanceLabel {
        font-size: 18px;
        color: #333;
    }

    #deleteButton {
        background: rgba(234, 67, 53, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }

    #editButton {
        background: rgba(66, 133, 244, 1);
        color: #fff;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 5px;
        padding: 7px;
    }
    """

    def __init__(self, parent):
        super().__init__(parent)
        
        top_frame = QFrame()

        self.title_label = QLabel('User Name')
        self.title_label.setObjectName('titleLabel')

        close_button = IconButton(':/images/close_48px.png', 16, '#333', '#EA4335')
        close_button.clicked.connect(self.close)

        top_frame_layout = QHBoxLayout(top_frame)
        top_frame_layout.addWidget(self.title_label)
        top_frame_layout.addWidget(close_button)
        top_frame_layout.setStretch(0, 1)

        self.pic_label = QLabel()
        self.member_label = QLabel('User')
        self.email_label = QLabel('Email')

        self.edit_button = QPushButton('EDIT')
        self.remove_button = QPushButton('DELETE')

        self.edit_button.setMinimumWidth(70)
        self.remove_button.setMinimumWidth(70)

        self.edit_button.setObjectName('editButton')
        self.remove_button.setObjectName('deleteButton')

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.remove_button)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.setSpacing(10)

        layout__1 = QVBoxLayout()
        layout__1.addWidget(self.member_label)
        layout__1.addWidget(self.email_label)
        layout__1.addStretch(1)
        layout__1.addLayout(buttons_layout)
        layout__1.setSpacing(1)
        layout__1.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        layout__2 = QHBoxLayout()
        layout__2.addWidget(self.pic_label)
        layout__2.addLayout(layout__1)
        layout__2.setSpacing(20)
        layout__2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        content_layout = QVBoxLayout(self.contentFrame)
        content_layout.addWidget(top_frame)
        content_layout.addLayout(layout__2)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(0)

        self.contentFrame.setMinimumSize(300, 200)
        self.contentFrame.setStyleSheet(self.__qss__)

    def set_pic(self, pic_url):
        image_data = urllib.request.urlopen(pic_url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        pixmap = pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.pic_label.setPixmap(pixmap)
    

class SearchUI(Frameless):
    __qss__ = """
        FramelessContentFrame {
            background: rgba(255, 255, 255, 0.97);
            border-radius: 5px;
        }

        #titleLabel {
            color: #444;
            font-weight: 600;
            font-size: 24px;
        }
    """ 

    countChanged = Signal(int)

    def __init__(self, parent):
        super().__init__(parent)

        self.page = 1
        self.count = 0

        top_frame = QFrame()

        self.title_label = QLabel('Semesters')
        self.title_label.setObjectName('titleLabel')

        close_button = IconButton(':/images/close_48px.png', 16, '#333', '#EA4335')
        close_button.clicked.connect(self.close)

        top_frame_layout = QHBoxLayout(top_frame)
        top_frame_layout.addWidget(self.title_label)
        top_frame_layout.addWidget(close_button)
        top_frame_layout.setStretch(0, 1)

        self.central_widget = SlidingStackedWidget()

        content_layout = QVBoxLayout(self.contentFrame)
        content_layout.addWidget(top_frame)
        content_layout.addWidget(self.central_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setContentsMargins(5, 5, 5, 40)

        self.contentFrame.setMinimumSize(360, 200)
        self.contentFrame.setStyleSheet(self.__qss__)
