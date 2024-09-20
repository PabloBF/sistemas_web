from flask import Blueprint, request, redirect, url_for, make_response, jsonify, render_template
from flask_login import login_user, current_user,login_required,LoginManager
from werkzeug.security import check_password_hash
from models.user import User
from models.credores import Title
from app import db, csrf

bp = Blueprint('contas', __name__)
@bp.route('/contas')
@login_required
def credores():
    todas_contas = Title.query.all()
    return render_template('contas.html',contas=todas_contas)

