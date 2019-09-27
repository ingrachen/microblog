from flask import Flask, request, current_app
from flask_mail import Mail
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel

from flask_babel import lazy_gettext as _l

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view ='auth.login'
login.login_message= _l('please log in to access this page')
mail = Mail()
babel =Babel()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    from webapp.auth import bp as auth_bp
    from webapp.main import bp as main_bp
    from webapp.api import bp as api_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    return app

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])









