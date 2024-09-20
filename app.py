import os
import importlib
from flask import Flask, redirect, url_for
from extensions import db, csrf, login_manager  #INFO: Importe as extensões
from models import user  # INFO: Certifique-se de importar depois que o app for criado
from models.user import create_admin
app = Flask(__name__)
app.config.from_pyfile('config.py')

# INFO: Inicialize as extensões com a aplicação
db.init_app(app)
csrf.init_app(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return user.User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('home'))

# INFO: Importar todos os modelos


models_dir = os.path.join(os.path.dirname(__file__), 'models')
for filename in os.listdir(models_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f'models.{filename[:-3]}'
        importlib.import_module(module_name)

# INFO: Importar e registrar todos os blueprints
routes_dir = os.path.join(os.path.dirname(__file__), 'routes')
for filename in os.listdir(routes_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f'routes.{filename[:-3]}'
        module = importlib.import_module(module_name)
        if hasattr(module, 'bp'):
            app.register_blueprint(module.bp)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin()
        
    app.run(debug=True)
