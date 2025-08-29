from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.models.questions import Question
from app.models.category import Category
from app.models import db
from app.schemas.questions import QuestionResponse
from app.errors.question_errors import QuestionEmptyError, QuestionValueError

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('/', methods=['GET'])
def get_questions():
    """
    Returns a list of all questions with their categories.
    """
    questions = Question.query.all()
    data = []
    for item in questions:
        category = {"id": item.category.id, "name": item.category.name} if item.category else None
        res = {
            "id": item.id,
            "question": item.question,
            "category": category
        }
        data.append(res)
    return jsonify(data), 200


@questions_bp.route('/', methods=['POST'])
def create_question():
    """
    Creates a new question with optional category.
    """
    data = request.get_json()
    if not data:
        raise QuestionEmptyError('No data provided.')

    text = data.get('question') or data.get('text')
    if not text or not text.strip():
        raise QuestionEmptyError('No text provided.')
    text = text.strip()
    if len(text) < 10:
        raise QuestionValueError('Text too short.')

    category_id = data.get('category_id')
    category = None
    if category_id:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404

    question = Question(question=text, category_id=category_id)
    db.session.add(question)
    db.session.commit()

    response = {
        "id": question.id,
        "question": question.question,
        "category": {"id": category.id, "name": category.name} if category else None
    }
    return jsonify(response), 201


@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    """
    Returns a question by id with its category.
    """
    question = Question.query.get(id)
    if not question:
        return jsonify({'error': 'Question with that id does not exist'}), 404

    category = {"id": question.category.id, "name": question.category.name} if question.category else None
    return jsonify({
        'id': question.id,
        'question': question.question,
        'category': category
    }), 200


@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    """
    Updates a question by id and optionally changes its category.
    """
    question = Question.query.get(id)
    if not question:
        return jsonify({'error': 'Question with that id does not exist'}), 404

    data = request.get_json()
    if not data or ('question' not in data and 'category_id' not in data):
        return jsonify({'error': 'No data provided for update'}), 400

    if 'question' in data:
        text = data['question'].strip()
        if not text:
            return jsonify({'error': 'No question text provided'}), 400
        question.question = text

    if 'category_id' in data:
        category_id = data['category_id']
        if category_id:
            category = Category.query.get(category_id)
            if not category:
                return jsonify({'error': 'Category not found'}), 404
            question.category_id = category_id
        else:
            question.category_id = None  # Remove category

    db.session.commit()
    return jsonify({'message': 'Question updated successfully'}), 200


@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    """
    Deletes a question by id.
    """
    question = Question.query.get(id)
    if not question:
        return jsonify({'error': 'Question with that id does not exist'}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Question deleted successfully'}), 200