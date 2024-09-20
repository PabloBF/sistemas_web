from flask import Blueprint, request, redirect, url_for, make_response, jsonify, render_template
from flask_login import login_user, current_user,login_required,LoginManager
from werkzeug.security import check_password_hash
from models.user import User
from models.credores import Credor
from app import db, csrf

bp = Blueprint('credores', __name__)
@bp.route('/credores')
@login_required
def credores():
    todos_credores = Credor.query.all()
    return render_template('credores.html',credores=todos_credores)

