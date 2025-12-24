"""
API Routes for Scientific Calculator
All endpoints handle JSON requests and responses
"""

from flask import request, jsonify
from . import api
from calculator.parser import ExpressionParser
from calculator.memory import Memory
from calculator.config import CalculatorConfig


# Global instances (shared across requests)
parser = ExpressionParser()
memory = Memory()
config = CalculatorConfig()


@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API is running"""
    return jsonify({
        'status': 'healthy',
        'message': 'Scientific Calculator API is running',
        'version': '1.0.0'
    }), 200


@api.route('/calculate', methods=['POST'])
def calculate():
    """
    Calculate a mathematical expression
    
    Request JSON:
    {
        "expression": "2 + 3 * 4"
    }
    
    Response:
    {
        "result": 14.0,
        "expression": "2 + 3 * 4",
        "success": true
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'expression' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: expression'
            }), 400
        
        expression = str(data['expression']).strip()
        
        if not expression:
            return jsonify({
                'success': False,
                'error': 'Expression cannot be empty'
            }), 400
        
        # Evaluate expression
        result = parser.evaluate(expression)
        
        # Format result according to config
        formatted_result = config.format_result(result)
        
        # Store in memory
        memory.add_to_history(expression, result)
        
        return jsonify({
            'success': True,
            'expression': expression,
            'result': result,
            'formatted_result': formatted_result
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 422
    except SyntaxError as e:
        return jsonify({
            'success': False,
            'error': f'Syntax error: {str(e)}'
        }), 422
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@api.route('/history', methods=['GET'])
def get_history():
    """
    Get calculation history
    
    Query Parameters:
    - limit: Maximum number of entries to return (optional)
    
    Response:
    {
        "success": true,
        "count": 3,
        "history": [
            {
                "expression": "2 + 3",
                "result": 5.0,
                "timestamp": "2025-12-24 10:30:45"
            },
            ...
        ]
    }
    """
    try:
        limit = request.args.get('limit', type=int)
        history = memory.get_history(limit=limit)
        
        return jsonify({
            'success': True,
            'count': len(history),
            'history': history
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/history/clear', methods=['DELETE'])
def clear_history():
    """
    Clear all calculation history
    
    Response:
    {
        "success": true,
        "message": "History cleared"
    }
    """
    try:
        memory.clear_history()
        return jsonify({
            'success': True,
            'message': 'History cleared successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/history/search', methods=['GET'])
def search_history():
    """
    Search history by expression
    
    Query Parameters:
    - query: Expression to search for (required)
    
    Response:
    {
        "success": true,
        "query": "sin",
        "results": [
            {
                "expression": "sin(45)",
                "result": 0.707...,
                "timestamp": "..."
            }
        ]
    }
    """
    try:
        query = request.args.get('query')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Missing required parameter: query'
            }), 400
        
        results = memory.get_history_by_expression(query)
        
        return jsonify({
            'success': True,
            'query': query,
            'count': len(results),
            'results': results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/memory', methods=['GET'])
def get_memory():
    """
    Get current memory value
    
    Response:
    {
        "success": true,
        "memory_value": 45.0,
        "formatted_value": "45"
    }
    """
    try:
        memory_value = memory.memory_recall()
        formatted = config.format_result(memory_value)
        
        return jsonify({
            'success': True,
            'memory_value': memory_value,
            'formatted_value': formatted
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/memory/add', methods=['POST'])
def memory_add():
    """
    Add value to memory (M+)
    
    Request JSON:
    {
        "value": 10.5
    }
    
    Response:
    {
        "success": true,
        "memory_value": 55.5,
        "operation": "add"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'value' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: value'
            }), 400
        
        try:
            value = float(data['value'])
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'Value must be a number'
            }), 422
        
        memory.memory_add(value)
        new_memory = memory.memory_recall()
        
        return jsonify({
            'success': True,
            'operation': 'add',
            'value': value,
            'memory_value': new_memory,
            'formatted_value': config.format_result(new_memory)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/memory/subtract', methods=['POST'])
def memory_subtract():
    """
    Subtract value from memory (M-)
    
    Request JSON:
    {
        "value": 5.0
    }
    
    Response:
    {
        "success": true,
        "memory_value": 50.5,
        "operation": "subtract"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'value' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: value'
            }), 400
        
        try:
            value = float(data['value'])
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'Value must be a number'
            }), 422
        
        memory.memory_subtract(value)
        new_memory = memory.memory_recall()
        
        return jsonify({
            'success': True,
            'operation': 'subtract',
            'value': value,
            'memory_value': new_memory,
            'formatted_value': config.format_result(new_memory)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/memory/clear', methods=['DELETE'])
def memory_clear():
    """
    Clear memory (MC)
    
    Response:
    {
        "success": true,
        "memory_value": 0,
        "message": "Memory cleared"
    }
    """
    try:
        memory.memory_clear()
        
        return jsonify({
            'success': True,
            'memory_value': 0,
            'message': 'Memory cleared successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/config', methods=['GET'])
def get_config():
    """
    Get current configuration
    
    Response:
    {
        "success": true,
        "config": {
            "decimal_places": 10,
            "angle_mode": "degrees",
            "notation": "fixed",
            "max_history": 100,
            "show_timestamps": true
        }
    }
    """
    try:
        cfg = config.get_config()
        
        return jsonify({
            'success': True,
            'config': cfg
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/config/decimal-places', methods=['PUT'])
def set_decimal_places():
    """
    Set decimal places precision
    
    Request JSON:
    {
        "decimal_places": 5
    }
    
    Response:
    {
        "success": true,
        "decimal_places": 5,
        "message": "Decimal places updated"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'decimal_places' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: decimal_places'
            }), 400
        
        try:
            places = int(data['decimal_places'])
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'decimal_places must be an integer'
            }), 422
        
        config.set_decimal_places(places)
        
        return jsonify({
            'success': True,
            'decimal_places': places,
            'message': 'Decimal places updated successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 422
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/config/angle-mode', methods=['PUT'])
def set_angle_mode():
    """
    Set angle mode (degrees or radians)
    
    Request JSON:
    {
        "angle_mode": "radians"
    }
    
    Response:
    {
        "success": true,
        "angle_mode": "radians",
        "message": "Angle mode updated"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'angle_mode' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: angle_mode'
            }), 400
        
        mode = data['angle_mode']
        
        config.set_angle_mode(mode)
        parser.set_angle_mode(mode)
        
        return jsonify({
            'success': True,
            'angle_mode': mode,
            'message': 'Angle mode updated successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 422
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/config/notation', methods=['PUT'])
def set_notation():
    """
    Set number notation (fixed or scientific)
    
    Request JSON:
    {
        "notation": "scientific"
    }
    
    Response:
    {
        "success": true,
        "notation": "scientific",
        "message": "Notation updated"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'notation' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: notation'
            }), 400
        
        notation = data['notation']
        
        config.set_notation(notation)
        
        return jsonify({
            'success': True,
            'notation': notation,
            'message': 'Notation updated successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 422
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'status_code': 404
    }), 404


@api.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'success': False,
        'error': 'Method not allowed',
        'status_code': 405
    }), 405


@api.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'status_code': 500
    }), 500
