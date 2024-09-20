from flask import Blueprint, request, redirect, url_for, make_response, jsonify, render_template
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash
from models.user import User
from app import db, csrf

bp = Blueprint('auth', __name__)

@bp.route('/auth', methods=['POST'])
@csrf.exempt
def auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            response = {'success': True}
            return make_response(jsonify(response), 200)
        else:
            response = {'sucess': False}
            return make_response(jsonify(response), 200)
    return render_template('index.html')



@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.home'))
