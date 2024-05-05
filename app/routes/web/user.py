from flask import Blueprint, jsonify, render_template_string, request, make_response
import json
import traceback
from app.daos.user import UserDAO
user_view = Blueprint('user_view', __name__)
from app.middleware.auth_middleware import token_required

@user_view.route('/w1/user', methods=['GET'])
@token_required
def get_user(current_user):
    print(current_user.id)
    if request.headers.get('Content-Type') == 'application/json':
        template = 'templates/web/w1/user_show.json'
        user = UserDAO.get_user(current_user.id)
        if user:
            json_output = render_template_string(open(template).read(), user=user)
            response = jsonify(user=json.loads(json_output))
            response.status_code = 200  # Set status code to 200 (OK)
            return response
        else:
            response = jsonify({'error': 'User no found'})
            response.status_code = 404  # Set status code to 200 (OK)
            return response
    else:
        response = jsonify({'error': 'Invalid request. Expected Content-Type: application/json'})
        response.status_code = 400  # Set status code to 200 (OK)
        return response


@user_view.route('/w1/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    if request.headers.get('Content-Type') == 'application/json':
        template = 'templates/web/w1/user_index.json'
        users = UserDAO.get_all_users()
        if users:
            json_output = render_template_string(open(template).read(), users=users)
            response = jsonify(users=json.loads(json_output))
            response.status_code = 200  # Set status code to 200 (OK)
            return response
        else:
            response = jsonify({'error': 'No users found'})
            response.status_code = 404  # Set status code to 200 (OK)
            return response
    else:
        response = jsonify({'error': 'Invalid request. Expected Content-Type: application/json'})
        response.status_code = 400  # Set status code to 200 (OK)
        return response
    

@user_view.route('/w1/user/update', methods=['PUT'])
@token_required
def update_user(current_user):
    if request.headers.get('Content-Type') == 'application/json':
        template = 'templates/web/w1/user_show.json'
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        try:
            result, error = UserDAO.update_user(current_user.id, data)
            if result is True:  # Check if update was successful
                # Fetch the updated user from the database
                updated_user = UserDAO.get_user(current_user.id)
                if updated_user:
                    json_output = render_template_string(open(template).read(), user=updated_user)
                    response = jsonify(user=json.loads(json_output))
                    response.status_code = 200  # Set status code to 200 (OK)
                    return response
                else:
                    response = jsonify({'error': 'User not found after update'})
                    response.status_code = 404  # Set status code to 404 (Not Found)
                    return response
            else:
                response = jsonify({'error': error})
                response.status_code = 500  # Set status code to 500 (Internal Server Error)
                return response
        except Exception as e:
            # Print exception message and traceback for debugging
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500  # Return error message with status code 500
    else:
        response = jsonify({'error': 'Invalid request. Expected Content-Type: application/json'})
        response.status_code = 400  # Set status code to 400 (Bad Request)
        return response
    

@user_view.route('/w1/user/delete', methods=['DELETE'])
@token_required
def delete_user(current_user):
    try:
        # Call the DAO method to delete user
        deleted_user = UserDAO.delete_user(current_user.id)
        if deleted_user:
            return jsonify({'message': 'User deleted successfully'}), 200  # Return success message with status code 200 (OK)
        else:
            return jsonify({'error': 'User not found'}), 404  # Return error with status code 404 (Not Found)
    except Exception as e:
        # Print exception message and traceback for debugging
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500  # Return error message with status code 500 (Internal Server Error)
