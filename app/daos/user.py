# DAO for User
import oracledb
from walletcredentials import uname, pwd, cdir, wltloc, wltpwd, dsn
from app.models.user import User

class UserDAO:
    @staticmethod
    def get_user(user_id):
        with oracledb.connect(user=uname, password=pwd, dsn=dsn, config_dir=cdir, wallet_location=wltloc, wallet_password=wltpwd) as connection:
            with connection.cursor() as cursor:
                sql = """SELECT id, first_name FROM users WHERE id = :user_id"""
                cursor.execute(sql, user_id=user_id)
                result = cursor.fetchone()
                
                if result:
                    return User(result[0], result[1])
                else:
                    return None
