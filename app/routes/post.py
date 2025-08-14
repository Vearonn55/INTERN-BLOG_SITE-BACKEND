from flask import Blueprint, jsonify, abort, request, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_pydantic_spec import Response, Request
from pydantic import ValidationError

from app.schemas.post import PostCreateSchema, PostOut, PostsListResponse, PostDeleteMessageOut
from app import spec
from app.crud.post import *
from app.crud.user import get_user_by_id
from app.crud.category import get_category_by_id
from app.schemas import PaginationParams
from app.utils.decorators import with_session, admin_required
from app.utils.pagination import parse_pagination_params, serialize_post, build_paginated_response

post_bp = Blueprint('post', __name__, url_prefix='/api/posts')

@post_bp.route('', methods=['GET'])
@spec.validate(
    resp=Response(HTTP_200=PostsListResponse),
    tags=["Posts"]
)
@with_session
def list_posts_route():
    pagination, error = parse_pagination_params()
    if error:
        return error, 422

    posts, total = list_posts(g.session, limit=pagination.limit, offset=pagination.offset)
    response = build_paginated_response(posts, total, pagination)
    return response, 200

@post_bp.route('', methods=['POST'])
@jwt_required()
@with_session
@spec.validate(
    body=Request(PostCreateSchema),
    resp=Response(HTTP_201=PostOut, HTTP_401=None, HTTP_422=None),
    tags=["Posts"]
)
def create_post_route():
    data = request.context.body
    user_id = int(get_jwt_identity())

    post = create_post(
        g.session,
        title=data.title,
        slug=data.slug,
        content=data.content,
        image_url=data.image_url,
        category_id=data.category_id,
        published=data.published,
        author_id=user_id
    )

    author = get_user_by_id(g.session, user_id)
    category = get_category_by_id(g.session, data.category_id)

    result = PostOut(
        id=post.id,
        title=post.title,
        slug=post.slug,
        content=post.content,
        image_url=post.image_url,
        created_at=post.created_at,
        published=post.published,
        author={"id": author.id, "username": author.username},
        category={"id": category.id, "name": category.name}
    )

    response_dict = result.model_dump()
    response_dict["created_at"] = response_dict["created_at"].isoformat()

    return response_dict, 201

@post_bp.route('/<int:post_id>', methods=['GET'])
@spec.validate(
    resp=Response(HTTP_200=PostOut, HTTP_404=None),
    tags=["Posts"]
)
@with_session
def get_post_route(post_id: int):
    post = get_post_by_id(g.session, post_id)
    if not post or not post.published:
        abort(404, description="Post not found or not published")

    author = post.author
    category = post.category

    data = post.model_dump()
    data.pop('author_id', None)
    data.pop('category_id', None)

    data['author'] = {
        "id": author.id,
        "username": author.username
    }
    data['category'] = {
        "id": category.id,
        "name": category.name
    }

    data['created_at'] = data['created_at'].isoformat()
    if data.get('updated_at'):
        data['updated_at'] = data['updated_at'].isoformat()

    return jsonify(data), 200

@post_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
@with_session
@spec.validate(
    body=Request(PostCreateSchema),
    resp=Response(HTTP_200=PostOut, HTTP_401=None, HTTP_403=None, HTTP_404=None, HTTP_422=None),
    tags=["Posts"]
)
def update_post_route(post_id: int):
    data = request.context.body
    user_id = int(get_jwt_identity())

    post = get_post_by_id(g.session, post_id)
    if not post:
        abort(404, description="Post not found")

    if post.author_id != user_id:
        abort(403, description="You do not have permission to edit this post")

    updated_post = update_post(
        g.session,
        post,
        title=data.title,
        slug=data.slug,
        content=data.content,
        image_url=data.image_url,
        category_id=data.category_id,
        published=data.published
    )

    data_out = updated_post.model_dump()
    data_out['created_at'] = data_out['created_at'].isoformat()
    if data_out.get('updated_at'):
        data_out['updated_at'] = data_out['updated_at'].isoformat()

    return jsonify(data_out), 200

@post_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
@admin_required
@with_session
@spec.validate(
    resp=Response(HTTP_200=PostDeleteMessageOut, HTTP_401=None, HTTP_403=None, HTTP_404=None),
    tags=["Posts"]
)
def delete_post_route(post_id: int):
    post = get_post_by_id(g.session, post_id)
    if not post:
        abort(404, description="Post not found")

    delete_post(g.session, post)

    return jsonify({"message": "Post deleted successfully"}), 200

@post_bp.route('/unpublished', methods=['GET'])
@jwt_required()
@spec.validate(
    body=Request(PaginationParams),
    resp=Response(HTTP_200=PostsListResponse),
    tags=["Posts"]
)
@with_session
def list_unpublished_posts_route():
    pagination, error = parse_pagination_params()
    if error:
        return error, 422

    posts, total = list_unpublished_posts(g.session, limit=pagination.limit, offset=pagination.offset), count_unpublished_posts(g.session)

    response = build_paginated_response(posts, total, pagination)
    return response, 200

@post_bp.route('/myposts', methods=['GET'])
@jwt_required()
@spec.validate(
    body=Request(PaginationParams),
    resp=Response(HTTP_200=PostsListResponse),
    tags=["Posts"]
)
@with_session
def list_my_posts_route():
    pagination, error = parse_pagination_params()
    if error:
        return error, 422

    user_id = int(get_jwt_identity())

    posts, total = list_posts_by_author(g.session, user_id, limit=pagination.limit, offset=pagination.offset)

    response = build_paginated_response(posts, total, pagination)
    return response, 200

@post_bp.route('/<int:post_id>/publish', methods=['PUT'])
@jwt_required()
@admin_required
@with_session
@spec.validate(
    resp=Response(HTTP_200=PostOut, HTTP_401=None, HTTP_403=None, HTTP_404=None),
    tags=["Posts"]
)
def publish_post_route(post_id: int):
    post = get_post_by_id(g.session, post_id)
    if not post:
        abort(404, description="Post not found")

    post.published = True
    g.session.commit()

    data_out = post.model_dump()

    # Fix timestamp formatting
    if post.created_at:
        data_out['created_at'] = post.created_at.isoformat()
    if post.updated_at:
        data_out['updated_at'] = post.updated_at.isoformat()

    data_out['author'] = {
        "id": post.author.id,
        "username": post.author.username
    }
    data_out['category'] = {
        "id": post.category.id,
        "name": post.category.name
    }

    return jsonify(data_out), 200
