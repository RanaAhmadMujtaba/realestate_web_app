from flask import Flask
from config import Config
from extensions import mysql
from controllers.property_controller import property_blueprint
from errors import errors



app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(errors)
mysql.init_app(app)

# Register Blueprints
app.register_blueprint(property_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
