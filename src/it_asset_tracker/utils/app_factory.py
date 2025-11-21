from src.it_asset_tracker.repositories.db_context import SQLiteContext
from src.it_asset_tracker.repositories.sqlite_asset_repository import SQLiteAssetRepository
from src.it_asset_tracker.services.asset_service import AssetService
from src.it_asset_tracker.controllers.asset_controller import AssetController
from src.it_asset_tracker.services.exporters import CsvExporter, JsonExporter
from src.it_asset_tracker.services.export_service import ExportService
from src.it_asset_tracker.views.cli_view import CLIView

class AppFactory:
    def __init__(self, export_path: str, view: CLIView):
        exporters = {
            'csv': CsvExporter(),
            'json': JsonExporter()
        }

        self.export_service = ExportService(export_path, exporters)
        self.view = view

    def create_controller(self, db_path: str) -> AssetController:
        context = SQLiteContext(db_path)
        repo = SQLiteAssetRepository(context)
        service = AssetService(repo)
        
        return AssetController(service, self.export_service, self.view)
    
    def create_repo_for_setup(self, db_path: str) -> SQLiteAssetRepository:
        context = SQLiteContext(db_path)
        return SQLiteAssetRepository(context)