from flask import Flask, g
from app.db.extensions import db
from walletcredentials import uname, pwd, cdir, wltloc, wltpwd, dsn

app = Flask(__name__)
db.init_app(app)

# registering routes
from app.routes.web.user import user_view
from app.routes.web.document_user import document_type_view
from app.routes.web.document import document_view

app.register_blueprint(user_view)
app.register_blueprint(document_type_view)
app.register_blueprint(document_view)

if __name__ == '__main__':
    app.run(debug=True)
