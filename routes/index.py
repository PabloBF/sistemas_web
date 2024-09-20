from flask import Blueprint, request, redirect, url_for, make_response, jsonify, render_template
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
from models.user import User
from app import db, csrf

bp = Blueprint('index', __name__)

@csrf.exempt
@bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    return render_template('index.html')
