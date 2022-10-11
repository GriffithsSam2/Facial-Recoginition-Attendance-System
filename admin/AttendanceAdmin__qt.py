import datetime
from functools import partial

from PySide6.QtWidgets import QApplication, QFrame, QMessageBox
from PySide6.QtCore import QThread

from AttendanceAdmin_Resource__au import LoginUI
from AttendanceAdmin_Resource__de import AttendanceAdminUI
from AttendanceAdmin_Resource__wd import CreateEditLecturerDialog, CreateEditStudentDialog, CreateEditUserDialog, LecturerDialog, MemberButton, SearchUI, SemesterDialog, FlowLayout, SemesterButton, SlidingStackedWidget, StudentDialog, UserDialog
from AttendanceAdmin_Resource__ed import Attendance, Users, Lecturers, Semesters, Students
from AttendanceAdmin_Resource__ut import wait

from AttendanceAdmin__Subprocess import CaptureFace


class AttendanceAdmin(QApplication):
    def __init__(self):
        super().__init__()

        self.admin_data = None
        self.login_ui: LoginUI
        self.admin_ui: AttendanceAdminUI
        self.cp = CaptureFace()
        self.cp_thread = QThread()
        self.cp_thread.started.connect(self.cp.run)

    def setup(self):
        """ Set application details. """
        
        self.setApplicationDisplayName('Attendance')
        self.setApplicationName('Attendance')
        self.setApplicationVersion('0.0.1')

    def handle_login_button(self):
        response = Users.login(self.login_ui.username_line_edit.text(), self.login_ui.password_line_edit.text())
        
        if response.status_code == 200:
            self.login_ui.hide()
            
            self.admin_data = dict(response.json()['data'])

            # Initiate the Admin user interface
            self.admin_ui = AttendanceAdminUI(self.cp.terminate_)
            self.admin_ui.bottom_frame.hide()
            self.admin_ui.show()

            self.admin_ui.top_frame.logout_button.clicked.connect(self.handle_logout_button)

            self.admin_ui.side_frame.menu_button.clicked.connect(self.handle_menu_button)
            self.admin_ui.side_frame.add_semester_button.clicked.connect(self.handle_add_semester_button)
            self.admin_ui.side_frame.home_button.clicked.connect(self.handle_home_button)
            self.admin_ui.side_frame.semesters_button.clicked.connect(self.handle_semesters_button)
            self.admin_ui.side_frame.lecturers_button.clicked.connect(self.handle_lecturers_button)
            self.admin_ui.side_frame.students_button.clicked.connect(self.handle_students_button)
            self.admin_ui.side_frame.users_button.clicked.connect(self.handle_users_button)
            self.admin_ui.side_frame.logout_button.clicked.connect(self.handle_logout_button)
            self.admin_ui.side_frame.settings_button.clicked.connect(self.handle_settings_button)

            self.admin_ui.top_frame.menu_button.clicked.connect(self.handle_menu_button)
            
            self.admin_ui.central_widget.home_ui.add_semester_button.clicked.connect(self.handle_add_semester_button)
            self.admin_ui.central_widget.home_ui.semesters_button.clicked.connect(self.handle_semesters_button)
            self.admin_ui.central_widget.home_ui.lecturers_button.clicked.connect(self.handle_lecturers_button)
            self.admin_ui.central_widget.home_ui.students_button.clicked.connect(self.handle_students_button)
            self.admin_ui.central_widget.home_ui.users_button.clicked.connect(self.handle_users_button)
            self.admin_ui.central_widget.home_ui.settings_button.clicked.connect(self.handle_settings_button)

            self.admin_ui.central_widget.semesters_ui.menu_button.clicked.connect(self.handle_menu_button)
            self.admin_ui.central_widget.semesters_ui.search_button.clicked.connect(self.handle_semesters_search_button)
            self.admin_ui.central_widget.semesters_ui.add_semester_button.clicked.connect(lambda f=self.handle_add_semester_button, x=True: f(x))
            
            self.admin_ui.central_widget.lecturers_ui.add_member_button.clicked.connect(self.handle_add_lecturer_button)
            self.admin_ui.central_widget.lecturers_ui.search_button.clicked.connect(self.handle_lecturers_search_button)
            self.admin_ui.central_widget.lecturers_ui.menu_button.clicked.connect(self.handle_menu_button)

            self.admin_ui.central_widget.students_ui.add_member_button.clicked.connect(self.handle_add_student_button)
            self.admin_ui.central_widget.students_ui.menu_button.clicked.connect(self.handle_menu_button)
            self.admin_ui.central_widget.students_ui.search_button.clicked.connect(self.handle_students_search_button)

            self.admin_ui.central_widget.users_ui.add_member_button.clicked.connect(self.handle_add_user_button)
            self.admin_ui.central_widget.users_ui.menu_button.clicked.connect(self.handle_menu_button)
            self.admin_ui.central_widget.users_ui.search_button.clicked.connect(self.handle_users_search_button)
        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Error')
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText('Invalid user credentials')
            msg_box.exec_()
            
    def handle_home_button(self):
        self.admin_ui.bottom_frame.hide()
        self.hide_side_frame() if self.admin_ui.side_frame.isVisible() else self.show_side_frame()

        if self.admin_ui.central_widget.currentIndex() != 0:
            self.admin_ui.setWindowTitle('Home')
            self.admin_ui.top_frame.show()
            self.admin_ui.bottom_frame.hide()
            self.admin_ui.central_widget.slideInIdx(0)

    def hide_side_frame(self):
        self.admin_ui.side_frame.slider_widget.slideInIdx(1)
        self.admin_ui.side_frame.hide()

    def show_side_frame(self):
        self.admin_ui.side_frame.show()
        self.admin_ui.side_frame.slider_widget.slideInIdx(0)

    def handle_menu_button(self):
        self.hide_side_frame() if self.admin_ui.side_frame.isVisible() else self.show_side_frame()

    def handle_add_semester_button(self, reload_ui=False):
        self.hide_side_frame()

        dialog = SemesterDialog(self.admin_ui)
        dialog.cancel_button.hide()
        dialog.delete_button.hide()
        dialog.edit_button.hide()

        dialog.save_button.clicked.connect(lambda f=self.handle_semester_dialog_save_button, a='create', b=dialog, c=None, d=reload_ui: f(a, b, c, d))
        dialog.exec_()

    def handle_semester_dialog_save_button(self, operation, dialog: SemesterDialog, _id=None, reload_ui=False):
        dialog.close()

        member = 'Student' if dialog.students_radio_button.isChecked() else 'Lecturer'
        
        data = {
            'member': member,
            'department': dialog.department_form_field.lineEdit.text(),
            'programme': dialog.program_form_field.lineEdit.text(),
            'semester_year': dialog.semester_year_form_field.lineEdit.text(),
            'semester': dialog.semester_form_field.lineEdit.text(),
            'attendance': dialog.expected_attendance_form_field.lineEdit.text(),
            'is_current': dialog.is_current_cb.isChecked()
        }
        
        if operation == 'create':
            response = Semesters.create(data)
        else:
            data.update({'id': _id})
            response = Semesters.update(data)

        if response.status_code in (200, 201):
            if reload_ui:
                self.handle_semesters_button()

    def handle_semester_dialog_delete_button(self, _id, dialog: SemesterDialog):
        dialog.close()

        response = Semesters.remove(_id)

        if response.status_code == 204:
            self.handle_semesters_button()

    def handle_edit_semester(self, _id, dialog: SemesterDialog):
        dialog.title_label.setText('Edit Semester')
        dialog.set_fields_enabled_state(True)
        dialog.edit_button.hide()
        dialog.delete_button.hide()
        dialog.cancel_button.show()
        dialog.save_button.show()

        dialog.save_button.clicked.connect(lambda f=self.handle_semester_dialog_save_button, a='update', b=dialog, c=_id, d=True: f(a, b, c, d))

    def handle_semester_button(self, button: SemesterButton):
        dialog = SemesterDialog(self.admin_ui)
        dialog.title_label.setText('Semester')
        dialog.set_fields_enabled_state(False)

        if button.data['member'] == 'Student':
            dialog.students_radio_button.setChecked(True)
            dialog.department_form_field.hide()
            dialog.program_form_field.show()  
            dialog.program_form_field.lineEdit.setText(button.data['programme'])
        else:
            dialog.lecturers_radio_button.setChecked(True)
            dialog.department_form_field.show()
            dialog.program_form_field.hide()
            dialog.department_form_field.lineEdit.setText(button.data['department'])

        dialog.semester_year_form_field.lineEdit.setText(button.data['semester_year'])
        dialog.semester_form_field.lineEdit.setText(str(button.data['semester']))
        dialog.expected_attendance_form_field.lineEdit.setText(str(button.data['attendance']))

        dialog.is_current_cb.setChecked(button.data['is_current'])

        dialog.cancel_button.hide()
        dialog.save_button.hide()

        current_year = datetime.datetime.now().year

        if int(button.data['semester_year'].split('-')[0]) >= current_year:
            dialog.edit_button.clicked.connect(lambda f=self.handle_edit_semester, x=button.data['id'], y=dialog: f(x, y))
            dialog.delete_button.clicked.connect(lambda f=self.handle_semester_dialog_delete_button, x=button.data['id'], y=dialog: f(x, y))
        else:
            dialog.edit_button.hide()

        dialog.exec_()

    def handle_semesters_pagination(self, page):
        self.admin_ui.central_widget.semesters_ui.semester_page = page
        self.handle_semesters_button()
        self.admin_ui.central_widget.semesters_ui.central_widget.slideInIdx(page-1)

    def handle_semesters_button(self):
        self.admin_ui.bottom_frame.show()
        self.admin_ui.bottom_frame.set_pagination_callback_func(self.handle_semesters_pagination)

        if self.admin_ui.side_frame.isVisible():
            self.admin_ui.side_frame.slider_widget.slideInIdx(1)
            self.admin_ui.side_frame.hide()

        if self.admin_ui.central_widget.currentIndex() != 1:
            self.admin_ui.setWindowTitle('Semesters')
            self.admin_ui.top_frame.hide()
            self.admin_ui.central_widget.slideInIdx(1)
            self.admin_ui.bottom_frame.show()
        else:
            frames = self.admin_ui.central_widget.semesters_ui.findChildren(QFrame, 'semestersFrame')
            
            for frame in frames:
                frame.deleteLater()

        wait(100)

        try:
            self.admin_ui.central_widget.semesters_ui.central_widget.hide()
            self.admin_ui.central_widget.semesters_ui.main_layout.removeWidget(self.admin_ui.central_widget.semesters_ui.central_widget)
            self.admin_ui.central_widget.semesters_ui.central_widget = None
            self.admin_ui.central_widget.semesters_ui.central_widget = SlidingStackedWidget()

            self.admin_ui.central_widget.semesters_ui.main_layout.addWidget(self.admin_ui.central_widget.semesters_ui.central_widget)
            
            self.fetch_semesters()
        except:
            pass

    def fetch_semesters(self):
        response = Semesters.retrieve_all(self.admin_ui.central_widget.semesters_ui.semester_page)

        if response.status_code == 200:
            data = dict(response.json())

            if self.admin_ui.central_widget.semesters_ui.semester_count != data['count']:
                self.admin_ui.central_widget.semesters_ui.semester_count = data['count']
                self.admin_ui.central_widget.semesters_ui.countChanged.emit(data['count'])

            if data['count']:

                frame = QFrame()
                frame.setContentsMargins(10, 10, 10, 0)
                frame.setObjectName('semestersFrame')
                
                layout = FlowLayout(frame)
                layout.setSpacing(30)

                self.admin_ui.central_widget.semesters_ui.central_widget.addWidget(frame)
                
                for semester in data['results']:
                    semester_button = SemesterButton(semester)
                    semester_button.clicked.connect(lambda f=self.handle_semester_button, x=semester_button: f(x))
                    layout.addWidget(semester_button)

                    wait(100)

    def handle_lecturers_pagination(self, page):
        self.admin_ui.central_widget.lecturers_ui.members_page = page
        self.handle_lecturers_button()
        self.admin_ui.central_widget.lecturers_ui.central_widget.slideInIdx(page-1)

    def handle_lecturers_button(self):
        self.admin_ui.bottom_frame.show()
        self.admin_ui.bottom_frame.set_pagination_callback_func(self.handle_lecturers_pagination)

        if self.admin_ui.side_frame.isVisible():
            self.admin_ui.side_frame.slider_widget.slideInIdx(1)
            self.admin_ui.side_frame.hide()

        if self.admin_ui.central_widget.currentIndex() != 2:
            self.admin_ui.setWindowTitle('Lecturers')
            self.admin_ui.central_widget.lecturers_ui.search_field.setPlaceholderText('Search Lecturers')
            self.admin_ui.top_frame.hide()
            self.admin_ui.central_widget.slideInIdx(2)
        else:
            frames = self.admin_ui.central_widget.lecturers_ui.findChildren(QFrame, 'lecturersFrame')
            
            for frame in frames:
                frame.deleteLater()

        wait(100)

        try:
            self.admin_ui.central_widget.lecturers_ui.central_widget.hide()
            self.admin_ui.central_widget.lecturers_ui.main_layout.removeWidget(self.admin_ui.central_widget.lecturers_ui.central_widget)
            self.admin_ui.central_widget.lecturers_ui.central_widget = None
            self.admin_ui.central_widget.lecturers_ui.central_widget = SlidingStackedWidget()

            self.admin_ui.central_widget.lecturers_ui.main_layout.addWidget(self.admin_ui.central_widget.lecturers_ui.central_widget)
            
            self.fetch_lecturers()
        except Exception as ex:
            print(ex)

    def fetch_lecturers(self):
        response = Lecturers.retrieve_all(self.admin_ui.central_widget.lecturers_ui.members_page)
        
        if response.status_code == 200:
            data = dict(response.json())

            if self.admin_ui.central_widget.lecturers_ui.members_count != data['count']:
                self.admin_ui.central_widget.lecturers_ui.members_count = data['count']
                self.admin_ui.central_widget.lecturers_ui.countChanged.emit(data['count'])

            if data['count']:
                frame = QFrame()
                frame.setContentsMargins(20, 10, 10, 0)
                frame.setObjectName('lecturersFrame')
                
                layout = FlowLayout(frame)
                layout.setSpacing(20)

                self.admin_ui.central_widget.lecturers_ui.central_widget.addWidget(frame)
                
                for lecturer in data['results']:
                    attendance_response = dict(Attendance.retrieve_lecturer(lecturer['id']).json())
                    
                    lecturer.update({'attendance': f"<small>{attendance_response['attendance']}</small>/<b>60</b>"})
                    lecturer_button = MemberButton(lecturer)
                    lecturer_button.clicked.connect(lambda f=self.handle_lecturer_button, x=lecturer: f(x))
                    layout.addWidget(lecturer_button)
                    wait(100)

    def handle_edit_lecturer_button(self, data: dict[str], dialog: LecturerDialog):
        dialog.close()
        edit_dialog = CreateEditLecturerDialog(self.admin_ui)
        edit_dialog.title_label.setText('Edit Lecturer')
        edit_dialog.first_name_form_field.lineEdit.setText(data['first_name'])
        edit_dialog.last_name_form_field.lineEdit.setText(data['last_name'])
        edit_dialog.dob_form_field.lineEdit.setText(data['dob'])
        edit_dialog.department_form_field.lineEdit.setText(data['department'])
        edit_dialog.save_button.clicked.connect(lambda f=self.handle_lecturer_save_button, x='update', y=edit_dialog, z=data['id']: f(x, y, z))
        edit_dialog.exec_()

    def handle_lecturer_save_button(self, operation, dialog: CreateEditLecturerDialog, _id=None):
        data = {
            'first_name': dialog.first_name_form_field.lineEdit.text(),
            'last_name': dialog.last_name_form_field.lineEdit.text(),
            'department': dialog.department_form_field.lineEdit.text(),
            'dob': dialog.dob_form_field.lineEdit.text()
        }
        data.update({
            'photo': dialog.file_lineEdit.text()
        })
        dialog.close()
        if operation == 'create':
            response = Lecturers.create(data)
        else:
            data.update({'id': _id})
            response = Lecturers.update(data)
        
        if response.status_code in (200, 201):
            self.handle_lecturers_button()

    def handle_add_lecturer_button(self):
        self.hide_side_frame()

        dialog = CreateEditLecturerDialog(self.admin_ui)
        dialog.save_button.clicked.connect(lambda f=self.handle_lecturer_save_button, x='create', y=dialog: f(x, y))
        dialog.exec_()

    def handle_lecturer_button(self, data):
        dialog = LecturerDialog(self.admin_ui)
        dialog.title_label.setText(f"{data['first_name']} {data['last_name']}")
        dialog.department_label.setText(data['department'])
        dialog.attendance_label.setText(data['attendance'])
        dialog.set_pic(data['photo'])
        dialog.remove_button.clicked.connect(lambda f=self.handle_lecturer_dialog_delete_button, x=data['id'], y=dialog: f(x, y))
        dialog.edit_button.clicked.connect(lambda f=self.handle_edit_lecturer_button, x=data, y=dialog: f(x, y))
        dialog.exec_()

    def handle_lecturer_dialog_delete_button(self, _id, dialog: LecturerDialog):
        dialog.close()

        response = Lecturers.remove(_id)
       
        if response.status_code == 204:
            self.handle_users_button()

    def handle_students_pagination(self, page):
        self.admin_ui.central_widget.students_ui.members_page = page
        self.handle_students_button()
        self.admin_ui.central_widget.students_ui.central_widget.slideInIdx(page-1)

    def handle_students_button(self):
        self.admin_ui.bottom_frame.show()
        self.admin_ui.bottom_frame.set_pagination_callback_func(self.handle_students_pagination)

        if self.admin_ui.side_frame.isVisible():
            self.admin_ui.side_frame.slider_widget.slideInIdx(1)
            self.admin_ui.side_frame.hide()

        if self.admin_ui.central_widget.currentIndex() != 3:
            self.admin_ui.setWindowTitle('Students')
            self.admin_ui.top_frame.hide()
            self.admin_ui.central_widget.slideInIdx(3)
        else:
            frames = self.admin_ui.central_widget.students_ui.findChildren(QFrame, 'studentsFrame')
            
            for frame in frames:
                frame.deleteLater()

        wait(100)

        try:
            self.admin_ui.central_widget.students_ui.central_widget.hide()
            self.admin_ui.central_widget.students_ui.main_layout.removeWidget(self.admin_ui.central_widget.students_ui.central_widget)
            self.admin_ui.central_widget.students_ui.central_widget = None
            self.admin_ui.central_widget.students_ui.central_widget = SlidingStackedWidget()

            self.admin_ui.central_widget.students_ui.main_layout.addWidget(self.admin_ui.central_widget.students_ui.central_widget)
            
            self.fetch_students()
        except Exception as ex:
            print(ex)

    def fetch_students(self):
        response = Students.retrieve_all(self.admin_ui.central_widget.students_ui.members_page)
        
        if response.status_code == 200:
            data = dict(response.json())

            if self.admin_ui.central_widget.students_ui.members_count != data['count']:
                self.admin_ui.central_widget.students_ui.members_count = data['count']
                self.admin_ui.central_widget.students_ui.countChanged.emit(data['count'])

            if data['count']:
                frame = QFrame()
                frame.setContentsMargins(20, 10, 10, 0)
                frame.setObjectName('studentsFrame')
                
                layout = FlowLayout(frame)
                layout.setSpacing(20)

                self.admin_ui.central_widget.students_ui.central_widget.addWidget(frame)
                
                for student in data['results']:
                    attendance_response = dict(Attendance.retrieve_student(student['id']).json())
                    print(attendance_response['attendance'])
                    student.update({'attendance': f"<small>{attendance_response['attendance']}</small>/<b>60</b>"})
                    student_button = MemberButton(student)
                    student_button.clicked.connect(lambda f=self.handle_student_button, x=student: f(x))
                    layout.addWidget(student_button)
                    wait(100)

    def handle_edit_student_button(self, data: dict[str], dialog: StudentDialog):
        dialog.close()
        edit_dialog = CreateEditStudentDialog(self.admin_ui)
        edit_dialog.title_label.setText('Edit Student')
        edit_dialog.first_name_form_field.lineEdit.setText(data['first_name'])
        edit_dialog.last_name_form_field.lineEdit.setText(data['last_name'])
        edit_dialog.student_id_form_field.lineEdit.setText(data['student_id'])
        edit_dialog.dob_form_field.lineEdit.setText(data['dob'])
        edit_dialog.programme_form_field.lineEdit.setText(data['programme'])
        edit_dialog.entry_date_form_field.lineEdit.setText(data['entry_date'])
        edit_dialog.save_button.clicked.connect(lambda f=self.handle_student_save_button, x='update', y=edit_dialog, z=data['id']: f(x, y, z))
        edit_dialog.exec_()

    def handle_student_save_button(self, operation, dialog: CreateEditStudentDialog, _id=None):
        data = {
            'first_name': dialog.first_name_form_field.lineEdit.text(),
            'last_name': dialog.last_name_form_field.lineEdit.text(),
            'student_id': dialog.student_id_form_field.lineEdit.text(),
            'dob': dialog.dob_form_field.lineEdit.text(),
            'programme': dialog.programme_form_field.lineEdit.text(),
            'entry_date': dialog.entry_date_form_field.lineEdit.text()
        }
        data.update({
            'photo': dialog.file_lineEdit.text()
        })
        dialog.close()
        if operation == 'create':
            response = Students.create(data)
        else:
            data.update({'id': _id})
            response = Students.update(data)
        
        if response.status_code in (200, 201):
            self.handle_students_button()

    def handle_add_student_button(self):
        dialog = CreateEditStudentDialog(self.admin_ui)
        dialog.save_button.clicked.connect(lambda f=self.handle_student_save_button, x='create', y=dialog: f(x, y))
        dialog.exec_()

    def handle_student_button(self, data):
        dialog = StudentDialog(self.admin_ui)
        dialog.title_label.setText(f"{data['first_name']} {data['last_name']}")
        dialog.student_id_label.setText(data['student_id'])
        dialog.programme_label.setText(data['programme'])
        dialog.entry_date_label.setText(data['entry_date'])
        dialog.attendance_label.setText(data['attendance'])
        dialog.set_pic(data['photo'])
        dialog.edit_button.clicked.connect(lambda f=self.handle_edit_student_button, x=data, y=dialog: f(x, y))
        dialog.remove_button.clicked.connect(lambda f=self.handle_student_dialog_delete_button, x=data['id'], y=dialog: f(x, y))
        dialog.exec_()

    def handle_student_dialog_delete_button(self, _id, dialog: StudentDialog):
        dialog.close()

        response = Students.remove(_id)
        if response.status_code == 204:
            self.handle_students_button()


    def handle_users_pagination(self, page):
        self.admin_ui.central_widget.users_ui.members_page = page
        self.handle_users_button()
        self.admin_ui.central_widget.users_ui.central_widget.slideInIdx(page-1)

    def handle_users_button(self):
        self.admin_ui.central_widget.users_ui.search_field.hide()
        self.admin_ui.central_widget.users_ui.search_button.hide()
        self.admin_ui.bottom_frame.show()
        self.admin_ui.bottom_frame.set_pagination_callback_func(self.handle_users_pagination)

        if self.admin_ui.side_frame.isVisible():
            self.admin_ui.side_frame.slider_widget.slideInIdx(1)
            self.admin_ui.side_frame.hide()

        if self.admin_ui.central_widget.currentIndex() != 4:
            self.admin_ui.setWindowTitle('Users')
            self.admin_ui.central_widget.users_ui.search_field.setPlaceholderText('Search user')
            self.admin_ui.top_frame.hide()
            self.admin_ui.central_widget.slideInIdx(4)
        else:
            frames = self.admin_ui.central_widget.users_ui.findChildren(QFrame, 'usersFrame')
            
            for frame in frames:
                frame.deleteLater()

        wait(100)

        self.admin_ui.central_widget.users_ui.central_widget.hide()
        self.admin_ui.central_widget.users_ui.main_layout.removeWidget(self.admin_ui.central_widget.users_ui.central_widget)
        self.admin_ui.central_widget.users_ui.central_widget = None
        self.admin_ui.central_widget.users_ui.central_widget = SlidingStackedWidget()

        self.admin_ui.central_widget.users_ui.main_layout.addWidget(self.admin_ui.central_widget.users_ui.central_widget)
            
        self.fetch_users()

    def fetch_users(self):
        response = Users.retrieve_all(self.admin_ui.central_widget.users_ui.members_page)
        
        if response.status_code == 200:
            data = dict(response.json())

            if self.admin_ui.central_widget.users_ui.members_count != data['count']:
                self.admin_ui.central_widget.users_ui.members_count = data['count']
                self.admin_ui.central_widget.users_ui.countChanged.emit(data['count'])

            if data['count']:
                frame = QFrame()
                frame.setContentsMargins(20, 10, 10, 0)
                frame.setObjectName('usersFrame')
                
                layout = FlowLayout(frame)
                layout.setSpacing(20)

                self.admin_ui.central_widget.users_ui.central_widget.addWidget(frame)
                
                for user in data['results']:
                    if user['id'] != self.admin_data['id']:
                        user_button = MemberButton(user)
                        user_button.clicked.connect(lambda f=self.handle_user_button, x=user: f(x))
                        layout.addWidget(user_button)
                    else:
                        self.admin_ui.central_widget.users_ui.members_count -= 1
                        self.admin_ui.central_widget.users_ui.countChanged.emit(self.admin_ui.central_widget.users_ui.members_count)
                    
                    wait(100)

    def handle_edit_user_button(self, data: dict[str], dialog: UserDialog):
        dialog.close()
        edit_dialog = CreateEditUserDialog(self.admin_ui)
        edit_dialog.title_label.setText('Edit User')
        edit_dialog.first_name_form_field.lineEdit.setText(data['first_name'])
        edit_dialog.last_name_form_field.lineEdit.setText(data['last_name'])
        edit_dialog.save_button.clicked.connect(lambda f=self.handle_user_save_button, x='update', y=edit_dialog, z=data['id']: f(x, y, z))
        edit_dialog.exec_()

    def handle_user_save_button(self, operation, dialog: CreateEditUserDialog, _id=None):
        data = {
            'first_name': dialog.first_name_form_field.lineEdit.text(),
            'last_name': dialog.last_name_form_field.lineEdit.text(),
            'email': dialog.email_form_field.lineEdit.text(),
            'password': dialog.password_form_field.lineEdit.text()
        }
        
        data.update({
            'photo': dialog.file_lineEdit.text()
        })

        dialog.close()

        if operation == 'create':
            response = Users.register(data)
        else:
            _id = _id if _id else self.admin_data['id']

            data.update({'id': _id})
            response = Users.update(data)

            if data['password']:
                Users.update_password(_id, data['password'])
        
        if response.status_code in (200, 201):
            if _id == self.admin_data['id']:
                self.admin_data = dict(response.json())

            self.handle_users_button()

    def handle_add_user_button(self):
        dialog = CreateEditUserDialog(self.admin_ui)
        dialog.save_button.clicked.connect(lambda f=self.handle_user_save_button, x='create', y=dialog: f(x, y))
        dialog.exec_()

    def handle_user_button(self, data):
        dialog = UserDialog(self.admin_ui)
        dialog.title_label.setText(f"{data['first_name']} {data['last_name']}")
        dialog.email_label.setText(data['email'])
        dialog.set_pic(data['photo'])
        dialog.edit_button.clicked.connect(lambda f=self.handle_edit_user_button, x=data, y=dialog: f(x, y))
        dialog.remove_button.clicked.connect(lambda f=self.handle_user_dialog_delete_button, x=data['id'], y=dialog: f(x, y))
        dialog.exec_()

    def handle_user_dialog_delete_button(self, _id, dialog: UserDialog):
        dialog.close()

        response = Users.remove(_id)
       
        if response.status_code == 204:
            self.handle_users_button()

    def handle_settings_button(self):
        self.hide_side_frame()

        dialog = CreateEditUserDialog(self.admin_ui)
        dialog.title_label.setText('Settings')
        dialog.first_name_form_field.lineEdit.setText(self.admin_data['first_name'])
        dialog.last_name_form_field.lineEdit.setText(self.admin_data['last_name'])
        dialog.email_form_field.lineEdit.setText(self.admin_data['email'])
        dialog.save_button.clicked.connect(lambda f=self.handle_user_save_button, x='update', y=dialog: f(x, y))
        dialog.exec_()

    def handle_semesters_search_button(self):
        semester_year = self.admin_ui.central_widget.semesters_ui.search_field.text()

        try:
            response = Semesters.search(semester_year)
            
            if response.status_code == 200:
                data = dict(response.json())

                if data['count']:
                    search_ui = SearchUI(self.admin_ui)

                    frame = QFrame()
                    frame.setContentsMargins(10, 10, 10, 0)
                    frame.setObjectName('searchFrame')
                    
                    layout = FlowLayout(frame)
                    layout.setSpacing(20)

                    search_ui.central_widget.addWidget(frame)
                    
                    for semester in data['results']:
                        semester_button = SemesterButton(semester)
                        semester_button.clicked.connect(lambda f=self.handle_semester_button, x=semester_button: f(x))
                        layout.addWidget(semester_button)

                        wait(100)

                    search_ui.exec_()
        except:
            pass
        
    def handle_lecturers_search_button(self):
        lecturer_search = self.admin_ui.central_widget.lecturers_ui.search_field.text()

        try:
            response = Lecturers.search(lecturer_search)
            
            if response.status_code == 200:
                data = dict(response.json())

                if data['count']:
                    search_ui = SearchUI(self.admin_ui)
                    search_ui.title_label.setText('Lecturers')

                    frame = QFrame()
                    frame.setContentsMargins(10, 10, 10, 0)
                    frame.setObjectName('lecturerFrame')
                    
                    layout = FlowLayout(frame)
                    layout.setSpacing(20)

                    search_ui.central_widget.addWidget(frame)
                    
                    for lecturer in data['results']:
                        attendance_response = dict(Attendance.retrieve_lecturer(lecturer['id']).json())
                        print(attendance_response)
                        lecturer.update({'attendance': f"<small>{attendance_response['attendance']}</small>/<b>60</b>"})
                        lecturer_button = MemberButton(lecturer)
                        lecturer_button.clicked.connect(partial(self.handle_lecturer_button(lecturer)))
                        layout.addWidget(lecturer_button)
                        wait(100)

                    search_ui.exec_()
        except:
            pass

    def handle_students_search_button(self):
        student_search = self.admin_ui.central_widget.students_ui.search_field.text()

        try:
            response = Students.search(student_search)
            
            if response.status_code == 200:
                data = dict(response.json())

                if data['count']:
                    search_ui = SearchUI(self.admin_ui)
                    search_ui.title_label.setText('Students')

                    frame = QFrame()
                    frame.setContentsMargins(10, 10, 10, 0)
                    frame.setObjectName('studentFrame')
                    
                    layout = FlowLayout(frame)
                    layout.setSpacing(20)

                    search_ui.central_widget.addWidget(frame)
                    
                    for student in data['results']:
                        attendance_response = dict(Attendance.retrieve_student(student['id']).json())
                        student.update({'attendance': f"<small>{attendance_response['attendance']}</small>/<b>60</b>"})
                        button = MemberButton(student)
                        button.clicked.connect(partial(self.handle_student_button(student)))
                        layout.addWidget(button)
                        wait(100)

                    search_ui.exec_()
        except:
            pass

    def handle_users_search_button(self):
        search = self.admin_ui.central_widget.users_ui.search_field.text()

        try:
            response = Users.search(search)
            
            if response.status_code == 200:
                data = dict(response.json())

                if data['count']:
                    search_ui = SearchUI(self.admin_ui)
                    search_ui.title_label.setText('Users')

                    frame = QFrame()
                    frame.setContentsMargins(10, 10, 10, 0)
                    frame.setObjectName('userFrame')
                    
                    layout = FlowLayout(frame)
                    layout.setSpacing(20)

                    search_ui.central_widget.addWidget(frame)
                    
                    for user in data['results']:
                        if user['id'] != self.admin_data['id']:
                            user_button = MemberButton(user)
                            user_button.clicked.connect(partial(self.handle_user_button(user)))
                            layout.addWidget(user_button)
                        wait(100)
        except:
            pass

    def handle_logout_button(self):
        self.login_ui.show()
        self.admin_ui = None

    def execute__(self):
        self.setup()

        self.login_ui = LoginUI()
        self.login_ui.show()
        self.login_ui.login_button.clicked.connect(self.handle_login_button)

        self.cp_thread.start()
        return self.exec()
