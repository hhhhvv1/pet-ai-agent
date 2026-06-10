import sqlite3

conn = sqlite3.connect("memory.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO pets(
    name,
    species,
    age,
    weight,
    personality
)
VALUES(
    '초코',
    '강아지',
    5,
    4.2,
    '예민함'
)
""")

cursor.execute("""
INSERT INTO pets(
    name,
    species,
    age,
    weight,
    personality
)
VALUES(
    '나비',
    '고양이',
    3,
    3.1,
    '식욕이 적음'
)
""")

conn.commit()

print("반려동물 등록 완료!")