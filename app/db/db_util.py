
from contextlib import contextmanager
import oracledb
from walletcredentials import uname, pwd, cdir, wltloc, wltpwd, dsn

class OracleDB:
    def __init__(self):
        self.app = None
        self.pool = None

    def init_app(self, app):
        self.app = app
        self.connect()

    def connect(self):
        self.pool = oracledb.create_pool(user=uname
                            ,password=pwd
                            ,dsn=dsn
                            ,config_dir=cdir
                            ,wallet_location=wltloc
                            ,wallet_password=wltpwd
                            ,min=1
                            ,max=5
                            ,increment=1
                            )
        return self.pool

    @contextmanager
    def get_cursor(self):
        if self.pool is None:
            self.connect()
        con = self.pool.acquire()
        try:
            yield con.cursor()
            con.commit()
        finally:
            con.close()