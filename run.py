from flask import Flask, jsonify
from app.daos.user import UserDAO

app = Flask(__name__)

# registering routes
from app.routes.web.user import user_view
from app.routes.web.document_user import document_type_view
from app.routes.web.document import document_view


app.register_blueprint(user_view)
app.register_blueprint(document_type_view)
app.register_blueprint(document_view)

if __name__ == '__main__':
    app.run(debug=True)
