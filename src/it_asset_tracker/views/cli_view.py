from tabulate import tabulate
from typing import List
from src.it_asset_tracker.models.asset import Asset

class CLIView:
    def show_startup_menu(self):
        print("\n===== IT Asset Tracker Main Menu =====")
        print("1) List Existing databases")
        print("2) Open / Create a new database")
        print("3) Exit application")
        return input("Enter your choice: ")

    def display_database_list(self, database_names: List[str]):
        print("\n===== Existing Databases =====")
        if not database_names:
            print("No databases found.")
            return
        
        for i, name in enumerate(database_names):
            print(f"{i + 1}) {name}")

    def prompt_db_name(self):
        return input("Enter database name to create or open (e.g. 'company_assets'): ")

    def show_goodbye(self):
        print("Exiting application. Goodbye!")

    def show_error(self, message: str):
        print(f"[ERROR] {message}")




    def show_welcome(self):
        print("\n===== Managing Assets =====")

    def show_menu(self):
        print("\n1. List Assets")
        print("2. Add Asset")
        print("3. Update Asset")
        print("4. Delete Asset")
        print("5. Export Assets") 
        print("6. Back to Main Menu")
        return input("Select an option: ")

    def display_assets(self, assets: List[Asset]):
        if not assets:
            print("No assets found.")
            return
        data = [[a.id, a.device_type, a.manufacturer, a.model, a.serial_number] for a in assets]
        headers = ["ID", "Type", "Manufacturer", "Model", "Serial"]
        print(tabulate(data, headers=headers, tablefmt="grid"))

    def prompt_for_asset_data(self):
        print("\n--- Add New Asset ---")
        dtype = input("Device Type: ")
        manuf = input("Manufacturer: ")
        model = input("Model: ")
        serial = input("Serial Number: ")
        return dtype, manuf, model, serial

    def prompt_for_id(self, action="delete"):
        return int(input(f"Enter ID to {action}: "))
    
    def show_message(self, message: str):
        print(f"[INFO] {message}")
    
    def prompt_for_update(self, current_asset: Asset):
        print(f"\n--- Update Asset (ID: {current_asset.id}) ---")
        print("Press [Enter] to keep current value.")
        
        dtype = input(f"Device Type [{current_asset.device_type}]: ") or current_asset.device_type
        manuf = input(f"Manufacturer [{current_asset.manufacturer}]: ") or current_asset.manufacturer
        model = input(f"Model [{current_asset.model}]: ") or current_asset.model
        serial = input(f"Serial Number [{current_asset.serial_number}]: ") or current_asset.serial_number
        
        return Asset(id=current_asset.id, device_type=dtype, manufacturer=manuf, model=model, serial_number=serial)
    
    def prompt_for_export(self):
        print("\n--- Export Assets ---")
        print("Available formats: csv, json")
        fmt = input("Enter format: ").lower()
        fname = input("Enter filename (without extension): ")
        return fmt, fname