from src.it_asset_tracker.services.asset_service import AssetService
from src.it_asset_tracker.views.cli_view import CLIView
from src.it_asset_tracker.services.export_service import ExportService

class AssetController:
    def __init__(self, service: AssetService, export_service: ExportService, view: CLIView):
        self.service = service
        self.export_service = export_service
        self.view = view

    def run(self):
        self.view.show_welcome()
        
        while True:
            choice = self.view.show_menu()
            
            if choice == '1':
                assets = self.service.get_all_assets()
                self.view.display_assets(assets)
            
            elif choice == '2':
                try:
                    dtype, manuf, model, serial = self.view.prompt_for_asset_data()
                    new_id = self.service.create_asset(dtype, manuf, model, serial)
                    self.view.show_message(f"Asset created successfully with ID: {new_id}")
                except ValueError as e:
                    self.view.show_error(str(e))
            
            elif choice == '3':
                try:
                    asset_id = self.view.prompt_for_id("update")
                    existing_asset = self.service.get_asset(asset_id)
                    
                    if existing_asset:
                        updated_asset = self.view.prompt_for_update(existing_asset)
                        self.service.update_asset_details(updated_asset)
                        self.view.show_message("Asset updated successfully.")
                    else:
                        self.view.show_message("Asset not found.")
                except ValueError:
                    self.view.show_message("Invalid input.")

            elif choice == '4':
                try:
                    asset_id = self.view.prompt_for_id("delete")
                    success = self.service.remove_asset(asset_id)
                    if success:
                        self.view.show_message("Asset deleted.")
                    else:
                        self.view.show_message("Asset not found.")
                except ValueError:
                    self.view.show_message("Invalid ID format.")

            elif choice == '5':
                fmt, fname = self.view.prompt_for_export()
                try:
                    assets = self.service.get_all_assets()
                    if not assets:
                        self.view.show_message("No assets to export.")
                        continue

                    path = self.export_service.export_data(assets, fmt, fname)
                    self.view.show_message(f"Exported successfully to: {path}")
                    
                except ValueError as e:
                    self.view.show_error(str(e))
                except Exception as e:
                    self.view.show_error(f"Export failed: {e}")

            elif choice == '6': 
                print("Returning to Main Menu...")
                break