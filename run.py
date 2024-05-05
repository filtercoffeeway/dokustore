from flask import Flask, g
from app.db.extensions import db
from walletcredentials import uname, pwd, cdir, wltloc, wltpwd, dsn

app = Flask(__name__)
db.init_app(app)
app.config['SECRET_KEY'] = 'ac8fa875-146d-4567-b1cb-0da6aaaa9963'

# registering routes
from app.routes.web.user import user_view
from app.routes.web.document_user import document_type_view
from app.routes.web.document import document_view
from app.routes.web.account import account_view

app.register_blueprint(user_view)
app.register_blueprint(document_type_view)
app.register_blueprint(document_view)
app.register_blueprint(account_view)

if __name__ == '__main__':
    app.run(debug=True)
