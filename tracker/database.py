import sqlite3
from sqlite3 import Error;

class DatabaseManager:
    """Manages the SQLite databise connection and its operations"""

    def __init__(self, db_file):
        self.connection = None
        self.db_file = db_file

        try:
            self.connection = sqlite3.connect(db_file)
            print(f"Connected to SQLite DB {db_file}")

        except Error as e:
            print(f"Error connecting to database: {e}")

    def create_table(self, table_name, columns):
        try: 
            column_definitions = ", ".join([f"{name} {dtype}" for name, dtype in columns.items()])            
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions});"            
            self.connection.cursor().execute(sql)            
            print(f"Table '{table_name}' created or already exists.")        
        except Error as e:            
            print(f"Error creating table: {e}")

    def add_row(self, table_name, data_dict):
        columns = ', '.join(data_dict.keys())        
        placeholders = ', '.join(['?'] * len(data_dict))        
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"                
        try:            
            cur = self.connection.cursor()            
            cur.execute(sql, tuple(data_dict.values()))            
            self.connection.commit()            
            print(f"Added new row with ID: {cur.lastrowid}")            
            return cur.lastrowid        
        except Error as e:            
            print(f"Error adding row to '{table_name}': {e}")            
            return None    
    
    def list_tables(self):
        try:
            temp = self.connection.cursor()
            temp.execute("SELECT name FROM sqlite_master WHERE type='table';")

            tables = [row[0] for row in temp.fetchall()]
            return tables
        except Error as e:
            print(f"Error listing tables: {e}")
            return []
    
    def get_table_columns(self, table_name):
        try: 
            temp = self.connection.cursor()
            temp.execute(f"PRAGMA table_info({table_name})")

            columns = [row[1] for row in temp.fetchall()]
            return columns
        except Error as e:
            print(f"Error getting column names for '{table_name}': {e}")
            return []

    def get_table_data(self, table_name):
        try:
            temp = self.connection.cursor()
            temp.execute(f"SELECT * FROM {table_name}")
            rows = temp.fetchall()
            return rows
        except Error as e:
            print(f"Error getting data from '{table_name}': {e}")
            return []    

    def update_row(self, table_name, row_id, data_dict, pk_column='id'):
        set_clause = ", ".join([f"{key} = ?" for key in data_dict.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {pk_column} = ?"
    
        try:
            temp = self.connection.cursor()
            temp.execute(sql, (*data_dict.values(), row_id))
            self.connection.commit()
            print(f"Row with id {row_id} updated successfully.")
        except Error as e:
            print(f"Error updating row: {e}")

    def delete_row(self, table_name, row_id, pk_column='id'):
        sql = f"DELETE FROM {table_name} WHERE {pk_column} = ?"
    
        try:
            temp = self.connection.cursor()
            temp.execute(sql, (row_id,))
            self.connection.commit()
            print(f"Row with id {row_id} deleted successfully")
        except Error as e:
            print(f"Error deleting row: {e}")
    

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
    
            

if __name__ == '__main__':
    """
    TESTING DATABASE
    
    ADD NEW DATA !!!!!!!!!!!!!!!!!!
    
    [8-)]
    """
     
    db = DatabaseManager("../data/test_assets.db")    

    asset_columns = {        
        'asset_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',        
        'device_type': 'TEXT NOT NULL',        
        'manufacturer': 'TEXT NOT NULL',        
        'model': 'TEXT NOT NULL',        
        'serial_number': 'TEXT NOT NULL UNIQUE'    
        }    
    
    db.create_table('assets', asset_columns)    
    
    
    # Data is chatgpt genereated to save time
    # T_T It would take hours to make this data from scratch
    new_assets = [
    {'device_type': 'Laptop',    'manufacturer': 'Apple',     'model': 'MacBook Pro M3',        'serial_number': 'XYZ98765'},
    {'device_type': 'Desktop',   'manufacturer': 'Dell',      'model': 'OptiPlex 7090',        'serial_number': 'DL7090-5566'},
    {'device_type': 'Laptop',    'manufacturer': 'HP',        'model': 'EliteBook 840 G8',      'serial_number': 'HP840G8-2211'},
    {'device_type': 'Tablet',    'manufacturer': 'Samsung',   'model': 'Galaxy Tab S9',         'serial_number': 'SM-T875-3344'},
    {'device_type': 'Phone',     'manufacturer': 'Google',    'model': 'Pixel 8',               'serial_number': 'GPX8-1122'},
    {'device_type': 'Router',    'manufacturer': 'Cisco',     'model': 'ISR4451-X',             'serial_number': 'CS-ISR4451-0099'},
    {'device_type': 'Laptop',    'manufacturer': 'Lenovo',    'model': 'ThinkPad T14 Gen 2',    'serial_number': 'LNV-T14-3322'},
    {'device_type': 'Monitor',   'manufacturer': 'ASUS',      'model': 'ProArt PA278QV',        'serial_number': 'AS-PA278-7788'},
    {'device_type': 'Printer',   'manufacturer': 'Brother',   'model': 'HL-L2395DW',            'serial_number': 'BR-HL2395-4455'},
    {'device_type': 'Server',    'manufacturer': 'HPE',       'model': 'ProLiant DL380 Gen10',  'serial_number': 'HPE-DL380-9001'},
    {'device_type': 'Laptop',    'manufacturer': 'Acer',      'model': 'Swift 3',               'serial_number': 'AC-SW3-6677'},
    {'device_type': 'Desktop',   'manufacturer': 'Custom',    'model': 'Workstation R5',        'serial_number': 'CW-R5-3340'},
    {'device_type': 'NAS',       'manufacturer': 'Synology',  'model': 'DS923+',                'serial_number': 'SY-DS923-2210'},
    {'device_type': 'Phone',     'manufacturer': 'Apple',     'model': 'iPhone 15 Pro',         'serial_number': 'APL-IP15P-778'},
    {'device_type': 'Accessory', 'manufacturer': 'Logitech',  'model': 'MX Master 3',           'serial_number': 'LG-MX3-9009'},
    ]
 
    for row in new_assets:
        db.add_row('assets', row)    
    
    db.close()






