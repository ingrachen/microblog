from webapp.api import bp
from webapp.models import User, Post
from flask import jsonify, request
from webapp.models import dbase as db


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['GET'])
def get_users():
    #page = request.args.get('page', 1 , type=int)
    #per_page = request.args.get('per_page', 10, type=int)
    return jsonify(User.to_collection_dict(User.query, 1, 10, 'api.get_users'))


@bp.route('/users/<int:id>/posts', methods=['GET'])
def get_posts(id):
    posts = Post.query.filter_by(id=User.query.get(id))
    return jsonify(posts.to_dict())
@bp.route('/users', methods=['POST'])
def create_user():
    user = User.query.filter_by(User.query.get_or_404())


@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass