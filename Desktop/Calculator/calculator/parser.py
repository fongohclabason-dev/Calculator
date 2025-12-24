"""
Expression parser module for evaluating mathematical expressions
Handles: PEMDAS order of operations, parentheses, function calls
"""

import re
import math
from .arithmetic import Arithmetic
from .advanced import AdvancedMath


class ExpressionParser:
    """Parse and evaluate mathematical expressions with proper order of operations"""

    def __init__(self, angle_mode='degrees'):
        """
        Initialize parser with angle mode
        
        Args:
            angle_mode: 'degrees' or 'radians' (default: 'degrees')
        """
        self.arithmetic = Arithmetic()
        self.advanced = AdvancedMath(angle_mode)
        self.angle_mode = angle_mode
        self.last_result = 0

    def set_angle_mode(self, mode):
        """Set angle mode for trigonometric functions"""
        self.angle_mode = mode
        self.advanced.set_angle_mode(mode)

    def evaluate(self, expression):
        """
        Evaluate a mathematical expression
        
        Args:
            expression: Mathematical expression as string
            
        Returns:
            Result of evaluation
            
        Raises:
            ValueError: If expression is invalid
            SyntaxError: If expression has syntax errors
        """
        try:
            # Clean the expression
            expression = str(expression).strip()
            
            if not expression:
                raise ValueError("Empty expression")
            
            # Replace function calls FIRST before replacing constants
            expression = self._replace_functions(expression)
            
            # Replace 'ans' with last result
            expression = expression.replace('ans', str(self.last_result))
            
            # Replace mathematical constants
            expression = expression.replace('pi', str(math.pi))
            expression = expression.replace('π', str(math.pi))
            # Only replace 'e' if it's not part of a function name
            expression = re.sub(r'\be\b', str(math.e), expression)
            
            # Validate expression
            self._validate_expression(expression)
            
            # Create safe namespace with math functions and custom functions
            safe_dict = {
                'math': math,
                'abs': abs,
                'sin_deg': self.advanced.sine,
                'cos_deg': self.advanced.cosine,
                'tan_deg': self.advanced.tangent,
                'asin_deg': self.advanced.arcsine,
                'acos_deg': self.advanced.arccosine,
                'atan_deg': self.advanced.arctangent,
                '__builtins__': {}
            }
            
            # Evaluate using eval (safe after validation)
            result = eval(expression, safe_dict)
            
            self.last_result = result
            return result
            
        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero")
        except ValueError as e:
            raise ValueError(f"Invalid expression: {str(e)}")
        except SyntaxError as e:
            raise SyntaxError(f"Syntax error in expression: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {str(e)}")

    def _replace_functions(self, expression):
        """Replace function calls with Python equivalents"""
        
        # Process functions in order - longest first to avoid conflicts
        # Replace ln() before log() to avoid matching "ln" inside "log"
        functions = [
            ('ln', 'math.log'),
            ('log2', 'math.log2'),
            ('log', 'math.log10'),
            ('sqrt', 'math.sqrt'),
            ('sin', 'sin_deg'),
            ('cos', 'cos_deg'),
            ('tan', 'tan_deg'),
            ('asin', 'asin_deg'),
            ('acos', 'acos_deg'),
            ('atan', 'atan_deg'),
            ('exp', 'math.exp'),
            ('abs', 'abs'),
            ('fact', 'math.factorial'),
        ]
        
        for func_name, replacement in functions:
            # Match function call pattern: function( 
            # Use negative lookbehind to ensure it's not already preceded by "math."
            pattern = rf'(?<!\.)\b{func_name}\s*\('
            expression = re.sub(pattern, f'{replacement}(', expression)
        
        return expression

    def _validate_expression(self, expression):
        """
        Validate expression for safety and correctness
        
        Args:
            expression: Expression to validate
            
        Raises:
            ValueError: If expression is invalid
        """
        # Check for balanced parentheses
        if expression.count('(') != expression.count(')'):
            raise ValueError("Unbalanced parentheses")
        
        # Check for balanced brackets
        if expression.count('[') != expression.count(']'):
            raise ValueError("Unbalanced brackets")
        
        # Check for valid characters
        valid_chars = set('0123456789+-*/%().^,. ')
        valid_chars.update('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_')
        
        for char in expression:
            if char not in valid_chars:
                raise ValueError(f"Invalid character: '{char}'")
        
        # Check for consecutive operators (but allow -- for negative numbers)
        if re.search(r'[+\-%/]{2,}', expression):
            raise ValueError("Invalid consecutive operators")
        
        # Check for ** (exponentiation) - this is valid
        # Just ensure it's not used incorrectly
        if '**' in expression:
            parts = expression.split('**')
            if len(parts) > 1 and (not parts[-1].strip() or parts[-1].strip()[0] in '+-%/*'):
                raise ValueError("Invalid exponentiation syntax")

    def validate_only(self, expression):
        """
        Validate an expression without evaluating it
        
        Args:
            expression: Expression to validate
            
        Returns:
            True if valid, raises exception if invalid
        """
        try:
            expression = str(expression).strip()
            self._validate_expression(expression)
            return True
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")

    def get_last_result(self):
        """Get the last calculation result"""
        return self.last_result

    def reset(self):
        """Reset parser state"""
        self.last_result = 0

