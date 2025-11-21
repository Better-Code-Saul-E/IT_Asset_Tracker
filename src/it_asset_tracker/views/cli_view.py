from typing import List, Dict
from src.it_asset_tracker.views.console_io import ConsoleIO
from src.it_asset_tracker.views.renderers import TableRenderer, MenuRenderer
from src.it_asset_tracker.views.dialogs import SchemaBuilderDialog

class CLIView:
    def __init__(self):
        self.io = ConsoleIO()
        self.table_renderer = TableRenderer()
        self.menu_renderer = MenuRenderer()

    def show_message(self, message: str):
        self.io.display(f"\n[INFO] {message}")
        self.io.get_input("Press Enter to continue...")

    def show_error(self, message: str):
        self.io.display(f"\n[ERROR] {message}")
        self.io.get_input("Press Enter to continue...")

    def show_startup_menu(self) -> str:
        self.io.clear()
        options = [
            "1) List Existing Databases",
            "2) Open Existing Database",
            "3) Create New Database",
            "4) Exit"
        ]

        formatted_menu = self.menu_renderer.render("IT Asset Tracker", options)
        self.io.display(formatted_menu)
        return self.io.get_input("Enter choice: ")

    def show_menu(self) -> str:
        self.io.clear()
        options = [
            "1. List Assets", 
            "2. Add Asset", 
            "3. Update Asset",
            "4. Delete Asset", 
            "5. Export Assets", 
            "6. Back"
        ]
        self.io.display(self.menu_renderer.render("Asset Manager", options))
        return self.io.get_input("Select option: ")
    

    def display_assets(self, assets: List[dict]):
        formatted_table = self.table_renderer.render(assets)
        self.io.display("\n" + formatted_table)
        self.io.get_input("\nPress Enter to continue...")

    def display_database_list(self, names: List[str]):
        self.io.display(self.menu_renderer.render("Existing Databases", 
            [f"{i+1}) {name}" for i, name in enumerate(names)]))
        
        self.io.get_input("\nPress Enter to continue...")
        

    def prompt_for_schema(self) -> Dict[str, str]:
        dialog = SchemaBuilderDialog(self.io, self.io)
        return dialog.run()


    def prompt_db_name(self):
        return self.io.get_input("Enter database name: ")
    
    def prompt_for_id(self, action="delete"):
        return int(self.io.get_input(f"Enter ID to {action}: "))

    def prompt_for_asset_data(self, columns: list) -> dict:
        self.io.display("\n--- Add New Entry ---")
        data = {}
        for col in columns:
            if "id" in col.lower(): continue
            data[col] = self.io.get_input(f"Enter {col}: ")
        return data

    def prompt_for_update(self, current: dict) -> dict:
        self.io.display(f"\n--- Update Asset ---")
        updated = {}
        for col, val in current.items():
            if col == 'asset_id': continue
            new_val = self.io.get_input(f"{col} [{val}]: ")
            updated[col] = new_val if new_val else val
        return updated
    
    def prompt_for_export(self):
        fmt = self.io.get_input("Format (csv/json): ").lower()
        fname = self.io.get_input("Filename: ")
        return fmt, fname

