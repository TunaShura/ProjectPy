import sqlite3

# Ket noi toi co so du lieu
conn = sqlite3.connect('university.db')
cursor = conn.cursor()

# PHAN 1: TAO BANG students
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id      INTEGER PRIMARY KEY,
        name    TEXT,
        major   TEXT,
        gpa     REAL
    )
""")
conn.commit()
print("Da tao database 'university.db' va bang 'students'.")

# PHAN 2: THEM DU LIEU (5+ sinh vien)
students_data = [
    ("Nguyen Van An",  "Cong nghe thong tin",  3.5),
    ("Tran Thi Binh",  "Kinh te",              2.8),
    ("Le Hoang Nam",   "Ky thuat dien",        3.2),
    ("Pham Thu Ha",    "Ngon ngu Anh",         1.8),
    ("Do Minh Khoa",   "Cong nghe thong tin",  3.9),
    ("Nguyen Lan Anh", "Quan tri kinh doanh",  2.5),
]
cursor.executemany(
    "INSERT INTO students (name, major, gpa) VALUES (?, ?, ?)",
    students_data
)
conn.commit()
print(f"Da them {len(students_data)} sinh vien.")

# PHAN 3: TRUY VAN
print("\n--- TAT CA SINH VIEN ---")
cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(row)

print("\n--- SINH VIEN CO GPA > 3.0 ---")
cursor.execute("SELECT * FROM students WHERE gpa > 3.0")
for row in cursor.fetchall():
    print(row)

# PHAN 4: CAP NHAT GPA
cursor.execute("UPDATE students SET gpa = ? WHERE name = ?", (3.7, "Tran Thi Binh"))
conn.commit()
print("\nDa cap nhat GPA cua Tran Thi Binh -> 3.7")

# PHAN 5: XOA SINH VIEN GPA < 2.0
cursor.execute("SELECT name, gpa FROM students WHERE gpa < 2.0")
to_delete = cursor.fetchall()
cursor.execute("DELETE FROM students WHERE gpa < 2.0")
conn.commit()
print(f"\nDa xoa {len(to_delete)} sinh vien co GPA < 2.0: {to_delete}")

print("\n--- DANH SACH CUOI CUNG ---")
cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(row)

conn.close()
print("\nDong ket noi.")