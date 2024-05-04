# DAO for User
import oracledb
from walletcredentials import uname, pwd, cdir, wltloc, wltpwd, dsn
from app.models.document import Document, DocumentSummary
from app.db.extensions import db

class DocumentDao:
    @staticmethod
    def get_document(document_id):
        with db.get_cursor() as cursor:
            sql = """SELECT  id
                            ,document_name
                            ,status
                            ,document_type_id
                            ,user_id
                            ,file_id
                            ,file_path
                            ,file_size
                            ,file_type
                            ,due_date
                            ,created_at
                            ,updated_at
                        FROM documents 
                        WHERE id = :document_id"""
            cursor.execute(sql, document_id=document_id)
            result = cursor.fetchone()
            
            if result:
                column_names = [description[0].lower() for description in cursor.description]
                document_data = dict(zip(column_names, result))
                return Document(**document_data)
            else:
                return None


    @staticmethod
    def get_all_documents(user_id, document_type_id=None, document_name=None, offset=0, limit=None, sort_field='document_name', sort_direction='asc'):
        with db.get_cursor() as cursor:
            sql = """SELECT id
                            ,document_name
                            ,status
                            ,document_type_id
                            ,user_id
                            ,file_id
                            ,file_path
                            ,file_size
                            ,file_type
                            ,due_date
                            ,created_at
                            ,updated_at
                        FROM documents
                        WHERE status = 'active'
                            AND user_id = :user_id"""  # Placeholder for user_id
            
            bind_vars = {'user_id': user_id}
            if document_type_id is not None:
                # If document_type_id is provided, add a condition to filter by document_type_id
                sql += " AND document_type_id = :document_type_id "
                bind_vars['document_type_id'] = document_type_id  # Add document_type to bind variables
            
            if document_name is not None:
                # If document_name is provided, add a condition to filter by document_name
                sql += " AND UPPER(document_name) LIKE '%' || UPPER(:document_name) || '%'"
                bind_vars['document_name'] = document_name  # Add document_type to bind variables

            # Add sorting
            if sort_field == 'document_name':
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
            documents = []

            for row in results:
                document_data = dict(zip(column_names, row))
                documents.append(Document(**document_data))

            # Calculate page_no
            page_no = offset // limit + 1 if limit else 1

            response_data = {
                'page_no': page_no,
                'page_size': limit,
                'records_count': records_count,
                'documents': documents
            }

            return response_data
        
            
    @staticmethod
    def update_document(document_id, new_data):
        try:
            with db.get_cursor() as cursor:
                # Construct the UPDATE SQL statement
                sql = "UPDATE documents SET "
                updates = []
                for key, value in new_data.items():
                    updates.append(f"{key} = :{key}")  # Using bind variables
                sql += ", ".join(updates)
                sql += " WHERE id = :document_id"

                # Execute the UPDATE SQL statement
                new_data['document_id'] = document_id
                cursor.execute(sql, new_data)
                
            return True, None  # Return True if update is successful
            
        except Exception as e:
            error_message = str(e)  # Get the error message
            return False, error_message  # Return False and error message
        

    @staticmethod
    def create_document(document_data):
        try:
            with db.get_cursor() as cursor:
                # Construct the INSERT SQL statement dynamically with RETURNING clause
                columns = ', '.join(document_data.keys())
                values_placeholder = ', '.join(f":{key}" for key in document_data)
                sql = f"INSERT INTO documents ({columns}) VALUES ({values_placeholder}) RETURNING id INTO :new_id"
                
                # Execute the INSERT SQL statement
                new_id = cursor.var(oracledb.NUMBER)
                bind_vars = {**document_data, 'new_id': new_id}
                cursor.execute(sql, bind_vars)
                
                # Retrieve the new document ID
                document_id = int(new_id.getvalue()[0])
                
            return True, document_id, None  # Return True if creation is successful along with the new document ID
            
        except Exception as e:
            error_message = str(e)  # Get the error message
            return False, None, error_message  # Return False and error message
        
    
    @staticmethod
    def delete_document(document_id):
        try:
            with db.get_cursor() as cursor:
                # Construct the DELETE SQL statement
                sql = "DELETE FROM documents WHERE id = :document_id"

                # Execute the DELETE SQL statement
                cursor.execute(sql, document_id=document_id)
                
            return True, None  # Return True if deletion is successful
            
        except Exception as e:
            error_message = str(e)  # Get the error message
            return False, error_message  # Return False and error message
        
    
    @staticmethod
    def get_document_summary(user_id):
        with db.get_cursor() as cursor:
            sql = """
                        SELECT  COUNT(*) AS total_documents,
                                NVL(SUM(file_size), 0) AS total_file_size,
                                SUM(CASE WHEN due_date < SYSDATE THEN 1 ELSE 0 END) AS documents_past_due
                        FROM documents
                    WHERE user_id = :user_id"""
            cursor.execute(sql, user_id=user_id)
            result = cursor.fetchone()
            
            if result:
                column_names = [description[0].lower() for description in cursor.description]
                documents_summary = dict(zip(column_names, result))
                return DocumentSummary(**documents_summary)
            else:
                return None