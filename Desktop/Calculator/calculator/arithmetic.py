"""
Arithmetic module for basic mathematical operations
Handles: addition, subtraction, multiplication, division
"""


class Arithmetic:
    """Basic arithmetic operations for the calculator"""

    @staticmethod
    def add(a, b):
        """
        Add two numbers
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Sum of a and b
        """
        return a + b

    @staticmethod
    def subtract(a, b):
        """
        Subtract two numbers
        
        Args:
            a: First number (minuend)
            b: Second number (subtrahend)
            
        Returns:
            Difference of a and b
        """
        return a - b

    @staticmethod
    def multiply(a, b):
        """
        Multiply two numbers
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Product of a and b
        """
        return a * b

    @staticmethod
    def divide(a, b):
        """
        Divide two numbers with zero-division handling
        
        Args:
            a: Numerator
            b: Denominator
            
        Returns:
            Quotient of a divided by b
            
        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    @staticmethod
    def modulo(a, b):
        """
        Calculate remainder of division
        
        Args:
            a: Dividend
            b: Divisor
            
        Returns:
            Remainder of a divided by b
            
        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Cannot perform modulo with zero")
        return a % b

    @staticmethod
    def power(a, b):
        """
        Raise a number to a power
        
        Args:
            a: Base
            b: Exponent
            
        Returns:
            a raised to the power of b
        """
        return a ** b
