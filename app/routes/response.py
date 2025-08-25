from flask import Blueprint


response_bp = Blueprint('response', __name__, url_prefix='/responses')


@response_bp.route('/', methods=['GET'])
def get_responses():
    """
    Returns statistic by responses
    :return:
    """
    return "Статистика всех ответов"


@response_bp.route('/', methods=['POST'])
def create_response():
    """
    Adds a new response
    :return:
    """
    return "Ответ добавлен"