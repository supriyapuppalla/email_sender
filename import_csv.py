import csv
from database import Student, SessionLocal, init_db

init_db()

db = SessionLocal()

csv_file_path = 'emails.csv'

with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        student = Student(
            name=row['name'].strip(),
            email=row['email'].strip(),
            department=row['department'].strip()
        )
        db.add(student)

db.commit()
db.close()

print("Data imported from CSV successfully!")
