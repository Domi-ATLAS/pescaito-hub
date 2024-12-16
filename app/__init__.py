# app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv

from core.configuration.configuration import get_app_version
from core.managers.module_manager import ModuleManager
from core.managers.config_manager import ConfigManager
from core.managers.error_handler_manager import ErrorHandlerManager
from core.managers.logging_manager import LoggingManager

# Load environment variables
load_dotenv()

# Create instances for extensions
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()  # Instancia de Flask-Mail aquí

def create_app(config_name='development'):
    app = Flask(__name__)

    # Load configuration according to environment
    config_manager = ConfigManager(app)
    config_manager.load_config(config_name=config_name)

    # Configuración de Flask-Mail para Outlook/Hotmail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587  # Puerto para TLS
    app.config['MAIL_USE_TLS'] = True  # Usar TLS
    app.config['MAIL_USE_SSL'] = False  # No usar SSL
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Tu correo de Gmail
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # La contraseña de la aplicación de Gmail
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')  # El correo por defecto para enviar

    # Inicialización de Flask-Mail
    mail.init_app(app)

    # Initialize SQLAlchemy and Migrate with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register modules
    module_manager = ModuleManager(app)
    module_manager.register_modules()

    # Register login manager
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        from app.modules.auth.models import User
        return User.query.get(int(user_id))

    # Set up logging
    logging_manager = LoggingManager(app)
    logging_manager.setup_logging()

    # Initialize error handler manager
    error_handler_manager = ErrorHandlerManager(app)
    error_handler_manager.register_error_handlers()

    # Injecting environment variables into jinja context
    @app.context_processor
    def inject_vars_into_jinja():
        return {
            'FLASK_APP_NAME': os.getenv('FLASK_APP_NAME'),
            'FLASK_ENV': os.getenv('FLASK_ENV'),
            'DOMAIN': os.getenv('DOMAIN', 'localhost'),
            'APP_VERSION': get_app_version()
        }

    return app

app = create_app() 


