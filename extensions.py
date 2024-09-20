from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Inicialize as extensões
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
