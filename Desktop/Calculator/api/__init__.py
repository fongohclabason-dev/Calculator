"""
API Blueprint for Scientific Calculator
"""

from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

from . import routes
