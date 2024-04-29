from flask import Blueprint, jsonify, render_template_string
import json
from app.daos.user import UserDAO
user_view = Blueprint('user_view', __name__)

@user_view.route('/w1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    template = 'templates/web/w1/get_user.json'
    user = UserDAO.get_user(user_id)
    if user:
        json_output = render_template_string(open(template).read(), user=user)
        return jsonify(user=json.loads(json_output))
    else:
        return jsonify({'error': 'User not found'}), 404
