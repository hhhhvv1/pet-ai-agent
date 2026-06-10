import sqlite3

conn = sqlite3.connect("memory.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    species TEXT,
    age INTEGER,
    weight REAL,
    personality TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS health_logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_name TEXT,
    symptom TEXT,
    analysis TEXT,
    risk TEXT,
    risk_score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

print("DB 생성 완료")