from src.it_asset_tracker.services.asset_service import AssetService
from src.it_asset_tracker.views.cli_view import CLIView
from src.it_asset_tracker.services.export_service import ExportService

from src.it_asset_tracker.interfaces.asset_service_interface import IAssetService
from src.it_asset_tracker.interfaces.exporter_interface import IFileExporter
from src.it_asset_tracker.interfaces.cli_view_interface import IView

class AssetController:
    def __init__(self, service: IAssetService, export_service: IFileExporter, view: IView):
        self.service = service
        self.export_service = export_service
        self.view = view

        self.actions = {
            '1': self._list_assets,
            '2': self._add_asset,
            '3': self._update_asset,
            '4': self._delete_asset,
            '5': self._export_assets,
        }
 
    def run(self):
        while True:
            choice = self.view.show_menu()
            if choice == '6':
                break

            action = self.actions.get(choice)
            if action:
                action()
            else:
                self.view.show_error("Invalid choice")

    def _list_assets(self):
        assets = self.service.get_all_assets()
        self.view.display_assets(assets)

    def _add_asset(self):
        columns = self.service.get_table_columns()
        data = self.view.prompt_for_asset_data(columns)

        try:
            new_id = self.service.create_asset(data)
            self.view.show_message(f"Created with ID: {new_id}")

        except ValueError as e:
            self.view.show_error(str(e))

    def _update_asset(self):
        try:
            asset_id = self.view.prompt_for_id("update")
            existing = self.service.get_asset(asset_id)

            if existing:
                updated = self.view.prompt_for_update(existing)
                self.service.update_asset(asset_id, updated)
                self.view.show_message("Asset updated successfully.")
                
            else:
                self.view.show_message("Asset not found.")

        except ValueError:
            self.view.show_message("Invalid input.")

    def _delete_asset(self):
        try:
            asset_id = self.view.prompt_for_id("delete")
            success = self.service.remove_asset(asset_id)

            if success:
                self.view.show_message("Asset deleted.")
            else:
                self.view.show_message("Asset not found.")

        except ValueError:
            self.view.show_message("Invalid ID format.")

    def _export_assets(self):
        fmt, fname = self.view.prompt_for_export()
        try:
            assets = self.service.get_all_assets()
            if not assets:
                self.view.show_message("No assets to export.")
                return
            
            path = self.export_service.export_data(assets, fmt, fname)
            self.view.show_message(f"Exported successfully to: {path}")

        except ValueError as e:
            self.view.show_error(str(e))

        except Exception as e:
            self.view.show_error(f"Export failed: {e}")