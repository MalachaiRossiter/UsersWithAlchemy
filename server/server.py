from flask_app import app
from flask_app.routes import user
from flask_app.routes import address

if __name__ == "__main__":
    app.run(debug=True)