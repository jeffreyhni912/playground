import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional

class ScriptsDatabase:
    def __init__(self, db_name: str = 'scripts_database.db'):
        self.db_name = db_name
        self.create_table()
    
    def create_table(self):
        """Create the scripts table if it doesn't exist"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scripts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    script TEXT NOT NULL,
                    date TEXT NOT NULL,
                    run_status TEXT NOT NULL
                )
            ''')
            conn.commit()
    
    def add_script(self, script: str, date: str, run_status: str) -> int:
        """Add a new script record to the database"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO scripts (script, date, run_status) VALUES (?, ?, ?)
            ''', (script, date, run_status))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_scripts(self) -> List[Tuple]:
        """Get all scripts from the database"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM scripts')
            return cursor.fetchall()
    
    def get_scripts_by_status(self, status: str) -> List[Tuple]:
        """Get scripts filtered by run status"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM scripts WHERE run_status = ?', (status,))
            return cursor.fetchall()
    
    def update_script_status(self, script_id: int, new_status: str):
        """Update the run status of a script"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE scripts SET run_status = ? WHERE id = ?
            ''', (new_status, script_id))
            conn.commit()
    
    def delete_script(self, script_id: int):
        """Delete a script from the database"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM scripts WHERE id = ?', (script_id,))
            conn.commit()

# Example usage
if __name__ == "__main__":
    # Create database instance
    db = ScriptsDatabase()
    
    # Add some scripts
    db.add_script('backup_script.py', '2024-01-15', 'completed')
    db.add_script('data_processing.py', '2024-01-16', 'running')
    db.add_script('cleanup_script.py', '2024-01-17', 'failed')
    
    # Get all scripts
    print("All scripts:")
    for script in db.get_all_scripts():
        print(f"ID: {script[0]}, Script: {script[1]}, Date: {script[2]}, Status: {script[3]}")
    
    # Get scripts by status
    print("\nCompleted scripts:")
    for script in db.get_scripts_by_status('completed'):
        print(f"ID: {script[0]}, Script: {script[1]}, Date: {script[2]}, Status: {script[3]}")
    
    # Update a script status
    db.update_script_status(2, 'completed')
    print("\nAfter updating script ID 2 to completed:")
    for script in db.get_all_scripts():
        print(f"ID: {script[0]}, Script: {script[1]}, Date: {script[2]}, Status: {script[3]}")