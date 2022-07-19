from flask import Blueprint, jsonify, request
from .models import Staff, Marker, Department
from .additional_functions import filled_or_empty


api = Blueprint('api', __name__)


@api.get('/api/v1/loadPhoto')
def load_photo():
    pass


@api.get('/api/v1/createStaff')
def create_staff():
    data = request.get_json()
    photo = data['photo']
    appointment = data['appointment']
    firstname = data['department_id']
    lastname = data['lastname']
    middle_name = data['middle_name']
    phone = data['phone']
    email = data['email']
    gender = data['gender']  # True/False
    at_work = data['at_work']  # '07:00'
    from_work = data['from_work']  # '20:00'
    password = data['password']
    admin = data['admin']  # True/False

    try:
        department_id = int(data['department_id'])
    except TypeError:
        department_id = None

    status = Staff.create_staff(photo=photo,
                                appointment=appointment,
                                firstname=firstname,
                                lastname=lastname,
                                middle_name=middle_name,
                                phone=phone,
                                email=email,
                                gender=gender,
                                at_work=at_work,
                                from_work=from_work,
                                password=password,
                                active=True,
                                admin=admin,
                                department_id=department_id)

    return jsonify({'status': status})


@api.get('/api/v1/editStaff')
def edit_staff():
    data = request.get_json()
    photo = data['photo']
    appointment = data['appointment']
    firstname = data['department_id']
    lastname = data['lastname']
    middle_name = data['middle_name']
    phone = data['phone']
    email = data['email']
    gender = data['gender']  # True/False
    at_work = data['at_work']  # '07:00'
    from_work = data['from_work']  # '20:00'
    password = data['password']
    admin = data['admin']  # True/False
    active = data['active']

    try:
        department_id = int(data['department_id'])
    except TypeError:
        department_id = None

    status = Staff.create_staff(
                                photo=photo,
                                appointment=appointment,
                                firstname=firstname,
                                lastname=lastname,
                                middle_name=middle_name,
                                phone=phone,
                                email=email,
                                gender=gender,
                                at_work=at_work,
                                from_work=from_work,
                                password=password,
                                active=active,
                                admin=admin,
                                department_id=department_id)

    return jsonify({'status': status})


@api.get('/api/v1/getStaff')
def get_staff():
    data = request.get_json()
    try:
        staff_id = int(data['staff_id'])
    except TypeError:
        return jsonify({'status': 'unacceptable value'}), 406

    status = Staff.get_staff(staff_id=staff_id)
    return jsonify({'status': status})


@api.get('/api/v1/addInDepartment')
def add_in_department():
    data = request.get_json()
    try:
        department_id = int(data['department_id'])
        staff_id = int(data['staff_id'])
    except TypeError:
        return jsonify({'status': 'unacceptable value'}), 406

    status = Staff.add_in_department(department_id=department_id, staff_id=staff_id)
    return jsonify({'status': status})


@api.get('/api/v1/getStaffsFromDepartment')
def get_staffs_from_department():
    data = request.get_json()
    try:
        department_id = int(data['department_id'])
    except TypeError:
        return jsonify({'status': 'unacceptable value'}), 406

    status = Staff.get_staffs_from_department(department_id=department_id)
    return jsonify({'status': status})


@api.get('/api/v1/searchStaff')
def search_staff():
    data = request.get_json()
    query = filled_or_empty(data['q'])
    if not query:
        return jsonify({'status': 'not value'}), 400

    status = Staff.search_staff(query=query)
    return jsonify({'status': status})


@api.get('/api/v1/markerIn')
def marker_in():
    data = request.get_json()

    try:
        staff_id = int(data['staff'])
        reason_in = filled_or_empty(data['reason'])
    except TypeError:
        return jsonify({'status': 'unacceptable value'}), 406

    status = Marker.marker_in(staff_id=staff_id, reason_in=reason_in)
    return jsonify({'status': status})


@api.get('/api/v1/markerOut')
def marker_out():
    data = request.get_json()

    try:
        staff_id = int(data['staff'])
        reason_out = filled_or_empty(data['reason'])
    except TypeError:
        return jsonify({'status': 'unacceptable value'}), 406

    status = Marker.marker_out(staff_id=staff_id, reason_out=reason_out)
    return jsonify({'status': status})


@api.get('/api/v1/editMarker')
def edit_marker():
    data = request.get_json()

    try:
        marker_id = int(data['marker_id'])
        time_in = filled_or_empty(data['time_in'])
        reason_in = filled_or_empty(data['reason_in'])
        time_out = filled_or_empty(data['time_out'])
        reason_out = filled_or_empty(data['reason_out'])
    except TypeError:
        return jsonify({'status': 'unacceptable value'}), 406

    status = Marker.edit_marker(marker_id=marker_id, reason_in=reason_in, reason_out=reason_out,
                                time_in=time_in, time_out=time_out)
    return jsonify({'status': status})


@api.get('/api/v1/todayMarkers')
def today_markers():
    status = Marker.today_markers()
    return jsonify({'data': status})


@api.get('/api/v1/createMarkerByAdmin')
def create_marker_by_admin():
    data = request.get_json()

    try:
        staff_id = int(data['marker_id'])
        reason_in = filled_or_empty(data['reason_in'])
        reason_out = filled_or_empty(data['reason_out'])
        time_in = filled_or_empty(data['time_in'])  # '%Y-%m-%d %H:%M'
        time_out = filled_or_empty(data['time_out'])  # '%Y-%m-%d %H:%M'
    except TypeError:
        return jsonify({'status': 'unacceptable value'}), 406

    status = Marker.create_marker_by_admin(staff_id=staff_id, reason_in=reason_in, reason_out=reason_out,
                                           time_in=time_in, time_out=time_out)
    return jsonify({'status': status})


@api.get('/api/v1/createDepartment')
def create_department():
    data = request.get_json()

    title = data['title']
    if not title or len(title) > 25:
        return jsonify({'status': 'no value or too long'}), 400

    status = Department.create_department(title=title)
    return jsonify({'status': status})


@api.get('/api/v1/editDepartment')
def edit_department():
    data = request.get_json()

    try:
        department_id = int(data['department_id'])
    except TypeError:
        return jsonify({'status': 'unacceptable value'}), 406

    title = data['title']
    if not title or len(title) > 25:
        return jsonify({'status': 'no value or too long'}), 400

    status = Department.edit_department(department_id=department_id, title=title)
    return jsonify({'status': status})
