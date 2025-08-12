from flask import Blueprint, jsonify, abort, request, g
from flask_jwt_extended import jwt_required
from flask_pydantic_spec import Response, Request
from pydantic import ValidationError

from app.schemas.category import CategoryCreateSchema, CategoryOut, CategoriesListResponse, CategoryDeleteMessageOut
from app import spec
from app.crud.category import *
from app.crud.user import get_user_by_id
from app.schemas import PaginationParams
from app.models.category import Category

from app.utils.decorators import with_session, admin_required

category_bp = Blueprint('category', __name__, url_prefix='/api/categories')

@category_bp.route('', methods=['GET'])
@spec.validate(
    resp=Response(HTTP_200=CategoriesListResponse),
    tags=["Categories"]
)
@with_session
def list_categories_route():
    try:
        pagination = PaginationParams(
            limit=int(request.args.get('limit', 10)),
            offset=int(request.args.get('offset', 0))
        )
    except ValidationError as e:
        return {"error": e.errors()}, 422

    categories, total = list_categories(g.session, limit=pagination.limit, offset=pagination.offset)
    result = [cat.model_dump() for cat in categories]

    return {
        "categories": result,
        "total": total,
        "limit": pagination.limit,
        "offset": pagination.offset
    }, 200

@category_bp.route('', methods=['POST'])
@jwt_required()
@admin_required
@with_session
@spec.validate(
    body=Request(CategoryCreateSchema),
    resp=Response(HTTP_201=CategoryOut, HTTP_401=None, HTTP_403=None, HTTP_422=None),
    tags=["Categories"]
)
def create_category_route():
    data = request.context.body

    if get_category_by_name_or_slug(g.session, data.name, data.slug):
        abort(409, description="Category with that name or slug already exists")

    new_cat = create_category(g.session, data.name, data.slug)
    return new_cat.model_dump(), 201


@category_bp.route('/<int:cat_id>', methods=['DELETE'])
@jwt_required()
@admin_required
@with_session
@spec.validate(
    resp=Response(HTTP_200=CategoryDeleteMessageOut, HTTP_401=None, HTTP_403=None, HTTP_404=None),
    tags=["Categories"]
)
def delete_category_route(cat_id: int):
    cat = get_category_by_id(g.session, cat_id)
    if not cat:
        abort(404, description="Category not found")

    delete_category(g.session, cat)
    return jsonify({"message": "Category deleted successfully"}), 200
