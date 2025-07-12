import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional

class Database:
    def __init__(self, db_name: str = 'db\\scripts_database.db'):
        self.db_name = db_name
    
    def create_table(self, table_name, columns: dict = None):
        if columns is None:
            ## Create blank table with autoincrementing primary key 
            columns = {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            }

        ## Create SQL query string based on dictionary
        columns_sql = ",\n                    ".join(
                    [f"{col} {col_type}" for col, col_type in columns.items()]
                    )

        create_sql = f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        {columns_sql}
                    )
                    '''

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(create_sql)
            conn.commit()

    def view_table(self, table_name):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {table_name}')

            ## Notes -> 7 elements in tuple from c.description provides column metadata (name, type_code, display_size, internal_size, precision, scale, null_ok). 
            print(cursor.description)
            all_rows = cursor.fetchall()
            print(all_rows)

    def insert_into_table(self, table_name, data_dict):
        """
        data_dict: {
            "col1": [val1_row1, val1_row2, ...],
            "col2": [val2_row1, val2_row2, ...],
            ...
        }
        """
        if not data_dict:
            raise ValueError("No data provided")

        columns = list(data_dict.keys())
        num_rows = len(next(iter(data_dict.values())))
        
        # Validate all columns have the same number of rows
        for col, values in data_dict.items():
            if len(values) != num_rows:
                raise ValueError(f"Column '{col}' has inconsistent number of values")
        
        # Build list of row tuples
        rows = []
        for i in range(num_rows):
            row = tuple(data_dict[col][i] for col in columns)
            rows.append(row)
        
        # Create SQL with dynamic columns and placeholders
        cols_sql = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))
        insert_sql = f"INSERT INTO {table_name} ({cols_sql}) VALUES ({placeholders})"

        # Insert
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.executemany(insert_sql, rows)
            conn.commit()



if __name__ == "__main__":
    ## Initate database instance
    db = Database()
    
    # Create tables
    script_dict = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "name": "TEXT NOT NULL",
    "description": "TEXT NOT NULL",
    }
    
    db.create_table(table_name='scripts',
                    columns = script_dict)

    client_dict = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "name": "TEXT NOT NULL",
    "code": "TEXT NOT NULL",
    "description": "TEXT NOT NULL",
    }
    
    db.create_table(table_name='clients',
                    columns = client_dict)


    job_dict = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "script_id": "INTEGER NOT NULL",
    "client_id": "INTEGER NOT NULL",
    "run_datetime": "DATETIME NOT NULL",
    "run_status": "BOOLEAN NOT NULL"
    }
    
    db.create_table(table_name='jobs',
                    columns = job_dict)



    # # Add some scripts
    # db.add_script('backup_script.py', '2024-01-15', 'completed')
    # db.add_script('data_processing.py', '2024-01-16', 'running')
    # db.add_script('cleanup_script.py', '2024-01-17', 'failed')
    
    # # Get all scripts
    # print("All scripts:")
    # for script in db.get_all_scripts():
    #     print(f"ID: {script[0]}, Script: {script[1]}, Date: {script[2]}, Status: {script[3]}")
    
    # # Get scripts by status
    # print("\nCompleted scripts:")
    # for script in db.get_scripts_by_status('completed'):
    #     print(f"ID: {script[0]}, Script: {script[1]}, Date: {script[2]}, Status: {script[3]}")
    
    # # Update a script status
    # db.update_script_status(2, 'completed')
    # print("\nAfter updating script ID 2 to completed:")
    # for script in db.get_all_scripts():
    #     print(f"ID: {script[0]}, Script: {script[1]}, Date: {script[2]}, Status: {script[3]}")