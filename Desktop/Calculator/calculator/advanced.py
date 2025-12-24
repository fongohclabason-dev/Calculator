"""
Advanced mathematics module for scientific operations
Handles: trigonometric, logarithmic, factorial, combinatorics functions
"""

import math


class AdvancedMath:
    """Advanced mathematical operations for scientific calculations"""

    def __init__(self, angle_mode='degrees'):
        """
        Initialize AdvancedMath with angle mode setting
        
        Args:
            angle_mode: 'degrees' or 'radians' (default: 'degrees')
        """
        if angle_mode not in ['degrees', 'radians']:
            raise ValueError("Angle mode must be 'degrees' or 'radians'")
        self.angle_mode = angle_mode

    def _to_radians(self, angle):
        """Convert angle to radians based on current mode"""
        if self.angle_mode == 'degrees':
            return math.radians(angle)
        return angle

    def _from_radians(self, angle):
        """Convert angle from radians to current mode"""
        if self.angle_mode == 'degrees':
            return math.degrees(angle)
        return angle

    def set_angle_mode(self, mode):
        """
        Set the angle mode for trigonometric functions
        
        Args:
            mode: 'degrees' or 'radians'
        """
        if mode not in ['degrees', 'radians']:
            raise ValueError("Angle mode must be 'degrees' or 'radians'")
        self.angle_mode = mode

    def square_root(self, x):
        """
        Calculate square root
        
        Args:
            x: Non-negative number
            
        Returns:
            Square root of x
            
        Raises:
            ValueError: If x is negative
        """
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(x)

    def nth_root(self, x, n):
        """
        Calculate nth root
        
        Args:
            x: Number to find root of
            n: Root degree
            
        Returns:
            Nth root of x
        """
        if n == 0:
            raise ValueError("Root degree cannot be zero")
        if x < 0 and n % 2 == 0:
            raise ValueError(f"Cannot calculate {n}th root of negative number")
        
        if x < 0:
            return -abs(x) ** (1 / n)
        return x ** (1 / n)

    def sine(self, angle):
        """
        Calculate sine of angle
        
        Args:
            angle: Angle in current mode (degrees/radians)
            
        Returns:
            Sine of angle
        """
        return math.sin(self._to_radians(angle))

    def cosine(self, angle):
        """
        Calculate cosine of angle
        
        Args:
            angle: Angle in current mode (degrees/radians)
            
        Returns:
            Cosine of angle
        """
        return math.cos(self._to_radians(angle))

    def tangent(self, angle):
        """
        Calculate tangent of angle
        
        Args:
            angle: Angle in current mode (degrees/radians)
            
        Returns:
            Tangent of angle
        """
        rad_angle = self._to_radians(angle)
        return math.tan(rad_angle)

    def arcsine(self, x):
        """
        Calculate inverse sine (arcsin)
        
        Args:
            x: Value between -1 and 1
            
        Returns:
            Angle in current mode (degrees/radians)
            
        Raises:
            ValueError: If x is outside [-1, 1]
        """
        if x < -1 or x > 1:
            raise ValueError("Arcsine input must be between -1 and 1")
        return self._from_radians(math.asin(x))

    def arccosine(self, x):
        """
        Calculate inverse cosine (arccos)
        
        Args:
            x: Value between -1 and 1
            
        Returns:
            Angle in current mode (degrees/radians)
            
        Raises:
            ValueError: If x is outside [-1, 1]
        """
        if x < -1 or x > 1:
            raise ValueError("Arccosine input must be between -1 and 1")
        return self._from_radians(math.acos(x))

    def arctangent(self, x):
        """
        Calculate inverse tangent (arctan)
        
        Args:
            x: Any real number
            
        Returns:
            Angle in current mode (degrees/radians)
        """
        return self._from_radians(math.atan(x))

    def logarithm(self, x, base=10):
        """
        Calculate logarithm with specified base
        
        Args:
            x: Positive number
            base: Base of logarithm (default: 10)
            
        Returns:
            Logarithm of x in specified base
            
        Raises:
            ValueError: If x <= 0 or base <= 0
        """
        if x <= 0:
            raise ValueError("Logarithm input must be positive")
        if base <= 0:
            raise ValueError("Logarithm base must be positive")
        if base == 1:
            raise ValueError("Logarithm base cannot be 1")
        
        return math.log(x, base)

    def natural_log(self, x):
        """
        Calculate natural logarithm (ln)
        
        Args:
            x: Positive number
            
        Returns:
            Natural logarithm of x
            
        Raises:
            ValueError: If x <= 0
        """
        if x <= 0:
            raise ValueError("Logarithm input must be positive")
        return math.log(x)

    def log10(self, x):
        """
        Calculate base-10 logarithm
        
        Args:
            x: Positive number
            
        Returns:
            Base-10 logarithm of x
            
        Raises:
            ValueError: If x <= 0
        """
        if x <= 0:
            raise ValueError("Logarithm input must be positive")
        return math.log10(x)

    def log2(self, x):
        """
        Calculate base-2 logarithm
        
        Args:
            x: Positive number
            
        Returns:
            Base-2 logarithm of x
            
        Raises:
            ValueError: If x <= 0
        """
        if x <= 0:
            raise ValueError("Logarithm input must be positive")
        return math.log2(x)

    def exponential(self, x):
        """
        Calculate e raised to power x
        
        Args:
            x: Any real number
            
        Returns:
            e^x
        """
        return math.exp(x)

    def factorial(self, n):
        """
        Calculate factorial of n
        
        Args:
            n: Non-negative integer
            
        Returns:
            n! (n factorial)
            
        Raises:
            ValueError: If n is negative or not an integer
        """
        if not isinstance(n, int) or n < 0:
            raise ValueError("Factorial input must be a non-negative integer")
        return math.factorial(n)

    def permutation(self, n, r):
        """
        Calculate permutations P(n, r) = n! / (n-r)!
        
        Args:
            n: Total items
            r: Items to arrange
            
        Returns:
            Number of permutations
            
        Raises:
            ValueError: If inputs are invalid
        """
        if not isinstance(n, int) or not isinstance(r, int):
            raise ValueError("Permutation inputs must be integers")
        if n < 0 or r < 0 or r > n:
            raise ValueError("Invalid permutation parameters")
        
        return math.factorial(n) // math.factorial(n - r)

    def combination(self, n, r):
        """
        Calculate combinations C(n, r) = n! / (r! * (n-r)!)
        
        Args:
            n: Total items
            r: Items to choose
            
        Returns:
            Number of combinations
            
        Raises:
            ValueError: If inputs are invalid
        """
        if not isinstance(n, int) or not isinstance(r, int):
            raise ValueError("Combination inputs must be integers")
        if n < 0 or r < 0 or r > n:
            raise ValueError("Invalid combination parameters")
        
        return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

    def absolute_value(self, x):
        """
        Calculate absolute value
        
        Args:
            x: Any real number
            
        Returns:
            Absolute value of x
        """
        return abs(x)

    def degrees_to_radians(self, degrees):
        """Convert degrees to radians"""
        return math.radians(degrees)

    def radians_to_degrees(self, radians):
        """Convert radians to degrees"""
        return math.degrees(radians)
