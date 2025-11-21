import os
import glob
from src.it_asset_tracker.views.cli_view import CLIView
from src.it_asset_tracker.utils.app_factory import AppFactory
from src.it_asset_tracker.config import AppConfig

from src.it_asset_tracker.views.console_io import ConsoleIO
from src.it_asset_tracker.views.renderers import TableRenderer, MenuRenderer
from src.it_asset_tracker.views.dialogs import SchemaBuilderDialog

class StartupController:
    def __init__(self):
        self.io = ConsoleIO()
        self.table_renderer = TableRenderer()
        self.menu_renderer = MenuRenderer()

        self.view = CLIView(
            input_provider=self.io,
            output_display=self.io,
            table_renderer=self.table_renderer,
            menu_renderer=self.menu_renderer 
            )        
        self.factory = AppFactory(AppConfig.EXPORT_DIR, self.view)
        
        self.actions = {
            '1': self._list_databases,
            '2': self._open_database,
            '3': self._create_database,
            '4': self._exit_app
        }
        self.running = True

    def run(self):
        AppConfig.ensure_dirs_exist()
        while self.running:
            choice = self.view.show_startup_menu()
            action = self.actions.get(choice)
            if action:
                action()
            else:
                self.view.show_error("Invalid choice.")

    def _list_databases(self):
        db_files = glob.glob(os.path.join(AppConfig.DATA_DIR, "*.db"))
        db_names = [os.path.basename(f).replace('.db', '') for f in db_files]
        self.view.display_database_list(db_names)

    def _get_db_path(self, name: str) -> str:
        if not name.endswith(".db"):
            name += ".db"
        return os.path.join(AppConfig.DATA_DIR, name)

    def _open_database(self):
        db_name = self.view.prompt_db_name()
        if not db_name: return

        db_path = self._get_db_path(db_name)
        if not os.path.exists(db_path):
            self.view.show_error("Database does not exist! Use option 3 to create it.")
            return

        controller = self.factory.create_controller(db_path)
        controller.run()

    def _create_database(self):
        db_name = self.view.prompt_db_name()
        if not db_name: return

        db_path = self._get_db_path(db_name)
        if os.path.exists(db_path):
            self.view.show_error("Database already exists! Use option 2 to open it.")
            return

        schema = self.view.prompt_for_schema()
        
        repo = self.factory.create_repo_for_setup(db_path)
        repo.create_table(schema)

        controller = self.factory.create_controller(db_path)
        controller.run()

    def _exit_app(self):
        self.view.show_message("\nGoodbye! Thanks for using IT Asset Tracker.")
        self.running = False