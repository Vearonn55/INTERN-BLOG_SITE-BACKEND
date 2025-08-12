from flask import Blueprint, jsonify, abort, request, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_pydantic_spec import Response, Request
from pydantic import ValidationError

from app.schemas.comment import CommentCreateSchema, CommentOut, CommentsListResponse, CommentDeleteMessageOut
from app import spec
from app.crud.comment import list_comments, create_comment, get_comment_by_id, delete_comment
from app.crud.user import get_user_by_id
from app.schemas import PaginationParams
from app.utils.decorators import with_session, admin_required
from app.crud.post import get_post_by_id

comment_bp = Blueprint('comment', __name__, url_prefix='/api/comments')

@comment_bp.route('/<int:post_id>', methods=['GET'])
@spec.validate(
    resp=Response(HTTP_200=CommentsListResponse),
    tags=["Comments"]
)
@with_session
def list_comments_route(post_id: int):
    try:
        pagination = PaginationParams(
            limit=int(request.args.get('limit', 10)),
            offset=int(request.args.get('offset', 0))
        )
    except ValidationError as e:
        return {"error": e.errors()}, 422

    comments, total = list_comments(g.session, post_id, limit=pagination.limit, offset=pagination.offset)
    result = []
    for comment in comments:
        d = comment.model_dump()
        d['created_at'] = d['created_at'].isoformat()
        result.append(d)

    return {
        "comments": result,
        "total": total,
        "limit": pagination.limit,
        "offset": pagination.offset
    }, 200

@comment_bp.route('/<int:post_id>', methods=['POST'])
@jwt_required()
@with_session
@spec.validate(
    body=Request(CommentCreateSchema),
    resp=Response(HTTP_201=CommentOut, HTTP_401=None),
    tags=["Comments"]
)
def add_comment_route(post_id: int):
    data = request.context.body
    user_id = int(g.jwt_oid) if hasattr(g, 'jwt_oid') else int(get_jwt_identity())
    post = get_post_by_id(g.session, post_id)
    if not post or not post.published:
        abort(404, description="Post not found or not published")

    comment = create_comment(g.session, data.content, user_id, post_id)
    comment_dict = comment.model_dump()
    comment_dict['created_at'] = comment_dict['created_at'].isoformat()

    return comment_dict, 201

@comment_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
@admin_required
@with_session
@spec.validate(
    resp=Response(HTTP_200=CommentDeleteMessageOut, HTTP_401=None, HTTP_403=None, HTTP_404=None),
    tags=["Comments"]
)
def delete_comment_route(comment_id: int):
    comment = get_comment_by_id(g.session, comment_id)
    if not comment:
        abort(404, description="Comment not found")

    delete_comment(g.session, comment)
    return jsonify({"message": "Comment deleted successfully"}), 200
