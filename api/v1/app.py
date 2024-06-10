#!/usr/bin/python3
"""
    Flask application
"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.url_map.strict_slashes = False
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_storage(exc):
    """ Close the storage engine """
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """ Handle 404 errors with a JSON response """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
