"""
Configuration module for calculator settings
"""


class CalculatorConfig:
    """Configuration settings for the calculator"""

    def __init__(self):
        """Initialize default configuration"""
        self.decimal_places = 10
        self.angle_mode = 'degrees'  # 'degrees' or 'radians'
        self.notation = 'fixed'  # 'fixed' or 'scientific'
        self.max_history = 100
        self.show_timestamps = True

    def set_decimal_places(self, places):
        """
        Set decimal precision
        
        Args:
            places: Number of decimal places to display
        """
        if not isinstance(places, int) or places < 0:
            raise ValueError("Decimal places must be a non-negative integer")
        self.decimal_places = places

    def set_angle_mode(self, mode):
        """
        Set angle mode for trigonometric functions
        
        Args:
            mode: 'degrees' or 'radians'
        """
        if mode not in ['degrees', 'radians']:
            raise ValueError("Angle mode must be 'degrees' or 'radians'")
        self.angle_mode = mode

    def set_notation(self, notation):
        """
        Set number notation
        
        Args:
            notation: 'fixed' or 'scientific'
        """
        if notation not in ['fixed', 'scientific']:
            raise ValueError("Notation must be 'fixed' or 'scientific'")
        self.notation = notation

    def set_max_history(self, max_size):
        """
        Set maximum history size
        
        Args:
            max_size: Maximum number of history entries
        """
        if not isinstance(max_size, int) or max_size < 0:
            raise ValueError("Max history must be a non-negative integer")
        self.max_history = max_size

    def format_result(self, result):
        """
        Format result based on configuration
        
        Args:
            result: Numeric result to format
            
        Returns:
            Formatted result string
        """
        try:
            result = float(result)
            
            if self.notation == 'scientific':
                return f"{result:.{self.decimal_places}e}"
            else:
                # Fixed notation
                if result == int(result):
                    return str(int(result))
                return f"{result:.{self.decimal_places}f}".rstrip('0').rstrip('.')
        except (TypeError, ValueError):
            return str(result)

    def get_config(self):
        """Get all configuration settings"""
        return {
            'decimal_places': self.decimal_places,
            'angle_mode': self.angle_mode,
            'notation': self.notation,
            'max_history': self.max_history,
            'show_timestamps': self.show_timestamps
        }

    def print_config(self):
        """Print current configuration"""
        config = self.get_config()
        output = "\n" + "=" * 40 + "\n"
        output += "CALCULATOR CONFIGURATION\n"
        output += "=" * 40 + "\n"
        for key, value in config.items():
            output += f"{key}: {value}\n"
        output += "=" * 40 + "\n"
        return output
