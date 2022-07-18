import datetime
import sqlalchemy.exc
from sqlalchemy import func
from . import db


class Marker(db.Model):
    __tablename__ = 'marker'
    id = db.Column(db.Integer, primary_key=True)
    time_in = db.Column(db.DateTime)
    reason_in = db.Column(db.Text)
    time_out = db.Column(db.DateTime)
    reason_out = db.Column(db.Text)
    staff_id = db.Column(db.Integer(), db.ForeignKey('staff.id'), nullable=False)

    def __init__(self, staff_id=None, reason_in=None, time_in=None, time_out=None, reason_out=None):
        self.time_in = time_in
        self.reason_in = reason_in
        self.time_out = time_out
        self.reason_out = reason_out
        self.staff_id = staff_id

    @classmethod
    def marker_in(cls, staff_id=None, reason_in=None):
        """
        Метод создания маркера входа
        """

        marker = cls.query.filter(cls.staff_id == staff_id, cls.time_out == None).first()

        if marker:
            return 'still here'

        marker = cls(staff_id, reason_in, time_in=datetime.datetime.now().replace(microsecond=0).replace(second=0))

        try:
            db.session.add(marker)
            db.session.commit()
            db.session.remove()
            return 'ok'
        except sqlalchemy.exc.IntegrityError as error:
            db.session.rollback()
            db.session.remove()

            if 'UNIQUE' in str(error):
                return 'not unique'
            if 'NOT NULL' in str(error):
                return None
            return f'{error}'

    @classmethod
    def marker_out(cls, staff_id=None, reason_out=None):
        """
        Метод создания маркера выхода
        """

        if not staff_id:
            return 'access denied'

        marker = cls.query.filter(cls.staff_id == staff_id, cls.time_out == None).first()

        if not marker:
            return 'did not come yet'

        marker.time_out = datetime.datetime.now().replace(microsecond=0).replace(second=0)
        marker.reason_out = reason_out

        try:
            db.session.commit()
            db.session.remove()
            return 'ok'
        except sqlalchemy.exc.IntegrityError as error:
            db.session.rollback()
            db.session.remove()

            if 'UNIQUE' in str(error):
                return 'not unique'
            if 'NOT NULL' in str(error):
                return None
            return f'{error}'

    @classmethod
    def edit_marker(cls, reason_in=None, reason_out=None, time_in=None, time_out=None, marker_id=None):
        """
        Метод изменения маркера
        """
        marker = cls.query.filter(cls.id == marker_id).first()

        if not marker:
            return None

        if time_in:
            try:
                datetime_time_in = datetime.datetime.strptime(f'{time_in}', '%Y-%m-%d %H:%M')
                marker.time_in = datetime_time_in
            except ValueError:
                marker.time_in = None
                return None

        if time_out:
            try:
                datetime_time_out = datetime.datetime.strptime(f'{time_out}', '%Y-%m-%d %H:%M')
                marker.time_out = datetime_time_out
            except ValueError:
                marker.time_out = None
                return None

        marker.reason_in = reason_in
        marker.reason_out = reason_out

        try:
            db.session.commit()
            db.session.remove()
            return 'ok'
        except sqlalchemy.exc.IntegrityError as error:
            db.session.rollback()
            db.session.remove()

            if 'UNIQUE' in str(error):
                return 'not unique'
            if 'NOT NULL' in str(error):
                return None
            return f'{error}'

    @classmethod
    def create_marker_by_admin(cls, reason_in=None, reason_out=None, time_in=None, time_out=None, staff_id=None):
        """
        Метод создания маркера админом
        """
        datetime_time_out = None
        datetime_time_in = None

        if time_in:
            try:
                datetime_time_in = datetime.datetime.strptime(f'{time_in}', '%Y-%m-%d %H:%M')
            except ValueError:
                return 'error date'

        if time_out:
            try:
                datetime_time_out = datetime.datetime.strptime(f'{time_out}', '%Y-%m-%d %H:%M')
            except ValueError:
                return 'error date'

        marker = cls(staff_id=staff_id, reason_in=reason_in, reason_out=reason_out,
                     time_in=datetime_time_in, time_out=datetime_time_out)

        try:
            db.session.add(marker)
            db.session.commit()
            db.session.remove()
            return 'ok'
        except sqlalchemy.exc.IntegrityError as error:
            db.session.rollback()
            db.session.remove()

            if 'UNIQUE' in str(error):
                return 'not unique'
            if 'NOT NULL' in str(error):
                return None
            return f'{error}'

    @classmethod
    def today_markers(cls):
        """
        Метод отдает сегодняшние маркеры
        """
        markers = cls.query.filter(func.DATE(cls.time_in) == datetime.date.today()).all()

        if not markers:
            return None

        data_markers = []
        for marker in markers:
            data_markers.append({
                'time_in': marker.time_in,
                'time_out': marker.time_out,
                'reason_in': marker.reason_in,
                'reason_out': marker.reason_out,
                'staff_id': marker.staff_id
            })

        return data_markers

    def __repr__(self):
        return f'<Marker {self.staff_id!r} {self.time_in!r} - {self.time_out!r}>'


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    staff = db.relationship('Staff', backref='department')

    def __init__(self, title=None):
        self.title = title

    @classmethod
    def create_department(cls, title=None):
        """
        Метод создания отдела
        """
        department = cls(title=title)
        try:
            db.session.add(department)
            db.session.commit()
            db.session.remove()
            return 'ok'
        except sqlalchemy.exc.IntegrityError as error:
            db.session.rollback()
            db.session.remove()

            if 'UNIQUE' in str(error):
                return 'not unique'
            if 'NOT NULL' in str(error):
                return None
            return f'{error}'

    @classmethod
    def edit_department(cls, department_id=None, title=None):
        """
        Метод создания отдела
        """

        department = cls.query.filter(cls.id == department_id).first()
        department.title = title

        try:
            db.session.commit()
            db.session.remove()
            return 'ok'
        except sqlalchemy.exc.IntegrityError as error:
            db.session.rollback()
            db.session.remove()

            if 'UNIQUE' in str(error):
                return 'not unique'
            if 'NOT NULL' in str(error):
                return None
            return f'{error}'

    def __repr__(self):
        return f'<Department {self.title!r} {self.staff_id!r}>'


