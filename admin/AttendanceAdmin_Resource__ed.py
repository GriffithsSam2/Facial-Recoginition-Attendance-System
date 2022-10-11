import requests

from AttendanceAdmin_Resource__ut import verify_face


__BASE_URL__ = 'http://127.0.0.1:8001/api'


class Users:

    @staticmethod
    def login(email, password):
        url = f"{__BASE_URL__}/accounts/login/"

        payload = {
            'email': email,
            'password': password
        }
        files=[]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files=files) 
        return response

    @staticmethod
    def search(string: str):
        first_name = string.split(' ')[0]
        last_name = string.split(' ')[1]

        url = f'{__BASE_URL__}/accounts/search/{first_name}/{last_name}/'

        payload={}
        headers = {}

        return requests.request("GET", url, headers=headers, data=payload)

    @staticmethod
    def register(data):
        url = f"{__BASE_URL__}/accounts/register/"

        payload={
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': data['password']
        }

        files=[]

        if data['photo']:
            files.append(('photo', (data['photo'].split('/')[-1], open(data['photo'],'rb'), data['photo'].split('/')[-1].split('.')[-1])))

        headers = {}

        return requests.request("POST", url, headers=headers, data=payload, files=files)


    @staticmethod
    def update(data):
        url = f"{__BASE_URL__}/accounts/users/{data['id']}/"

        payload={
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email']
        }

        files=[]

        if data['photo']:
            files.append(('photo', (data['photo'].split('/')[-1], open(data['photo'],'rb'), data['photo'].split('/')[-1].split('.')[-1])))

        headers = {}

        return requests.request("PATCH", url, headers=headers, data=payload, files=files)

    @staticmethod
    def retrieve_all(page) -> requests.Response:
        url = f'{__BASE_URL__}/accounts/users/?page={page}'

        payload={}
        headers = {}

        return requests.request("GET", url, headers=headers, data=payload)

    @staticmethod
    def remove(_id):
        url = f'{__BASE_URL__}/accounts/users/{_id}/'

        payload={}
        headers = {}

        return requests.request("DELETE", url, headers=headers, data=payload)

    @staticmethod
    def update_password(id_, password):
        url = f"{__BASE_URL__}/accounts/update/password/{id_}/"

        payload={
            'password': password
        }

        files=[]
        headers = {}

        return requests.request("PATCH", url, headers=headers, data=payload, files=files)


class Semesters:
    @staticmethod
    def create(data):
        url = f"{__BASE_URL__}/semesters/"

        payload={
            'member': data['member'],
            'department': data['department'],
            'programme': data['programme'],
            'semester_year': data['semester_year'],
            'semester': data['semester'],
            'attendance': data['attendance'],
            'is_current': data['is_current']
        }

        files=[]
        headers = {}

        return requests.request("POST", url, headers=headers, data=payload, files=files)

    @staticmethod
    def retrieve_all(page) -> requests.Response:
        url = f'{__BASE_URL__}/semesters/?page={page}'

        payload={}
        headers = {}

        return requests.request("GET", url, headers=headers, data=payload)

    @staticmethod
    def update(data):
        url = f"{__BASE_URL__}/semesters/{data['id']}/"

        payload={
            'member': data['member'],
            'department': data['department'],
            'programme': data['programme'],
            'semester_year': data['semester_year'],
            'semester': data['semester'],
            'attendance': data['attendance'],
            'is_current': data['is_current']
        }

        files=[]
        headers = {}

        return requests.request("PATCH", url, headers=headers, data=payload, files=files)
   
    @staticmethod
    def search(string: str):
        searched = string.split(':')
        semester_year = searched[0]
        other = searched[1]

        url = f'{__BASE_URL__}/semesters/search/{semester_year}/{other}/'

        payload={}
        headers = {}

        return requests.request("GET", url, headers=headers, data=payload)


    @staticmethod
    def remove(_id):
        url = f'{__BASE_URL__}/semesters/{_id}/'

        payload={}
        headers = {}

        return requests.request("DELETE", url, headers=headers, data=payload)


