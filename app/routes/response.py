from flask import Blueprint, jsonify, request
from app.models.response import Response
from app.models.questions import Statistic, Question
from pydantic import BaseModel, ValidationError
from app.models import db

response_bp = Blueprint('response', __name__, url_prefix='/responses')


@response_bp.route('/', methods=['GET'])
def get_responses():
    """
    Returns statistic by responses
    :return:
    """
    statistics = Statistic.query.all()
    results = [
        {
            "question_id": stat.question_id,
            "agree_count": stat.agree_count,
            "disagree_count": stat.disagree_count
        }
        for stat in statistics
    ]
    return jsonify(results), 200


@response_bp.route('/', methods=['POST'])
def create_response():
    """
    Adds a new response
    :return:
    """
    data = request.get_json()
    if not data or 'question_id' not in data or 'is_agree' not in data:
        return jsonify({'message': "Некорректные данные"}), 400

    question = Question.query.get(data['question_id'])
    if not question:
        return jsonify({'message': "Вопрос не найден"}), 404

    response = Response(
        question_id=question.id,
        is_agree=data['is_agree']
    )
    db.session.add(response)

    # Обновление статистики
    statistic = Statistic.query.filter_by(question_id=question.id).first()
    if not statistic:
        statistic = Statistic(question_id=question.id, agree_count=0, disagree_count=0)
        db.session.add(statistic)
    if data['is_agree']:
        statistic.agree_count += 1
    else:
        statistic.disagree_count += 1

    db.session.commit()

    return jsonify({'message': f"Ответ на вопрос {question.id} добавлен"}), 201

@response_bp.route('/<int:response_id>', methods=['PUT'])
def update_response(response_id: int):
    """
    Updates an existing response without a separate Pydantic model
    """
    response = Response.query.get(response_id)
    if not response:
        return jsonify({'message': "Ответ не найден"}), 404

    data = request.get_json()
    if not data or 'is_agree' not in data:
        return jsonify({'message': "Поле 'is_agree' обязательно"}), 400

    if not isinstance(data['is_agree'], bool):
        return jsonify({'message': "Поле 'is_agree' должно быть bool"}), 400

    # Update statistics counts
    statistic = Statistic.query.filter_by(question_id=response.question_id).first()
    if statistic:
        if response.is_agree:
            statistic.agree_count -= 1
        else:
            statistic.disagree_count -= 1

        if data['is_agree']:
            statistic.agree_count += 1
        else:
            statistic.disagree_count += 1

    # Обновляем ответ
    response.is_agree = data['is_agree']
    db.session.commit()

    return jsonify({'message': f"Ответ {response_id} обновлён"}), 200


@response_bp.route('/<int:response_id>', methods=['DELETE'])
def delete_response(response_id: int):
    """
    Deletes an existing response
    """
    response = Response.query.get(response_id)
    if not response:
        return jsonify({'message': "Ответ не найден"}), 404

    statistic = Statistic.query.filter_by(question_id=response.question_id).first()
    if statistic:
        if response.is_agree:
            statistic.agree_count -= 1
        else:
            statistic.disagree_count -= 1

    db.session.delete(response)
    db.session.commit()

    return jsonify({'message': f"Ответ {response_id} удалён"}), 200