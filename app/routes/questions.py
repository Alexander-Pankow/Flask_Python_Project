from flask import Blueprint


questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('/', methods=['GET'])
def get_questions():
    """
    Returns a list of all questions.
    """
    return "Список всех вопросов"


@questions_bp.route('/', methods=['POST'])
def create_question():
    """
    Creates a new question.
    """
    return "Вопрос создан"


@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    """
    Returns a question by id.
    """
    return f"Детали вопроса {id}"


@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    """
    Updates a question by id.
    """
    return f"Вопрос {id} обновлен"


@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    """
    Deletes a question by id.
    """
    return f"Вопрос {id} удален"