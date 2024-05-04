# DAO for User
import oracledb
from walletcredentials import uname, pwd, cdir, wltloc, wltpwd, dsn
from app.models.document_type import DocumentType
from app.db.extensions import db

class DocumentTypeDao:
    @staticmethod
    def get_document_type(document_type_id):
        with db.get_cursor() as cursor:
            sql = """SELECT  id
                            ,document_type
                            ,user_id
                            ,status
                            ,created_at
                            ,updated_at
                        FROM document_types 
                        WHERE id = :document_type_id"""
            cursor.execute(sql, document_type_id=document_type_id)
            result = cursor.fetchone()
            
            if result:
                column_names = [description[0].lower() for description in cursor.description]
                document_type_data = dict(zip(column_names, result))
                return DocumentType(**document_type_data)
            else:
                return None


    @staticmethod
    def get_all_document_types(user_id, document_type=None, offset=0, limit=None, sort_field='document_type', sort_direction='asc'):
        with db.get_cursor() as cursor:
            sql = """SELECT id
                            ,document_type
                            ,user_id
                            ,status
                            ,created_at
                            ,updated_at
                        FROM document_types
                        WHERE user_id = :user_id"""  # Placeholder for user_id
            
            bind_vars = {'user_id': user_id}  # Bind variables dictionary
            
            if document_type is not None:
                # If document_type is provided, add a condition to filter by document_type
                sql += " AND UPPER(document_type) LIKE '%' || UPPER(:document_type) || '%'"
                bind_vars['document_type'] = document_type  # Add document_type to bind variables

            # Add sorting
            if sort_field == 'document_type':
                sql += f" ORDER BY LOWER({sort_field}) {sort_direction.upper()}"
            else:
                sql += f" ORDER BY {sort_field} {sort_direction.upper()}"

            # Add pagination
            if limit is not None:
                sql += " OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY"
                bind_vars['offset'] = offset
                bind_vars['limit'] = limit

            cursor.execute(sql, bind_vars)  # Pass bind variables to execute method
            results = cursor.fetchall()
            records_count = len(results)

            column_names = [description[0].lower() for description in cursor.description]
            document_types = []

            for row in results:
                document_type_data = dict(zip(column_names, row))
                document_types.append(DocumentType(**document_type_data))

            # Calculate page_no
            page_no = offset // limit + 1 if limit else 1

            response_data = {
                'page_no': page_no,
                'page_size': limit,
                'records_count': records_count,
                'document_types': document_types
            }

            return response_data
        
            
    @staticmethod
    def update_document_type(document_type_id, new_data):
        try:
            with db.get_cursor() as cursor:
                # Construct the UPDATE SQL statement
                sql = "UPDATE document_types SET "
                updates = []
                for key, value in new_data.items():
                    updates.append(f"{key} = :{key}")  # Using bind variables
                sql += ", ".join(updates)
                sql += " WHERE id = :document_type_id"

                # Execute the UPDATE SQL statement
                new_data['document_type_id'] = document_type_id
                cursor.execute(sql, new_data)

            return True, None  # Return True if update is successful
            
        except Exception as e:
            error_message = str(e)  # Get the error message
            return False, error_message  # Return False and error message
        

    @staticmethod
    def create_document_type(document_type_data):
        try:
            with db.get_cursor() as cursor:
                # Construct the INSERT SQL statement dynamically with RETURNING clause
                columns = ', '.join(document_type_data.keys())
                values_placeholder = ', '.join(f":{key}" for key in document_type_data)
                sql = f"INSERT INTO document_types ({columns}) VALUES ({values_placeholder}) RETURNING id INTO :new_id"
                
                # Execute the INSERT SQL statement
                new_id = cursor.var(oracledb.NUMBER)
                bind_vars = {**document_type_data, 'new_id': new_id}
                cursor.execute(sql, bind_vars)
                
                # Retrieve the new document type ID
                document_type_id = int(new_id.getvalue()[0])
                
            return True, document_type_id, None  # Return True if creation is successful along with the new document type ID
            
        except Exception as e:
            error_message = str(e)  # Get the error message
            return False, None, error_message  # Return False and error message
        
    
    @staticmethod
    def delete_document_type(document_type_id):
        try:
            with db.get_cursor() as cursor:
                # Construct the DELETE SQL statement
                sql = "DELETE FROM document_types WHERE id = :document_type_id"

                # Execute the DELETE SQL statement
                cursor.execute(sql, document_type_id=document_type_id)
                
            return True, None  # Return True if deletion is successful
            
        except Exception as e:
            error_message = str(e)  # Get the error message
            return False, error_message  # Return False and error message