from flask import Blueprint, jsonify, render_template_string, request
import json
import traceback
from app.daos.document import DocumentDao
from app.util.template_util import Pagination
document_view = Blueprint('document_view', __name__)


@document_view.route('/w1/documents/<int:document_id>', methods=['GET'])
def get_document(document_id):
    if request.headers.get('Content-Type') == 'application/json':
        template = 'templates/web/w1/document_show.json'
        document = DocumentDao.get_document(document_id)
        if document:
            json_output = render_template_string(open(template).read(), document=document)
            response = jsonify(document=json.loads(json_output))
            response.status_code = 200  # Set status code to 200 (OK)
            return response
        else:
            response = jsonify({'error': 'Document no found'})
            response.status_code = 404  # Set status code to 200 (OK)
            return response
    else:
        response = jsonify({'error': 'Invalid request. Expected Content-Type: application/json'})
        response.status_code = 400  # Set status code to 200 (OK)
        return response


@document_view.route('/w1/documents', methods=['GET'])
def get_all_documents():
    user_id = request.args.get('user_id')  # Get user_id from query parameters
    document_type_id = request.args.get('document_type_id')  # Get user_id from query parameters
    document_name = request.args.get('document_name')  # Get document_name from query parameters
    page = request.args.get('page', default=1, type=int)  # Get page number from query parameters (default to 1 if not provided)
    page_size = request.args.get('page_size', default=10, type=int)  # Get page size from query parameters (default to 2 if not provided)
    sort_field = request.args.get('sort_field', default='document_name', type=str)  # Get sort_field from query parameters (optional)
    sort_direction = request.args.get('sort_direction', default='asc', type=str)  # Get sort_direction from query parameters (optional)

    if user_id is None:
        response = jsonify({'error': 'Missing user_id parameter'})
        response.status_code = 400  # Set status code to 400 (Bad Request)
        return response
    
    try:
        user_id = int(user_id)
    except ValueError:
        response = jsonify({'error': 'Invalid user_id parameter. It must be an integer'})
        response.status_code = 400  # Set status code to 400 (Bad Request)
        return response

    # Convert document_type_id to integer if needed
    try:
        document_type_id = int(document_type_id)
    except ValueError:
        response = jsonify({'error': 'Invalid document_type_id parameter. It must be an integer'})
        response.status_code = 400  # Set status code to 400 (Bad Request)
        return response

    if request.headers.get('Content-Type') == 'application/json':
        template = 'templates/web/w1/document_index.json'
        
        # Calculate offset based on page number and page size
        offset = (page - 1) * page_size
        
        # Fetch document types with pagination from DAO method
        document_result = DocumentDao.get_all_documents(
            user_id=user_id,
            document_type_id=document_type_id, 
            document_name=document_name, 
            offset=offset, 
            limit=page_size, 
            sort_field=sort_field, 
            sort_direction=sort_direction
        )
        
        # Extract pagination info and document types from result
        documents = document_result.get('documents', [])
        records_count = document_result.get('records_count', 0)
        page_no = document_result.get('page_no', 1)
        page_size = document_result.get('page_size', page_size)

        # Prepare response data
        pagination = Pagination.format_pagination(page_no, page_size, records_count)
        
        json_output = render_template_string(open(template).read(), documents=documents)
        response = jsonify(documents=json.loads(json_output), pagination=json.loads(pagination))
        response.status_code = 200  # Set status code to 200 (OK)
        return response
    else:
        response = jsonify({'error': 'Invalid request. Expected Content-Type: application/json'})
        response.status_code = 400  # Set status code to 400 (Bad Request)
        return response
    

@document_view.route('/w1/documents/<int:document_id>', methods=['PUT'])
def update_document(document_id):
    if request.headers.get('Content-Type') == 'application/json':
        template = 'templates/web/w1/document_show.json'
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        try:
            result, error = DocumentDao.update_document(document_id, data)
            if result is True:  # Check if update was successful
                # Fetch the updated document_id from the database
                updated_document = DocumentDao.get_document(document_id)
                if updated_document:
                    json_output = render_template_string(open(template).read(), document=updated_document)
                    response = jsonify(document=json.loads(json_output))
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
    

@document_view.route('/w1/documents', methods=['POST'])
def create_document():
    if request.headers.get('Content-Type') == 'application/json':
        template = 'templates/web/w1/document_show.json'
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        try:
            # Call the DAO method to create document
            res, document_id, error = DocumentDao.create_document(data)
            if res:
                new_document = DocumentDao.get_document(document_id)
                if new_document:
                    json_output = render_template_string(open(template).read(), document=new_document)
                    response = jsonify(document_type=json.loads(json_output))
                    response.status_code = 200  # Set status code to 200 (OK)
                    return response
                else:
                    response = jsonify({'error': 'Document not found after update'})
                    response.status_code = 404  # Set status code to 404 (Not Found)
                    return response
            else:
                response = jsonify({'error': 'Failed to create document'})
                response.status_code = 500  # Set status code to 500 (Internal Server Error)
                return response
        except Exception as e:
            # Print exception message and traceback for debugging
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500  # Return error message with status code 500 (Internal Server Error)
    else:
        return jsonify({'error': 'Invalid request. Expected Content-Type: application/json'}), 400  # Return error with status code 400 (Bad Request)


@document_view.route('/w1/documents/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    try:
        # Call the DAO method to delete Document 
        deleted_document = DocumentDao.delete_document(document_id)
        if deleted_document:
            return jsonify({'message': 'Document  deleted successfully'}), 200  # Return success message with status code 200 (OK)
        else:
            return jsonify({'error': 'Document  not found'}), 404  # Return error with status code 404 (Not Found)
    except Exception as e:
        # Print exception message and traceback for debugging
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500  # Return error message with status code 500 (Internal Server Error)


@document_view.route('/w1/documents/summary/<int:user_id>', methods=['GET'])
def get_document_summary(user_id):
    if request.headers.get('Content-Type') == 'application/json':
        template = 'templates/web/w1/document_summary.json'
        document_summary = DocumentDao.get_document_summary(user_id)
        print(document_summary)
        if document_summary:
            json_output = render_template_string(open(template).read(), summary=document_summary)
            response = jsonify(summary=json.loads(json_output))
            response.status_code = 200  # Set status code to 200 (OK)
            return response
        else:
            response = jsonify({'error': 'Document no found'})
            response.status_code = 404  # Set status code to 200 (OK)
            return response
    else:
        response = jsonify({'error': 'Invalid request. Expected Content-Type: application/json'})
        response.status_code = 400  # Set status code to 200 (OK)
        return response