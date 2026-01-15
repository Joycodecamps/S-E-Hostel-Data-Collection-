import eel
import sqlite3

eel.init('web')


def init_db():
    conn = sqlite3.connect('collector.db')
    cursor = conn.cursor()
    # Removed image_path from table creation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            second_name TEXT,
            course TEXT,
            phone_number TEXT,
            room_number TEXT
        )
    ''')
    conn.commit()
    conn.close()


@eel.expose
def save_student(data):
    """Saves or Updates a student (Text data only)."""
    conn = sqlite3.connect('collector.db')
    cursor = conn.cursor()

    try:
        if data.get('id'):  # UPDATE existing
            cursor.execute('''
                UPDATE students
                SET first_name=?, second_name=?, course=?, phone_number=?, room_number=?
                WHERE id=?
            ''', (data['fName'], data['sName'], data['course'], data['phone'], data['room'], data['id']))
        else:  # INSERT new
            cursor.execute('''
                INSERT INTO students (first_name, second_name, course, phone_number, room_number)
                VALUES (?, ?, ?, ?, ?)
            ''', (data['fName'], data['sName'], data['course'], data['phone'], data['room']))

        conn.commit()
        return {"status": "success", "message": "Saved successfully!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()


@eel.expose
def get_students(search_query=""):
    conn = sqlite3.connect('collector.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if search_query:
        query = f"%{search_query}%"
        # Search by Name, Course, OR Room
        cursor.execute('''
            SELECT * FROM students 
            WHERE first_name LIKE ? 
            OR second_name LIKE ? 
            OR course LIKE ? 
            OR room_number LIKE ? 
            ORDER BY id DESC
        ''', (query, query, query, query))
    else:
        cursor.execute("SELECT * FROM students ORDER BY id DESC")

    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "id": row["id"],
            "fName": row["first_name"],
            "sName": row["second_name"],
            "course": row["course"],
            "phone": row["phone_number"],
            "room": row["room_number"]
        })
    return data


@eel.expose
def delete_student(student_id):
    conn = sqlite3.connect('collector.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    eel.start('index.html', size=(1200, 800), port=0)