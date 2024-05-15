from flask import Flask, request, jsonify, url_for, redirect, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Static services data
services = [
    {'id': '1', 'name': 'Service One'},
    {'id': '2', 'name': 'Service Two'},
    {'id': '3', 'name': 'Service Three'},
    {'id': '4', 'name': 'Service Four'}
]

active_services = []

@app.route('/service', methods=['GET'])
def get_services():
    """Fetch a list of all available services."""
    return jsonify(services), 200

@app.route('/service/active', methods=['GET'])
def get_active_services():
    """Fetch a list of services that are currently active."""
    return jsonify(active_services), 200

@app.route('/service/activate', methods=['POST'])
def activate_service():
    """Activate a specific service for a customer."""
    service_id = request.json.get('service_id')
    for service in services:
        if service['id'] == service_id:
            active_services.append(service)
            return jsonify({'message': 'Service activated successfully'}), 200
    return jsonify({'message': 'Service not found'}), 404

@app.route('/service/deactivate', methods=['DELETE'])
def deactivate_service():
    """Deactivate a specific service for a customer."""
    service_id = request.json.get('service_id')
    for service in active_services:
        if service['id'] == service_id:
            active_services.remove(service)
            return jsonify({'message': 'Service deactivated successfully'}), 200
    return jsonify({'message': 'Service not found'}), 404


# Swagger UI setup
SWAGGER_URL = '/swagger'
API_URL = '/swagger.yaml'  # Path to the Swagger JSON file

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Service Management API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def index():
    return redirect(url_for('swagger_ui.show'))


@app.route('/swagger.yaml')
def swagger_file():
    return send_from_directory(".", "swagger.yaml")

if __name__ == '__main__':
    app.run(debug=True)
