"""
Flask Application for Scientific Calculator
REST API Server with CORS support
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os


def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Configuration
    app.config['JSON_SORT_KEYS'] = False
    
    # Enable CORS (Cross-Origin Resource Sharing)
    # Allows requests from any origin (important for frontend)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register API blueprint
    from api import api
    app.register_blueprint(api)
    
    # Home endpoint
    @app.route('/', methods=['GET'])
    def home():
        """Home endpoint with API documentation"""
        return jsonify({
            'name': 'Modern Scientific Calculator API',
            'version': '1.0.0',
            'description': 'REST API for scientific calculator operations',
            'endpoints': {
                'health': 'GET /api/health',
                'calculate': 'POST /api/calculate',
                'history': 'GET /api/history',
                'history_search': 'GET /api/history/search',
                'history_clear': 'DELETE /api/history/clear',
                'memory': 'GET /api/memory',
                'memory_add': 'POST /api/memory/add',
                'memory_subtract': 'POST /api/memory/subtract',
                'memory_clear': 'DELETE /api/memory/clear',
                'config': 'GET /api/config',
                'config_decimal': 'PUT /api/config/decimal-places',
                'config_angle': 'PUT /api/config/angle-mode',
                'config_notation': 'PUT /api/config/notation'
            },
            'documentation': 'See README.md for detailed API documentation'
        }), 200
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 'Bad request',
            'status_code': 400
        }), 400
    
    return app


if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*60)
    print("Scientific Calculator API Server")
    print("="*60)
    print("\nStarting Flask server on http://localhost:5000")
    print("\nEndpoints available at:")
    print("  Health check: http://localhost:5000/api/health")
    print("  Documentation: http://localhost:5000/")
    print("\nPress Ctrl+C to stop the server\n")
    
    # Run on port 5000
    app.run(debug=False, host='0.0.0.0', port=5000)
