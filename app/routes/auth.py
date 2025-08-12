from flask import Blueprint, jsonify, request, abort, g
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_pydantic_spec import Request, Response
from pydantic import ValidationError

from app import spec
from app.schemas.user import * 
from app.crud.user import *
from app.schemas import PaginationParams

from app.utils.decorators import with_session, admin_required
from app.utils.pagination import parse_pagination_params

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/register', methods=['POST'])
@spec.validate(
    body=Request(UserRegisterSchema),
    resp=Response(HTTP_201=RegisterResponse, HTTP_409=None, HTTP_422=None),
    tags=["Auth"],
)
@with_session
def register():
    data = request.context.body  # Pydantic validated data
    
    if get_user_by_email(g.session, data.email) or get_user_by_username(g.session, data.username):
        abort(409, description="Username or email already exists")
    
    create_user(g.session, data.username, data.email, data.password)
    
    return {"message": "User registered successfully"}, 201

@auth_bp.route('/login', methods=['POST'])
@spec.validate(
    body=Request(UserLoginSchema),
    resp=Response(HTTP_200=LoginResponse, HTTP_401=None, HTTP_422=None),
    tags=["Auth"]
)
@with_session
def login():
    data = request.get_json()
    user = get_user_by_email(g.session, data['email'])
    if not user or not verify_password(data['password'], user.password_hash):
        abort(401, description="Invalid credentials")
    token = create_access_token(identity=str(user.id))
    
    return jsonify({"access_token": token}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
@spec.validate(
    resp=Response(HTTP_200=UserOut, HTTP_401=None),
    tags=["Auth"]
)
@with_session
def me():
    user_id = int(get_jwt_identity())
    user = get_user_by_id(g.session, user_id)
    if not user:
        abort(404, description="User not found")
    user_dict = user.model_dump()
    user_dict.pop("password_hash", None)  # Remove sensitive info
    
    return jsonify(user_dict), 200



@auth_bp.route('/users', methods=['GET'])
@jwt_required()
@with_session
@admin_required
@spec.validate(
    resp=Response(HTTP_200=UsersListResponse, HTTP_403=None),
    tags=["Auth"]
)
def list_users_route():
    pagination, error = parse_pagination_params()
    if error:
        return error, 422

    users, total = list_all_users(g.session, limit=pagination.limit, offset=pagination.offset)
    result = [user.model_dump() for user in users]

    return {
        "users": result,
        "total": total,
        "limit": pagination.limit,
        "offset": pagination.offset
    }, 200




@auth_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@jwt_required()
@spec.validate(
    body=Request(UserRoleUpdateSchema),
    resp=Response(HTTP_200=UserOut, HTTP_400=None, HTTP_403=None, HTTP_404=None),
    tags=["Auth"]
)
@admin_required
@with_session
def change_user_role_route(user_id: int):
    data = request.context.body
    user = change_user_role(g.session, user_id, data.role)
    if not user:
        abort(404, description="User not found")

    user_dict = user.model_dump()
    user_dict.pop("password_hash", None)
    return jsonify(user_dict), 200
