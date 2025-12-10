import mysql.connector
import datetime
import re

config = {
    "host": "your_db_hostname",
    "user": "your_username",
    "password": "your_password",
    "database": "your_db_name"
}

def get_connection():
    return mysql.connector.connect(**config)

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DROP TABLE IF EXISTS students;
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            roll VARCHAR(50) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            age INT,
            course VARCHAR(100),
            email VARCHAR(150) UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def add_student():
    while True:
        roll = input("Enter Roll Number: ").strip()
        if not roll.isdigit():
            print("Error: Roll number should contain only digits and not be empty. Please try again.")
        else:
            break

    while True:
        name = input("Enter Name: ").strip()
        if not name:
            print("Error: Name should not be empty. Please try again.")
        elif name.count(' ') > 1:
            print("Error: Name should not contain more than one space. Please try again.")
        elif not re.fullmatch(r"[a-zA-Z\s]+", name):
            print("Error: Name should only contain letters and spaces. Please try again.")
        else:
            break

    while True:
        age_raw = input("Enter Age: ").strip()
        if not age_raw.isdigit():
            print("Error: Age should be a number and not be empty. Please try again.")
        else:
            age = int(age_raw)
            if not (1 <= age <= 120):
                print("Error: Age should be between 1 and 120. Please try again.")
            else:
                break

    while True:
        course = input("Enter Course: ").strip()
        if not course:
            print("Error: Course should not be empty. Please try again.")
        elif not re.fullmatch(r"[a-zA-Z\s]+", course):
            print("Error: Course should only contain letters and spaces. Please try again.")
        else:
            break

    while True:
        email = input("Email (optional): ").strip() or None
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Error: Invalid email format. Please try again or leave blank.")
        else:
            break

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO students (roll, name, age, course, email) VALUES (%s, %s, %s, %s, %s)",
            (roll, name, age, course, email)
        )
        conn.commit()
        print("Student added successfully (ID {}).\n".format(cur.lastrowid))
    except mysql.connector.Error as err:
        if err.errno == 1062: # Duplicate entry error
            print(f"Error: A student with Roll Number '{roll}' or Email '{email}' already exists. Please use unique values.\n")
        else:
            print(f"Database error: {err}\n")
    finally:
        cur.close()
        conn.close()

def view_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, roll, name, age, course, email, created_at, updated_at FROM students ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print("No students found.\n")
        return

    print("\n--- Student List ---")
    for r in rows:
        print(f"ID:{r[0]} | Roll:{r[1]} | Name:{r[2]} | Age:{r[3]} | Course:{r[4]} | Email:{r[5]} | Created:{r[6]} | Updated:{r[7]}")
    print()

def search_student():
    roll = input("Enter roll number to search: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, roll, name, age, course, email FROM students WHERE roll = %s", (roll,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        print(f"Found --> ID:{row[0]} | Roll:{row[1]} | Name:{row[2]} | Age:{row[3]} | Course:{row[4]} | Email:{row[5]}\n")
    else:
        print("Student not found.\n")

def update_student():
    roll_to_update = input("Enter roll number of the student to update: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, roll, name, age, course, email FROM students WHERE roll = %s", (roll_to_update,))
    row = cur.fetchone()
    if not row:
        print("Student not found.\n")
        cur.close()
        conn.close()
        return

    sid, cur_roll, cur_name, cur_age, cur_course, cur_email = row
    print("Current values (leave blank to keep):")
    print(f" Roll: {cur_roll}")
    print(f" Name: {cur_name}")
    print(f" Age: {cur_age}")
    print(f" Course: {cur_course}")
    print(f" Email: {cur_email}")
    print()

    # Prompt for new values with validation
    while True:
        new_roll_input = input(f"New Roll [{cur_roll}]: ").strip()
        if not new_roll_input:
            new_roll = cur_roll
            break
        if not new_roll_input.isdigit():
            print("Error: Roll number should contain only digits. Please try again or leave blank.")
        else:
            new_roll = new_roll_input
            break

    while True:
        new_name_input = input(f"New Name [{cur_name}]: ").strip()
        if not new_name_input:
            new_name = cur_name
            break
        if new_name_input.count(' ') > 1:
            print("Error: Name should not contain more than one space. Please try again or leave blank.")
        elif not re.fullmatch(r"[a-zA-Z\s]+", new_name_input):
            print("Error: Name should only contain letters and spaces. Please try again or leave blank.")
        else:
            new_name = new_name_input
            break

    while True:
        new_age_raw = input(f"New Age [{cur_age}]: ").strip()
        if not new_age_raw:
            new_age = cur_age
            break
        if not new_age_raw.isdigit():
            print("Error: Age should be a number. Please try again or leave blank.")
        else:
            temp_age = int(new_age_raw)
            if not (1 <= temp_age <= 120):
                print("Error: Age should be between 1 and 120. Please try again or leave blank.")
            else:
                new_age = temp_age
                break

    while True:
        new_course_input = input(f"New Course [{cur_course or ''}]: ").strip()
        if not new_course_input:
            new_course = cur_course
            break
        if not re.fullmatch(r"[a-zA-Z\s]+", new_course_input):
            print("Error: Course should only contain letters and spaces. Please try again or leave blank.")
        else:
            new_course = new_course_input
            break

    while True:
        new_email = input(f"New Email [{cur_email or ''}]: ").strip()
        if not new_email:
            new_email = cur_email
            break
        if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
            print("Error: Invalid email format. Please try again or leave blank.")
        else:
            break

    # Update query
    try:
        cur.execute("""
            UPDATE students
            SET roll=%s, name=%s, age=%s, course=%s, email=%s, updated_at=%s
            WHERE id=%s
        """, (new_roll, new_name, new_age, new_course, new_email, datetime.datetime.now(), sid))
        conn.commit()
        print("Student updated successfully.\n")
    except mysql.connector.Error as err:
        if err.errno == 1062: # Duplicate entry error
            print(f"Error: A student with Roll Number '{new_roll}' or Email '{new_email}' already exists. Please use unique values.\n")
        else:
            print(f"Database error: {err}\n")
    finally:
        cur.close()
        conn.close()

def delete_student():
    roll = input("Enter roll number to delete: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM students WHERE roll = %s", (roll,))
    row = cur.fetchone()
    if not row:
        print("Student not found.\n")
        cur.close()
        conn.close()
        return
    sid, name = row
    confirm = input(f"Delete {name} (roll {roll})? (y/N): ").strip().lower()
    if confirm == 'y':
        cur.execute("DELETE FROM students WHERE id = %s", (sid,))
        conn.commit()
        print("Student deleted.\n")
    else:
        print("Deletion canceled.\n")
    cur.close()
    conn.close()

def main():
    create_table()
    while True:
        print("===== Student Management (MySQL + Colab) ====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid option!\n")

if __name__ == "__main__":
    main()
