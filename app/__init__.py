from flask import Flask, jsonify
from flask_migrate import Migrate
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from .models import db

from config import DevelopmentConfig, ProductionConfig, TestingConfig
from .routes.questions import questions_bp
from .routes.response import response_bp
from .routes.categories import categories_bp

from .models.response import Response
from .models.questions import Statistic, Question
from .models.category import Category
import os


config_mapping = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}


def create_app():
    env = os.getenv('FLASK_ENV', 'development')
    config = config_mapping.get(env, DevelopmentConfig)

    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate()
    migrate.init_app(app, db)

    app.register_blueprint(questions_bp)
    app.register_blueprint(response_bp)
    app.register_blueprint(categories_bp)
    # Просмотреть все зарегистрированные endpoint-ы
    # for rule in app.url_map.iter_rules():
    #     print(f"Endpoint: {rule.endpoint}, URL: {rule}")

    return app