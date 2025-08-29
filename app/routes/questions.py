from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.models.questions import Question
from app.models import db
from app.schemas.questions import QuestionResponse, MessageResponse, QuestionCreate
from sqlalchemy.exc import SQLAlchemyError
from app.errors.question_errors import QuestionError, QuestionEmptyError, QuestionValueError

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('/', methods=['GET'])
def get_questions():
    """
    Returns a list of all questions.
    """
    questions = Question.query.all()

    data = []
    for item in questions:
        try:
            res = QuestionResponse.model_validate(item)
            res = res.model_dump()
            data.append(res)
        except ValidationError as e:
            continue

    return jsonify(data), 200


@questions_bp.route('/', methods=['POST'])
def create_question():
    """
    Creates a new question.
    """
    data = request.get_json()
    if not data:
        raise QuestionEmptyError('No data provided.')
    text = data.get('text')
    if not text:
        raise QuestionEmptyError('No text provided.')
    text = text.strip()
    if not text:
        raise QuestionEmptyError('No text provided.')
    if len(text) < 10:
        raise QuestionValueError('Text too short.')

    # data = QuestionCreate(**data)
    question = Question(question=text)
    db.session.add(question)
    db.session.commit()
    return jsonify(QuestionResponse(id=question.id, question=question.question).model_dump()), 201


@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    """
    Returns a question by id.
    """
    question = Question.query.get(id)
    if not question: # question is None
        return jsonify({'error': 'Question with that id does not exist'}), 404

    return jsonify({
        'id': question.id,
        'question': question.question}), 200


@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    """
    Updates a question by id.
    """
    question = Question.query.get(id)
    if not question:
        return jsonify({'error': 'Question with that id does not exist'}), 404

    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'No question text provided'}), 400

    text = data['question'].strip()
    if not text:
        return jsonify({'error': 'No question text provided'}), 400

    question.question = text
    db.session.commit()
    # return jsonify({'id': question.id, 'question': question.question}), 200
    return jsonify({'message': 'Question updated successfully'}), 200




@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    """
    Deletes a question by id.
    """
    question = Question.query.get(id)
    if not question: # if question is None
        return jsonify({'error': 'Question with that id does not exist'}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Question deleted successfully'}), 200