from flask import Blueprint, jsonify, render_template_string, request, current_app
import json
import traceback
import bcrypt
from app.daos.user import UserDAO
from datetime import datetime, timedelta
import uuid
import jwt
from app.util.account_util import auth
account_view = Blueprint('account_view', __name__)


@account_view.route('/w1/account/login', methods=['POST'])
def login():
    if request.headers.get('Content-Type') == 'application/json':
        template = 'templates/web/w1/account_login.json'
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        mandatory_fields = {'password', 'email'}
        if not mandatory_fields.issubset(data.keys()):
            missing_fields = mandatory_fields - set(data.keys())
            return jsonify({'error': f'Missing mandatory fields: {", ".join(missing_fields)}'}), 400
        
        try:
            user = UserDAO.get_user_by_email(data['email'])

            if not user:
                response = jsonify({'error': 'Email or password is incorrect'})
                response.status_code = 404  # Set status code to 404 (Not Found)
                return response
            
            userBytes = data['password'].encode('utf-8') 
            print(userBytes)
            result = bcrypt.checkpw(userBytes, user.password.encode('utf-8'))

            if not result:
                response = jsonify({'error': 'Email or password is incorrect'})
                response.status_code = 404  # Set status code to 404 (Not Found)
                return response
            
            auth_token = auth.generate_token(50)
            print(auth_token)
            payload = {}
            payload['auth_token'] = auth_token
            payload['auth_expires_at'] = datetime.now() + timedelta(minutes=30)
            payload['auth_created_at'] = datetime.now()

            result, error = UserDAO.update_user(user.id, payload)

            if result is True:  # Check if update was successful
                # Fetch the updated user from the database
                updated_user = UserDAO.get_user(user.id)
                if updated_user:
                    token = jwt.encode({'auth_token': auth_token}, current_app.config['SECRET_KEY'], 'HS256')
                    json_output = render_template_string(open(template).read(), account=updated_user, token=token)
                    response = jsonify(user=json.loads(json_output))
                    response.status_code = 201  # Set status code to 200 (OK)
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
            return jsonify({'error': str(e)}), 500  # Return error message with status code 500 (Internal Server Error)

    else:
        return jsonify({'error': 'Invalid request. Expected Content-Type: application/json'}), 400  # Return error with status code 400 (Bad Request)

@account_view.route('/w1/account/signup', methods=['POST'])
def signup():
    if request.headers.get('Content-Type') == 'application/json':
        template = 'templates/web/w1/account_signup.json'
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Check if all mandatory fields are present in the payload
        mandatory_fields = {'password', 'first_name', 'last_name', 'email'}
        if not mandatory_fields.issubset(data.keys()):
            missing_fields = mandatory_fields - set(data.keys())
            return jsonify({'error': f'Missing mandatory fields: {", ".join(missing_fields)}'}), 400

        try:
            user = UserDAO.get_user_by_email(data['email'])
            if user:
                response = jsonify({'error': 'Email address already exists.'})
                response.status_code = 409  # Set status code to 404 (Not Found)
                return response
            
            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            # Replace the original password with the hashed one
            data['password'] = hashed_password.decode('utf-8')
            data['created_at'] = datetime.now()
            data['status'] = 'new'
            data['verification_token'] = str(uuid.uuid4())
            
            # Call the DAO method to create user
            res, user_id, error = UserDAO.create_user(data)
            if res:
                new_user = UserDAO.get_user(user_id)
                if new_user:
                    json_output = render_template_string(open(template).read(), user=new_user)
                    response = jsonify(user=json.loads(json_output))
                    response.status_code = 201  # Set status code to 200 (OK)
                    return response
                else:
                    response = jsonify({'error': 'User not found after create'})
                    response.status_code = 404  # Set status code to 404 (Not Found)
                    return response
            else:
                response = jsonify({'error': error})
                response.status_code = 400  # Set status code to 500 (Internal Server Error)
                return response
        except Exception as e:
            # Print exception message and traceback for debugging
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500  # Return error message with status code 500 (Internal Server Error)
    else:
        return jsonify({'error': 'Invalid request. Expected Content-Type: application/json'}), 400  # Return error with status code 400 (Bad Request)


@account_view.route('/w1/account/verify/<string:verification_token>', methods=['POST'])
def verify(verification_token):
    if request.headers.get('Content-Type') == 'application/json':
        print('inside method')
        
        try:
            user = UserDAO.get_user_by_verification_token(verification_token)
            if not user:
                response = jsonify({'error': 'Invalid verification token'})
                response.status_code = 404  # Set status code to 404 (Not Found)
                return response
        
            if user.verified_at:
                response = jsonify({'error': 'Email already verified'})
                response.status_code = 404  # Set status code to 404 (Not Found)
                return response
            
            payload = {}
            payload['verified_at'] = datetime.now()
            payload['status'] = 'active'

            result, error = UserDAO.update_user(user.id, payload)
            if result is True:  # Check if update was successful
                # Fetch the updated user from the database
                response = jsonify({'message': 'Email verified successfully.'})
                response.status_code = 200  # Set status code to 404 (Not Found)
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
        return jsonify({'error': 'Invalid request. Expected Content-Type: application/json'}), 400  # Return error with status code 400 (Bad Request)
