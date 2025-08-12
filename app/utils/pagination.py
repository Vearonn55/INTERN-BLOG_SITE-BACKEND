from flask import request
from pydantic import ValidationError
from app.schemas import PaginationParams

def parse_pagination_params(default_limit=10, default_offset=0):
    try:
        pagination = PaginationParams(
            limit=int(request.args.get('limit', default_limit)),
            offset=int(request.args.get('offset', default_offset))
        )
        return pagination, None
    except ValidationError as e:
        return None, {"error": e.errors()}

def serialize_post(post):
    post_dict = post.model_dump()
    post_dict['author'] = {
        'id': post.author.id,
        'username': post.author.username
    }
    post_dict['category'] = {
        'id': post.category.id,
        'name': post.category.name
    }
    post_dict.pop('author_id', None)
    post_dict.pop('category_id', None)
    post_dict['created_at'] = post_dict['created_at'].isoformat()
    if post_dict.get('updated_at'):
        post_dict['updated_at'] = post_dict['updated_at'].isoformat()
    return post_dict

def build_paginated_response(items, total, pagination):
    result = [serialize_post(item) for item in items]
    return {
        "posts": result,
        "total": total,
        "limit": pagination.limit,
        "offset": pagination.offset
    }
