# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models dynamically
import os
import importlib

models_dir = os.path.dirname(__file__)
for filename in os.listdir(models_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f'models.{filename[:-3]}'
        importlib.import_module(module_name)