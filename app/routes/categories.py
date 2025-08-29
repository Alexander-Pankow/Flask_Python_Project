from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.models import db
from app.models.category import Category
from app.schemas.category import CategoryBase, CategoryResponse

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")

@categories_bp.route("/", methods=["POST"])
def create_category():
    try:
        data = CategoryBase(**request.get_json())
    except ValidationError as e:
        return jsonify(e.errors()), 400

    category = Category(name=data.name)
    db.session.add(category)
    db.session.commit()

    return jsonify(CategoryResponse.from_orm(category).dict()), 201


@categories_bp.route("/", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([CategoryResponse.from_orm(cat).dict() for cat in categories]), 200


@categories_bp.route("/<int:id>", methods=["PUT"])
def update_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"message": "Категория не найдена"}), 404

    try:
        data = CategoryBase(**request.get_json())
    except ValidationError as e:
        return jsonify(e.errors()), 400

    category.name = data.name
    db.session.commit()

    return jsonify(CategoryResponse.from_orm(category).dict()), 200


@categories_bp.route("/<int:id>", methods=["DELETE"])
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"message": "Категория не найдена"}), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": f"Категория {id} удалена"}), 200