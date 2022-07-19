from flask import Blueprint, render_template


routes = Blueprint('routes', __name__)


@routes.get('/')
def new_staff():
    return render_template('index.html')
