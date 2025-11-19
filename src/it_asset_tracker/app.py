import os
import glob
from src.it_asset_tracker.repositories.sqlite_asset_repository import SQLiteAssetRepository
from src.it_asset_tracker.services.asset_service import AssetService
from src.it_asset_tracker.views.cli_view import CLIView
from src.it_asset_tracker.controllers.asset_controller import AssetController
from src.it_asset_tracker.services.export_service import ExportService

def main():
    view = CLIView()
    
    data_dir = get_data_directory()
    os.makedirs(data_dir, exist_ok=True)

    export_path = os.path.join(os.path.dirname(__file__), "../../exports")
    export_service = ExportService(export_path)

    while True:
        choice = view.show_startup_menu()

        if choice == '1':
            db_files = glob.glob(os.path.join(data_dir, "*.db"))
            db_names = [os.path.basename(f).replace('.db', '') for f in db_files]
            view.display_database_list(db_names)

        elif choice == '2':
            db_name = view.prompt_db_name()
            if not db_name:
                view.show_error("Database name cannot be empty.")
                continue
            
            if not db_name.endswith(".db"):
                db_name += ".db"
            
            db_path = os.path.join(data_dir, db_name)

            repo = SQLiteAssetRepository(db_path)
            service = AssetService(repo)
            controller = AssetController(service, export_service, view)

            controller.run()

        elif choice == '3':
            view.show_goodbye()
            break
        else:
            view.show_error("Invalid choice.")

def get_data_directory():
    return os.path.join(os.path.dirname(__file__), "../../data")


if __name__ == "__main__":
    main()