class Lecturers:

    @staticmethod
    def create(data: dict[str]):
        url = f"{__BASE_URL__}/lecturers/"

        payload={
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "dob": data['dob'],
            "department": data['department']
        }

        files=[
            ('photo', (data['photo'].split('/')[-1], open(data['photo'],'rb'), data['photo'].split('/')[-1].split('.')[-1]))
        ]
        headers = {}

        return requests.request("POST", url, headers=headers, data=payload, files=files)

    @staticmethod
    def search(string: str):
        searched = string.split(':')
        fullname = searched[0]
        department = searched[1]

        first_name = fullname.split(' ')[0]
        last_name = fullname.split(' ')[1]

        url = f'{__BASE_URL__}/lecturers/search/{first_name}/{last_name}/{department}/'

        payload={}
        headers = {}

        return requests.request("GET", url, headers=headers, data=payload)

    @staticmethod
    def update(data: dict[str]):
        url = f"{__BASE_URL__}/lecturers/{data['id']}/"

        payload={
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "dob": data['dob'],
            "department": data['department']
        }

        files=[]

        if data['photo']:
            files.append(('photo', (data['photo'].split('/')[-1], open(data['photo'],'rb'), data['photo'].split('/')[-1].split('.')[-1])))

        headers = {}

        return requests.request("PATCH", url, headers=headers, data=payload, files=files)

    @staticmethod
    def retrieve_all(page):
        url = f'{__BASE_URL__}/lecturers/?page={page}'

        payload={}
        headers = {}

        return requests.request("GET", url, headers=headers, data=payload)

    @staticmethod
    def retrieve_abs_all():
        url = f'{__BASE_URL__}/lecturers/all/'

        payload={}
        headers = {}

        return requests.request("GET", url, headers=headers, data=payload)

    @staticmethod
    def remove(_id):
        url = f'{__BASE_URL__}/lecturers/{_id}/'

        payload={}
        headers = {}

        return requests.request("DELETE", url, headers=headers, data=payload)

class Students:

    @staticmethod
    def create(data: dict[str]):
        url = f"{__BASE_URL__}/students/"

        payload={
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "dob": data['dob'],
            "programme": data['programme'],
            "student_id": data['student_id'],
            "entry_date": data['entry_date']
        }

        files=[
            ('photo', (data['photo'].split('/')[-1], open(data['photo'],'rb'), data['photo'].split('/')[-1].split('.')[-1]))
        ]
        headers = {}

        return requests.request("POST", url, headers=headers, data=payload, files=files)

    @staticmethod
    def search(string: str):
        searched = string.split(':')
        fullname = searched[0]
        programme = searched[1]

        first_name = fullname.split(' ')[0]
        last_name = fullname.split(' ')[1]

        url = f'{__BASE_URL__}/students/search/{first_name}/{last_name}/{programme}/'

        payload={}
        headers = {}

        return requests.request("GET", url, headers=headers, data=payload)

    @staticmethod
    def update(data: dict[str]):
        url = f"{__BASE_URL__}/students/{data['id']}/"

        payload={
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "dob": data['dob'],
            "programme": data['programme'],
            "student_id": data['student_id'],
            "entry_date": data['entry_date']
        }

        files=[]

        if data['photo']:
            files.append(('photo', (data['photo'].split('/')[-1], open(data['photo'],'rb'), data['photo'].split('/')[-1].split('.')[-1])))

        headers = {}

        return requests.request("PATCH", url, headers=headers, data=payload, files=files)


    @staticmethod
    def retrieve_all(page):
        url = f'{__BASE_URL__}/students/?page={page}'

        payload={}
        headers = {}

        return requests.request("GET", url, headers=headers, data=payload)
    
    @staticmethod
    def retrieve_abs_all():
        url = f'{__BASE_URL__}/students/all/'

        payload={}
        headers = {}

        return requests.request("GET", url, headers=headers, data=payload)
    
    @staticmethod
    def remove(_id):
        url = f'{__BASE_URL__}/students/{_id}/'

        payload={}
        headers = {}

        return requests.request("DELETE", url, headers=headers, data=payload) @staticmethod
    def remove(_id):
        url = f'{__BASE_URL__}/students/{_id}/'

        payload={}
        headers = {}

        return requests.request("DELETE", url, headers=headers, data=payload)


class Attendance:

    @staticmethod
    def record():
        students = list(Students.retrieve_abs_all().json())
        
        for student in students:
            found = verify_face(student['photo'])

            if found:
                url = f"{__BASE_URL__}/attendances/record/student/{student['id']}"

                payload={}
                files=[]
                headers = {}

                requests.request("POST", url, headers=headers, data=payload, files=files)
                return True

        lecturers = list(Lecturers.retrieve_abs_all().json())

        for lecturer in lecturers:
            found = verify_face(lecturer['photo'])

            if found:
                url = f"{__BASE_URL__}/attendances/record/student/{lecturer['id']}"

                payload={}
                files=[]
                headers = {}

                requests.request("POST", url, headers=headers, data=payload, files=files)
                return True

        return False

    @staticmethod
    def retrieve_lecturer(_id):
        url = f"{__BASE_URL__}/attendances/retrieve/lecturer/{_id}/"

        payload={}
        files={}
        headers = {}

        return requests.request("GET", url, headers=headers, data=payload, files=files)

    @staticmethod
    def retrieve_student(_id):
        url = f"{__BASE_URL__}/attendances/retrieve/student/{_id}/"

        payload={}
        files={}
        headers = {}

        return requests.request("GET", url, headers=headers, data=payload, files=files)
