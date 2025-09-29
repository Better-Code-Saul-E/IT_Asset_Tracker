from database import DatabaseManager
from tabulate import tabulate
import csv
import json
import os
import glob


def add_asset(db_manger):
    print("\n===== Add a New Asset =====")
    tables = db_manger.list_tables()
    if not tables:
        print("No tables found in this database. Please create a table first.")
        return

    table_name = tables[0]
    print(f"Adding asset to table: '{table_name}'")
    
    columns = db_manger.get_table_columns(table_name)[1:]
    asset_data = {}
    for col in columns:
        asset_data[col] = input(f"Enter the {col}: ")

    if asset_data:
        db_manger.add_row(table_name, asset_data)
        print("Asset added successfully.")
    else:
        print("No data entered. Asset not added.")

def list_databases():
    print("\n===== Existing Databases =====")

    if not os.path.exists("../data"):
        os.makedirs('../data')
    
    db_files = glob.glob('../data/*.db')
    if not db_files:
        print("No databases were found in the 'data' folder.")
        return
    
    for i, filepath in enumerate(db_files):
        filename = os.path.basename(filepath)
        print(f"{i + 1}) {filename}")


def table_creator(db_manager):
    print("\n===== Create a New Table =====")
    print("First, give the table a name (e.g. assets, employees, managers).")
    table_name = input("Enter the name for the table: ")

    if not table_name:
        print("Table name cannot be empty!")
        return
    
    columns = {'id': 'INTEGER PRIMARY KEY AUTOINCREMENT'}
    print("\nA 'id' column has been added automatically as the unique identifier.")
    print("Add the other columns. Type 'done' when you're finished.")
    
    while True:
        print("-" * 20)
        column_name = input("Enter column name (or type 'done' to finish): ")
        if column_name.lower() == 'done':
            break
        
        if not column_name: 
            print("Column type cannot be empty. Please try again")
            continue
        
        # Data selection Menu
        while True:
            print(f"\nWhat kind of data will the '{column_name}' column hold?")            
            print("  1. Text (e.g., names, descriptions)")            
            print("  2. Number (e.g., quantity, price)")            
            print("  3. Date (e.g., purchase_date)") 
            print("  4. Decimal (e.g., 9.99, 45.50)")
            print("  5. True/False (e.g., is_active)")           
            type_choice = input("\nSelect an option (1-5): ")
            
            sql_type = ""
            
            if type_choice == '1' or type_choice == '3':
                sql_type = "TEXT"
                break
            elif type_choice == '2' or type_choice == '5':
                sql_type = "INTEGER"
                break
            elif type_choice == '4':
                sql_type = "REAL"
                print("NOTE: True/False will be stored as 1/0.")
                break
            else: 
                print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
        
        is_required = input("\nCan this field be left empty? (yes/no): ").lower()
        if is_required == 'no':
            sql_type += " NOT NULL"
        
        columns[column_name] = sql_type
        print(f"COLUMN '{column_name}' added as {sql_type}.")

    if len(columns) > 1:
        print(f"\nCreating table '{table_name}'...")
        db_manager.create_table(table_name, columns)
    else:
        print("No columns wer defined. Nothing to create")

def update_asset(db_manager):
    print("===== Update an Asset =====")
    display_table(db_manager)
    
    tables = db_manager.list_tables()
    
    if not tables:
        return

    table_name = tables[0]
    try:
        primary_key_column = db_manager.get_table_columns(table_name)[0]
        
        asset_id = int(input(f"Enter the {primary_key_column} of the asset you want to updated: "))
        column_to_update = input("Enter the exact column name update (e.g., model): ")
        
        if column_to_update not in db_manager.get_table_columns(table_name):
            print(f"Error: Column '{column_to_update}' does not exist.")
            return
        new_value = input(f"Enter the new value for {column_to_update}: ")
        
        confirmation = input(f"Update row {asset_id} to set {column_to_update} to '{new_value}'? (yes/no): ").lower()
        if confirmation == 'yes':
            update_data = {column_to_update: new_value}
            db_manager.update_row(table_name, asset_id, update_data, pk_column=primary_key_column)
        else:
            print("Update cancelled.")
    except ValueError:
        print("Invalid ID. Please enter a number.")
        
def delete_asset(db_manager):
    print("\n===== Delete an Asset =====")
    display_table(db_manager)
    
    tables = db_manager.list_tables()
    if not tables:
        return

    table_name = tables[0]
    try:
        primary_key_column = db_manager.get_table_columns(table_name)[0]

        asset_id = int(input(f"Enter the {primary_key_column} of the asset you want to delete: "))
         
        confirmation = input(f"Are you sure you want to PERMANENTLY delete asset ID {asset_id}? (yes/no): ").lower()
        if confirmation == 'yes':
            db_manager.delete_row(table_name, asset_id, pk_column=primary_key_column)
        else:
            print("Deletion cancelled.")
    except ValueError:
        print("Invalid ID. Please enter a number.")

def display_table(db_manager):
    tables = db_manager.list_tables()
    if not tables:
        print("No tables found in this database. Please create one first.")
        return

    tables_to_list = tables[0]
    
    headers = db_manager.get_table_columns(tables_to_list)
    data = db_manager.get_table_data(tables_to_list)
    
    if not data:
        print(f"No dat gound in table '{tables_to_list}'.")
    else:
        print(tabulate(data, headers=headers, tablefmt="grid"))

def export_data(db_manager):
    print("\n===== Export All Assets =====")
    tables = db_manager.list_tables()
    if not tables:
        print("No tables availible to export.")
        return
    
    table_name = tables[0]
    columns = db_manager.get_table_columns(table_name)
    results = db_manager.get_table_data(table_name)
    
    if not results:
        print("No results found to export.")
        return
    
    print("Current data in the table:")
    print(tabulate(results, headers=columns, tablefmt="grid"))
    
    export_choice = input("\nChoice an export format (csv/json/no): ").lower()
    if export_choice not in ['csv', 'json']:
        print("Not exporting.")
        return

    export_path = '../exports'
    os.makedirs(export_path, exist_ok=True)

    filename = input("Enter a filename for the export (without extension): ")
    results_as_dict = [dict(zip(columns, row)) for row in results]
    
    if export_choice == "csv":
        
        full_filepath = os.path.join(export_path, f"{filename}.csv")
        try:
            with open(full_filepath, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writeheader()
                writer.writerows(results_as_dict)
            print(f"Successfully exported data to {filename}.csv")
        except IOError:
            print("Error writing to CSV file.")
    elif export_choice == "json":
        full_filepath = os.path.join(export_path, f"{filename}.json")
        try:
            with open(full_filepath, 'w') as jsonfile:
                json.dump(results_as_dict, jsonfile, indent=4)
            print(f"Successfully exported data to {filename}.json")
        except IOError:
            print("Error writing to JSON file.")
        