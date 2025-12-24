"""
Memory module for calculator history and memory operations
Handles: M+, M-, MC, MR, and calculation history
"""

from collections import deque
from datetime import datetime


class Memory:
    """Memory and history management for the calculator"""

    def __init__(self, max_history=100):
        """
        Initialize memory system
        
        Args:
            max_history: Maximum number of history entries to keep (default: 100)
        """
        self.memory_value = 0
        self.history = deque(maxlen=max_history)
        self.max_history = max_history

    def memory_add(self, value):
        """
        Add value to memory (M+)
        
        Args:
            value: Numeric value to add to memory
        """
        try:
            self.memory_value += float(value)
        except (TypeError, ValueError):
            raise ValueError(f"Cannot add non-numeric value to memory: {value}")

    def memory_subtract(self, value):
        """
        Subtract value from memory (M-)
        
        Args:
            value: Numeric value to subtract from memory
        """
        try:
            self.memory_value -= float(value)
        except (TypeError, ValueError):
            raise ValueError(f"Cannot subtract non-numeric value from memory: {value}")

    def memory_clear(self):
        """Clear memory (MC)"""
        self.memory_value = 0

    def memory_recall(self):
        """
        Recall memory value (MR)
        
        Returns:
            Current memory value
        """
        return self.memory_value

    def memory_set(self, value):
        """
        Set memory to a specific value
        
        Args:
            value: Numeric value to set in memory
        """
        try:
            self.memory_value = float(value)
        except (TypeError, ValueError):
            raise ValueError(f"Cannot set non-numeric value in memory: {value}")

    def add_to_history(self, expression, result):
        """
        Add calculation to history
        
        Args:
            expression: The mathematical expression evaluated
            result: The result of the calculation
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry = {
            'expression': str(expression),
            'result': result,
            'timestamp': timestamp
        }
        self.history.append(history_entry)

    def get_history(self, limit=None):
        """
        Get calculation history
        
        Args:
            limit: Maximum number of entries to return (None for all)
            
        Returns:
            List of history entries
        """
        if limit is None:
            return list(self.history)
        return list(self.history)[-limit:]

    def get_history_by_expression(self, expression):
        """
        Find history entries by expression
        
        Args:
            expression: Expression to search for
            
        Returns:
            List of matching history entries
        """
        return [h for h in self.history if expression in h['expression']]

    def clear_history(self):
        """Clear all history"""
        self.history.clear()

    def get_last_result(self):
        """
        Get the last calculation result from history
        
        Returns:
            Last result or None if no history
        """
        if self.history:
            return self.history[-1]['result']
        return None

    def get_history_count(self):
        """
        Get number of entries in history
        
        Returns:
            Number of history entries
        """
        return len(self.history)

    def print_history(self):
        """Print formatted history"""
        if not self.history:
            return "History is empty"
        
        output = "\n" + "=" * 60 + "\n"
        output += "CALCULATION HISTORY\n"
        output += "=" * 60 + "\n"
        
        for i, entry in enumerate(self.history, 1):
            output += f"{i}. {entry['timestamp']}\n"
            output += f"   Expression: {entry['expression']}\n"
            output += f"   Result: {entry['result']}\n"
            output += "-" * 60 + "\n"
        
        return output
