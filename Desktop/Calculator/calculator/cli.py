"""
Command Line Interface for the Scientific Calculator
Interactive REPL for terminal-based calculations
"""

import sys
from .arithmetic import Arithmetic
from .advanced import AdvancedMath
from .memory import Memory
from .parser import ExpressionParser
from .config import CalculatorConfig


class CalculatorCLI:
    """Command Line Interface for the calculator"""

    def __init__(self):
        """Initialize the calculator CLI"""
        self.arithmetic = Arithmetic()
        self.advanced = AdvancedMath()
        self.memory = Memory()
        self.parser = ExpressionParser()
        self.config = CalculatorConfig()
        self.running = True

    def print_welcome(self):
        """Print welcome message"""
        welcome = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║            MODERN SCIENTIFIC CALCULATOR v1.0                  ║
║                                                               ║
║  A comprehensive calculator for scientific computations       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

Type 'help' for available commands
Type 'quit' to exit

"""
        print(welcome)

    def print_help(self):
        """Print help menu"""
        help_text = """
╔═══════════════════════════════════════════════════════════════╗
║                      AVAILABLE COMMANDS                       ║
╚═══════════════════════════════════════════════════════════════╝

BASIC OPERATIONS:
  + (addition)          - a + b
  - (subtraction)       - a - b
  * (multiplication)    - a * b
  / (division)          - a / b
  % (modulo)            - a % b
  ^ (power)             - a ^ b or a ** b

ADVANCED FUNCTIONS:
  sqrt(x)               - Square root
  sin(x), cos(x), tan(x) - Trigonometric (angle mode dependent)
  asin(x), acos(x), atan(x) - Inverse trigonometric
  ln(x)                 - Natural logarithm
  log(x)                - Base-10 logarithm
  log2(x)               - Base-2 logarithm
  exp(x)                - e^x
  abs(x)                - Absolute value
  fact(x)               - Factorial

SPECIAL COMMANDS:
  history               - Show calculation history
  history [n]           - Show last n calculations
  clear_history         - Clear all history
  memory                - Show memory value
  m+                    - Add to memory (m+ [value])
  m-                    - Subtract from memory (m- [value])
  mc                    - Clear memory
  mr                    - Recall memory
  config                - Show configuration
  angle [mode]          - Set angle mode (degrees/radians)
  decimal [places]      - Set decimal places
  notation [type]       - Set notation (fixed/scientific)
  ans                   - Use previous result
  quit / exit           - Exit calculator

CONSTANTS:
  pi or π               - π (3.14159...)
  e                     - Euler's number (2.71828...)

EXAMPLES:
  >>> 5 + 3
  8.0
  
  >>> sin(45)
  0.7071067811865475
  
  >>> sqrt(16)
  4.0
  
  >>> 2 ** 8
  256.0
  
  >>> ans + 10
  266.0

╔═══════════════════════════════════════════════════════════════╗
"""
        print(help_text)

    def process_command(self, user_input):
        """
        Process user command
        
        Args:
            user_input: User's input string
            
        Returns:
            True to continue, False to quit
        """
        user_input = user_input.strip()
        
        if not user_input:
            return True
        
        # Handle special commands
        if user_input.lower() == 'help':
            self.print_help()
            return True
        
        if user_input.lower() in ['quit', 'exit']:
            self.running = False
            return False
        
        if user_input.lower() == 'history':
            print(self.memory.print_history())
            return True
        
        if user_input.lower().startswith('history '):
            try:
                limit = int(user_input.split()[1])
                history = self.memory.get_history(limit)
                if history:
                    print("\n" + "=" * 60)
                    print(f"LAST {limit} CALCULATIONS")
                    print("=" * 60)
                    for i, entry in enumerate(history, 1):
                        print(f"{i}. {entry['expression']} = {entry['result']}")
                    print("=" * 60 + "\n")
                else:
                    print("No history available")
            except ValueError:
                print("Invalid history limit. Use: history [number]")
            return True
        
        if user_input.lower() == 'clear_history':
            self.memory.clear_history()
            print("History cleared!")
            return True
        
        if user_input.lower() == 'memory':
            print(f"\nMemory value: {self.config.format_result(self.memory.memory_recall())}\n")
            return True
        
        if user_input.lower().startswith('m+ '):
            try:
                value = float(user_input[3:].strip())
                self.memory.memory_add(value)
                print(f"Added {value} to memory. Memory = {self.config.format_result(self.memory.memory_recall())}")
            except ValueError:
                print("Invalid value for M+. Usage: m+ [number]")
            return True
        
        if user_input.lower().startswith('m- '):
            try:
                value = float(user_input[3:].strip())
                self.memory.memory_subtract(value)
                print(f"Subtracted {value} from memory. Memory = {self.config.format_result(self.memory.memory_recall())}")
            except ValueError:
                print("Invalid value for M-. Usage: m- [number]")
            return True
        
        if user_input.lower() == 'mc':
            self.memory.memory_clear()
            print("Memory cleared!")
            return True
        
        if user_input.lower() == 'mr':
            value = self.memory.memory_recall()
            print(f"\nRecalled from memory: {self.config.format_result(value)}\n")
            return True
        
        if user_input.lower() == 'config':
            print(self.config.print_config())
            return True
        
        if user_input.lower().startswith('angle '):
            mode = user_input[6:].strip().lower()
            if mode in ['degrees', 'radians']:
                self.config.set_angle_mode(mode)
                self.parser.set_angle_mode(mode)
                self.advanced.set_angle_mode(mode)
                print(f"Angle mode set to: {mode}")
            else:
                print("Angle mode must be 'degrees' or 'radians'")
            return True
        
        if user_input.lower().startswith('decimal '):
            try:
                places = int(user_input[8:].strip())
                self.config.set_decimal_places(places)
                print(f"Decimal places set to: {places}")
            except ValueError:
                print("Invalid decimal places. Usage: decimal [number]")
            return True
        
        if user_input.lower().startswith('notation '):
            notation = user_input[9:].strip().lower()
            if notation in ['fixed', 'scientific']:
                self.config.set_notation(notation)
                print(f"Notation set to: {notation}")
            else:
                print("Notation must be 'fixed' or 'scientific'")
            return True
        
        # Handle mathematical expressions
        try:
            # Replace ^ with **
            expression = user_input.replace('^', '**')
            
            result = self.parser.evaluate(expression)
            
            # Store in memory
            self.memory.add_to_history(user_input, result)
            
            # Format and display result
            formatted_result = self.config.format_result(result)
            print(f"\n{formatted_result}\n")
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
        
        return True

    def run(self):
        """Run the calculator in interactive mode"""
        self.print_welcome()
        
        while self.running:
            try:
                user_input = input("calc> ").strip()
                self.process_command(user_input)
            except KeyboardInterrupt:
                print("\n\nCalculator closed. Goodbye!")
                self.running = False
            except EOFError:
                self.running = False

    def run_script(self, expressions):
        """
        Run calculator in script mode (non-interactive)
        
        Args:
            expressions: List of expressions to evaluate
        """
        for expr in expressions:
            print(f"calc> {expr}")
            self.process_command(expr)


def main():
    """Main entry point for the calculator"""
    calculator = CalculatorCLI()
    
    if len(sys.argv) > 1:
        # Script mode: pass expressions as arguments
        expressions = sys.argv[1:]
        calculator.run_script(expressions)
    else:
        # Interactive mode
        calculator.run()


if __name__ == '__main__':
    main()
