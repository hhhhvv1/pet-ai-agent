import sqlite3

conn = sqlite3.connect("memory.db")
cursor = conn.cursor()


def get_recent_history(pet_name, limit=5):

    cursor.execute("""
    SELECT symptom,risk
    FROM health_logs
    WHERE pet_name=?
    ORDER BY id DESC
    LIMIT ?
    """,
    (pet_name, limit))

    return cursor.fetchall()


def get_all_history(pet_name):

    cursor.execute("""
    SELECT created_at,symptom,risk
    FROM health_logs
    WHERE pet_name=?
    ORDER BY id DESC
    """,
    (pet_name,))

    return cursor.fetchall()


def symptom_trend(pet_name):

    cursor.execute(
        """
        SELECT symptom,risk,created_at
        FROM health_logs
        WHERE pet_name=?
        ORDER BY id DESC
        LIMIT 5
        """,
        (pet_name,)
    )

    return cursor.fetchall()