from typing import List, Dict
from src.it_asset_tracker.views.console_io import ConsoleIO
from src.it_asset_tracker.views.renderers import TableRenderer, MenuRenderer
from src.it_asset_tracker.views.dialogs import SchemaBuilderDialog
from src.it_asset_tracker.interfaces.cli_view_interface import IView
from src.it_asset_tracker.views.console_io import IInputProvider, IOutputDisplay

class CLIView(IView):
    def __init__(self, input_provider: IInputProvider, 
                output_display: IOutputDisplay, 
                table_renderer: TableRenderer, 
                menu_renderer: MenuRenderer):
        self.input = input_provider
        self.output = output_display
        self.table_renderer = table_renderer
        self.menu_renderer = menu_renderer

    def show_message(self, message: str):
        self.output.display(f"\n[INFO] {message}")
        self.input.get_input("Press Enter to continue...")

    def show_error(self, message: str):
        self.output.display(f"\n[ERROR] {message}")
        self.input.get_input("Press Enter to continue...")

    def show_startup_menu(self) -> str:
        self.output.clear()
        options = [
            "1) List Existing Databases",
            "2) Open Existing Database",
            "3) Create New Database",
            "4) Exit"
        ]

        formatted_menu = self.menu_renderer.render("IT Asset Tracker", options)
        self.output.display(formatted_menu)
        return self.input.get_input("Enter choice: ")

    def show_menu(self) -> str:
        self.output.clear()
        options = [
            "1. List Assets", 
            "2. Add Asset", 
            "3. Update Asset",
            "4. Delete Asset", 
            "5. Export Assets", 
            "6. Back"
        ]
        self.output.display(self.menu_renderer.render("Asset Manager", options))
        return self.input.get_input("Select option: ")
    

    def display_assets(self, assets: List[dict]):
        formatted_table = self.table_renderer.render(assets)
        self.output.display("\n" + formatted_table)
        self.input.get_input("\nPress Enter to continue...")

    def display_database_list(self, names: List[str]):
        self.output.display(self.menu_renderer.render("Existing Databases", 
            [f"{i+1}) {name}" for i, name in enumerate(names)]))
        
        self.input.get_input("\nPress Enter to continue...")
        

    def prompt_for_schema(self) -> Dict[str, str]:
        dialog = SchemaBuilderDialog(self.input, self.output)
        return dialog.run()

    def prompt_db_name(self):
        return self.input.get_input("Enter database name: ")
    
    def prompt_for_id(self, action="delete"):
        return int(self.input.get_input(f"Enter ID to {action}: "))

    def prompt_for_asset_data(self, columns: list) -> dict:
        self.output.display("\n--- Add New Entry ---")
        data = {}
        for col in columns:
            if "id" in col.lower(): continue
            data[col] = self.input.get_input(f"Enter {col}: ")
        return data

    def prompt_for_update(self, current: dict) -> dict:
        self.output.display(f"\n--- Update Asset ---")
        updated = {}
        for col, val in current.items():
            if col == 'asset_id': continue
            new_val = self.input.get_input(f"{col} [{val}]: ")
            updated[col] = new_val if new_val else val
        return updated
    
    def prompt_for_export(self):
        fmt = self.input.get_input("Format (csv/json): ").lower()
        fname = self.input.get_input("Filename: ")
        return fmt, fname

