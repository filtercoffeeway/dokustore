from flask import Blueprint, jsonify
from app.daos.user import UserDAO
user_view = Blueprint('user_view', __name__)

@user_view.route('/w1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserDAO.get_user(user_id)
    if user:
        return jsonify({'id': user.id, 'first_name': user.first_name})
    else:
        return jsonify({'error': 'User not found'}), 404