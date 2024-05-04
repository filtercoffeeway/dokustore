# DAO for User
import oracledb
from walletcredentials import uname, pwd, cdir, wltloc, wltpwd, dsn
from app.models.user import User
from app.db.extensions import db

class UserDAO:
    @staticmethod
    def get_user(user_id):
        with db.get_cursor() as cursor:
            sql = """SELECT  id
                            ,first_name
                            ,last_name 
                            ,email
                            ,phone
                            ,status 
                            ,username
                            ,created_at
                            ,updated_at
                            ,verified_at
                            ,deactivated_at
                        FROM users 
                        WHERE id = :user_id"""
            cursor.execute(sql, user_id=user_id)
            result = cursor.fetchone()
            
            if result:
                column_names = [description[0].lower() for description in cursor.description]
                user_data = dict(zip(column_names, result))
                return User(**user_data)
            else:
                return None


    @staticmethod
    def get_all_users():
        with db.get_cursor() as cursor:
            sql = """SELECT id
                            ,first_name
                            ,last_name 
                            ,email
                            ,phone
                            ,status 
                            ,username
                            ,created_at
                            ,updated_at
                            ,verified_at
                            ,deactivated_at
                        FROM users"""
            cursor.execute(sql)
            results = cursor.fetchall()

            column_names = [description[0].lower() for description in cursor.description]
            users = []

            for row in results:
                user_data = dict(zip(column_names, row))
                users.append(User(**user_data))

            return users
            

    @staticmethod
    def update_user(user_id, new_data):
        try:
            with db.get_cursor() as cursor:
                # Construct the UPDATE SQL statement
                sql = "UPDATE users SET "
                updates = []
                for key, value in new_data.items():
                    updates.append(f"{key} = :{key}")  # Using bind variables
                sql += ", ".join(updates)
                sql += " WHERE id = :user_id"

                # Execute the UPDATE SQL statement
                new_data['user_id'] = user_id
                cursor.execute(sql, new_data)
                
            return True, None  # Return True if update is successful
            
        except Exception as e:
            error_message = str(e)  # Get the error message
            return False, error_message  # Return False and error message
        

    @staticmethod
    def create_user(user_data):
        try:
            with db.get_cursor() as cursor:
                # Construct the INSERT SQL statement dynamically with RETURNING clause
                columns = ', '.join(user_data.keys())
                values_placeholder = ', '.join(f":{key}" for key in user_data)
                sql = f"INSERT INTO users ({columns}) VALUES ({values_placeholder}) RETURNING id INTO :new_id"
                
                # Execute the INSERT SQL statement
                new_id = cursor.var(oracledb.NUMBER)
                bind_vars = {**user_data, 'new_id': new_id}
                cursor.execute(sql, bind_vars)
                
                # Retrieve the new user ID
                user_id = int(new_id.getvalue()[0])
                
            return True, user_id, None  # Return True if creation is successful along with the new user ID
            
        except Exception as e:
            error_message = str(e)  # Get the error message
            return False, None, error_message  # Return False and error message
        
    
    @staticmethod
    def delete_user(user_id):
        try:
            with db.get_cursor() as cursor:
                # Construct the DELETE SQL statement
                sql = "DELETE FROM users WHERE id = :user_id"

                # Execute the DELETE SQL statement
                cursor.execute(sql, user_id=user_id)
                
            return True, None  # Return True if deletion is successful
            
        except Exception as e:
            error_message = str(e)  # Get the error message
            return False, error_message  # Return False and error message