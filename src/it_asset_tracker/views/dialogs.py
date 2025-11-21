from typing import Dict
from src.it_asset_tracker.views.console_io import IInputProvider, IOutputDisplay

class SchemaBuilderDialog:
    """
    Handles the specific logic of defining a table schema.
    """
    
    def __init__(self, input_provider: IInputProvider, output_display: IOutputDisplay):
        self.input = input_provider
        self.output = output_display

    def run(self) -> Dict[str, str]:
        self.output.display("\n--- Define Your Table Columns ---")
        self.output.display("Note: An 'id' column is created automatically.")
        
        columns = {}
        while True:
            self.output.display("-" * 20)
            col_name = self.input.get_input("Enter column name (or 'done'): ").strip()
            
            if col_name.lower() == 'done':
                if not columns:
                    self.output.display("You must define at least one column!")
                    continue
                break
            
            if not col_name: continue
            
            sql_type = self._get_type_selection(col_name)
            columns[col_name] = sql_type
            self.output.display(f"Added: {col_name} ({sql_type})")
            
        return columns

    def _get_type_selection(self, col_name: str) -> str:
        self.output.display(
            f"Select type for '{col_name}':\n"
            "1. Text\n"
            "2. Integer\n"
            "3. Real"
        )        
        choice = self.input.get_input("Choice: ")
        if choice == '2': return "INTEGER"
        if choice == '3': return "REAL"
        return "TEXT"