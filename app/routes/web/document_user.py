from flask import Blueprint, jsonify, render_template_string, request, make_response
import json
import traceback
from app.daos.document_type import DocumentTypeDao
document_type_view = Blueprint('document_type_view', __name__)


@document_type_view.route('/w1/document_types/<int:document_type_id>', methods=['GET'])
def get_document_type(document_type_id):
    if request.headers.get('Content-Type') == 'application/json':
        template = 'templates/web/w1/document_type_show.json'
        document_type = DocumentTypeDao.get_document_type(document_type_id)
        if document_type:
            json_output = render_template_string(open(template).read(), document_type=document_type)
            response = jsonify(document_type=json.loads(json_output))
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


@document_type_view.route('/w1/document_types', methods=['GET'])
def get_all_document_types():
    user_id = request.args.get('user_id')  # Get user_id from query parameters
    document_type = request.args.get('document_type')  # Get document_type from query parameters
    page = request.args.get('page', default=1, type=int)  # Get page number from query parameters (default to 1 if not provided)
    page_size = request.args.get('page_size', default=10, type=int)  # Get page size from query parameters (default to 2 if not provided)
    sort_field = request.args.get('sort_field', default='document_type', type=str)  # Get sort_field from query parameters (optional)
    sort_direction = request.args.get('sort_direction', default='asc', type=str)  # Get sort_direction from query parameters (optional)

    if user_id is None:
        response = jsonify({'error': 'Missing user_id parameter'})
        response.status_code = 400  # Set status code to 400 (Bad Request)
        return response

    # Convert user_id to integer if needed
    try:
        user_id = int(user_id)
    except ValueError:
        response = jsonify({'error': 'Invalid user_id parameter. It must be an integer'})
        response.status_code = 400  # Set status code to 400 (Bad Request)
        return response

    if request.headers.get('Content-Type') == 'application/json':
        template = 'templates/web/w1/document_type_index.json'
        pagination_template = 'templates/web/w1/pagination.json'
        
        # Calculate offset based on page number and page size
        offset = (page - 1) * page_size
        
        # Fetch document types with pagination from DAO method
        document_types_result = DocumentTypeDao.get_all_document_types(
            user_id, 
            document_type=document_type, 
            offset=offset, 
            limit=page_size, 
            sort_field=sort_field, 
            sort_direction=sort_direction
        )
        
        # Extract pagination info and document types from result
        document_types = document_types_result.get('document_types', [])
        records_count = document_types_result.get('records_count', 0)
        page_no = document_types_result.get('page_no', 1)
        page_size = document_types_result.get('page_size', page_size)

        # Prepare response data
        pagination = {
            'page_no': page_no,
            'page_size': page_size,
            'count': records_count
        }
        print(document_types)
        
        json_output = render_template_string(open(template).read(), document_types=document_types)
        pagination_output = render_template_string(open(pagination_template).read(), pagination=pagination)
        response = jsonify(document_types=json.loads(json_output), pagination=json.loads(pagination_output))
        response.status_code = 200  # Set status code to 200 (OK)
        return response
    else:
        response = jsonify({'error': 'Invalid request. Expected Content-Type: application/json'})
        response.status_code = 400  # Set status code to 400 (Bad Request)
        return response
    

@document_type_view.route('/w1/document_types/<int:document_type_id>', methods=['PUT'])
def update_document_type(document_type_id):
    if request.headers.get('Content-Type') == 'application/json':
        template = 'templates/web/w1/document_type_show.json'
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        try:
            result, error = DocumentTypeDao.update_document_type(document_type_id, data)
            if result is True:  # Check if update was successful
                # Fetch the updated document_type_id from the database
                updated_document_type = DocumentTypeDao.get_document_type(document_type_id)
                if updated_document_type:
                    json_output = render_template_string(open(template).read(), document_type=updated_document_type)
                    response = jsonify(document_type=json.loads(json_output))
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
    

@document_type_view.route('/w1/document_types', methods=['POST'])
def create_document_type():
    if request.headers.get('Content-Type') == 'application/json':
        template = 'templates/web/w1/document_type_show.json'
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        try:
            # Call the DAO method to create document_type
            res, document_type_id, error = DocumentTypeDao.create_document_type(data)
            if res:
                new_document_type = DocumentTypeDao.get_document_type(document_type_id)
                if new_document_type:
                    json_output = render_template_string(open(template).read(), document_type=new_document_type)
                    response = jsonify(document_type=json.loads(json_output))
                    response.status_code = 200  # Set status code to 200 (OK)
                    return response
                else:
                    response = jsonify({'error': 'Document_type not found after update'})
                    response.status_code = 404  # Set status code to 404 (Not Found)
                    return response
            else:
                response = jsonify({'error': 'Failed to create document_type'})
                response.status_code = 500  # Set status code to 500 (Internal Server Error)
                return response
        except Exception as e:
            # Print exception message and traceback for debugging
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500  # Return error message with status code 500 (Internal Server Error)
    else:
        return jsonify({'error': 'Invalid request. Expected Content-Type: application/json'}), 400  # Return error with status code 400 (Bad Request)


@document_type_view.route('/w1/document_types/<int:document_type_id>', methods=['DELETE'])
def delete_document_type(document_type_id):
    try:
        # Call the DAO method to delete Document type
        deleted_document_type = DocumentTypeDao.delete_document_type(document_type_id)
        if deleted_document_type:
            return jsonify({'message': 'Document type deleted successfully'}), 200  # Return success message with status code 200 (OK)
        else:
            return jsonify({'error': 'Document type not found'}), 404  # Return error with status code 404 (Not Found)
    except Exception as e:
        # Print exception message and traceback for debugging
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500  # Return error message with status code 500 (Internal Server Error)
