from flask import Flask
from flask_migrate import Migrate
from .models import db

from config import DevelopmentConfig, ProductionConfig, TestingConfig
from .routes.questions import questions_bp
from .routes.response import response_bp

from .models.response import Response
from .models.questions import Statistic, Question

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

    return app