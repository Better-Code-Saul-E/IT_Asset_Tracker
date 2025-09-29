import os
from database import DatabaseManager
from actions import *

def start_application():
    while True:
        print("\n===== IT asset Tracker Main Menu =====")
        print("1) List Existing databases")
        print("2) Open / Create a new database")
        print("3) Exit application")

        choice = input("Enter your choice: ")
        if choice == '1':
            list_databases()

        elif choice == '2':
            db_name = input("Enter database name to create or open (e.g. 'company_assets'): ")
            
            if not db_name:
                print("Database name cannot be empty.")
                continue
            if not db_name.endswith('.db'):
                db_name += '.db'

            db_file_path = f"../data/{db_name}"
            db_manager = DatabaseManager(db_file_path)

            asset_menu(db_manager)

        elif choice == '3':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

def asset_menu(db_manager):
    if not db_manager.connection:
        print("Could not connect to the database.")
        return

    while True:
        print(f"\n===== Managing '{os.path.basename(db_manager.db_file)}' =====")
        
        print("1) Add a new Asset")
        print("2) List all Assets")
        print("3) Create a Table")
        print("4) Update an Asset")
        print("5) Delete an Asset")
        print("6) Export Table")
        #coming soon
        print("9) Close this database (Return to main menu)")

        choice = input("Enter your choice: ")
        if choice == '1':
            add_asset(db_manager)
        elif choice == "2":
            display_table(db_manager)
        elif choice == '3':
            table_creator(db_manager)
        elif choice == '4':
            update_asset(db_manager)
        elif choice == '5':
            delete_asset(db_manager)
        elif choice == '6':
            export_data(db_manager)
        elif choice == '9':
            print("Closing database...")
            db_manager.close()
            break
        else:
            print("Invalid choice. Please try again")

if __name__ == '__main__':
    start_application()
    