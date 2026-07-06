import os
import shutil
import sqlite3
import random

DB_PATH = "instance/students.sqlite3"
BAK_PATH = "instance/students.sqlite3.bak"

def migrate():
    # 1. Back up database if it exists
    if os.path.exists(DB_PATH):
        print(f"Creating database backup at {BAK_PATH}...")
        shutil.copyfile(DB_PATH, BAK_PATH)
    else:
        print("Database file not found. Nothing to migrate.")
        return

    # 2. Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check existing columns
        cursor.execute("PRAGMA table_info(students)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # 3. Add column if it doesn't exist
        if "phone" not in columns:
            print("Adding 'phone' column to 'students' table...")
            cursor.execute("ALTER TABLE students ADD COLUMN phone VARCHAR(20)")
            conn.commit()
        else:
            print("'phone' column already exists.")

        # 4. Generate random phone numbers for existing rows
        cursor.execute("SELECT student_id, name, phone FROM students")
        rows = cursor.fetchall()
        
        for student_id, name, phone in rows:
            if not phone:
                # Generate a random formatted phone number e.g., 555-123-4567
                area = random.randint(200, 999)
                prefix = random.randint(100, 999)
                line = random.randint(1000, 9999)
                new_phone = f"{area}-{prefix}-{line}"
                
                print(f"Assigning phone number {new_phone} to student '{name.strip()}' (ID: {student_id})")
                cursor.execute(
                    "UPDATE students SET phone = ? WHERE student_id = ?",
                    (new_phone, student_id)
                )
        
        conn.commit()
        print("Database migration completed successfully.")
        
    except Exception as e:
        conn.rollback()
        print(f"Migration failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