class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(50), nullable=True)
    appointment = db.Column(db.String(50), nullable=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.Boolean, nullable=False)
    phone = db.Column(db.String(12), unique=True, nullable=True)
    email = db.Column(db.String(50), nullable=True)
    at_work = db.Column(db.Time, nullable=True)
    from_work = db.Column(db.Time, nullable=True)
    password = db.Column(db.String(16), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    marker = db.relationship('Marker', backref='staff')
    department_id = db.Column(db.Integer(), db.ForeignKey('department.id'))

    def __init__(self, photo=None, appointment=None, firstname=None, lastname=None, middle_name=None, gender=None,
                 phone=None, email=None, at_work=None, from_work=None, password=None, active=True, admin=False,
                 department_id=None):
        self.phone = photo
        self.appointment = appointment
        self.firstname = firstname
        self.lastname = lastname
        self.middle_name = middle_name
        self.phone = phone
        self.email = email
        self.gender = gender
        self.at_work = at_work
        self.from_work = from_work
        self.password = password
        self.active = active
        self.admin = admin
        self.department_id = department_id
        self.created = datetime.datetime.now().replace(microsecond=0)

    @classmethod
    def create_staff(cls, photo=None, appointment=None, firstname=None, lastname=None, middle_name=None, phone=None,
                     email=None, gender=None, at_work=None, from_work=None, password=None, active=None, admin=None,
                     department_id=None):

        """
        Метод создания персонала
        """

        try:
            at_work = at_work.split(':')
            from_work = from_work.split(':')

            at_work_time = datetime.time(int(at_work[0]), int(at_work[1]))
            from_work_time = datetime.time(int(from_work[0]), int(from_work[1]))
        except Exception as error:
            print(error)
            at_work_time = None
            from_work_time = None

        staff = cls(photo=photo, appointment=appointment, firstname=firstname, lastname=lastname,
                    middle_name=middle_name, phone=phone, email=email, gender=gender, at_work=at_work_time,
                    from_work=from_work_time, password=password, active=active, admin=admin,
                    department_id=department_id)

        try:
            db.session.add(staff)
            db.session.commit()
            db.session.remove()
            return 'ok'
        except sqlalchemy.exc.IntegrityError as error:
            db.session.rollback()
            db.session.remove()

            if 'UNIQUE' in str(error):
                return 'not unique'
            if 'NOT NULL' in str(error):
                return None
            return f'{error}'

    @classmethod
    def add_in_department(cls, department_id=None, staff_id=None):
        """
        Метод добавления персонала в отдел
        """
        staff = cls.query.filter_by(id=staff_id).first()

        if not staff:
            return None

        staff.department_id = department_id

        try:
            db.session.commit()
            db.session.remove()
            return 'ok'
        except Exception as error:
            db.session.remove()
            db.session.rollback()
            return f'{error}'

    @classmethod
    def edit_staff(cls, staff_id=None, photo=None, appointment=None, firstname=None, lastname=None, middle_name=None,
                   gender=None, phone=None, email=None, at_work=None, from_work=None, password=None, active=True,
                   admin=False, department_id=None):
        staff = cls.query.filter(cls.id == staff_id).first()

        if not staff:
            return 'did not come'

        staff.photo = photo
        staff.appointment = appointment
        staff.firstname = firstname
        staff.lastname = lastname
        staff.middle_name = middle_name
        staff.gender = gender
        staff.phone = phone
        staff.email = email
        staff.at_work = at_work
        staff.from_work = from_work
        staff.password = password
        staff.active = active
        staff.admin = admin
        staff.department_id = department_id

        try:
            db.session.commit()
            db.session.remove()
            return 'ok'
        except sqlalchemy.exc.IntegrityError as error:
            db.session.rollback()
            db.session.remove()

            if 'UNIQUE' in str(error):
                return 'not unique'
            if 'NOT NULL' in str(error):
                return None
            return f'{error}'

    @classmethod
    def get_staff(cls, staff_id=None):
        staff = cls.query.filter(cls.id == staff_id).first()

        if not staff:
            return None

        return {
            'photo': staff.photo,
            'appointment': staff.appointment,
            'firstname': staff.firstname,
            'lastname': staff.lastname,
            'middle_name': staff.middle_name,
            'gender': staff.gender,
            'phone': staff.phone,
            'email': staff.email,
            'active': staff.active,
            'department_id': staff.department_id
        }

    @classmethod
    def get_staffs_from_department(cls, department_id=None):
        staffs = cls.query.filter(cls.department_id == department_id).all()

        if not staffs:
            return None

        data_staffs = []
        for staff in staffs:
            data_staffs.append({
                'photo': staff.photo,
                'appointment': staff.appointment,
                'firstname': staff.firstname,
                'lastname': staff.lastname,
                'middle_name': staff.middle_name,
                'gender': staff.gender,
                'phone': staff.phone,
                'email': staff.email,
                'active': staff.active,
                'department_id': staff.department_id
            })

        return data_staffs

    @classmethod
    def search_staff(cls, query=None):
        if not query:
            return None

        staffs = cls.query.all()
        if not staffs:
            return None

        data_staffs = []
        for staff in staffs:
            if query.lower() not in f'{staff.firstname} {staff.lastname} {staff.middle_name} {staff.phone}'.lower():
                continue

            data_staffs.append({
                'photo': staff.photo,
                'appointment': staff.appointment,
                'firstname': staff.firstname,
                'lastname': staff.lastname,
                'middle_name': staff.middle_name,
                'gender': staff.gender,
                'phone': staff.phone,
                'email': staff.email,
                'active': staff.active,
                'department_id': staff.department_id
            })

        return data_staffs

    def __repr__(self):
        return f'<Staff {self.firstname!r} {self.lastname!r} {self.middle_name!r}>'
