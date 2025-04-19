import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="canvas",
        charset="utf8mb4",
        collation="utf8mb4_unicode_520_ci"
    )

def getTable():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def getRow(discord_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE discord_id = %s"
    cursor.execute(query, (discord_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def getOne(column, discord_id):
    allowed_columns = {"canvas_key", "assignments", "assignments_time", "discussions", "announcements"}
    if column not in allowed_columns:
        raise ValueError("Invalid column name")

    conn = get_connection()
    cursor = conn.cursor()
    query = f"SELECT {column} FROM users WHERE discord_id = %s"
    cursor.execute(query, (discord_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def updateSettings(settings):
    discord_id, canvas_id, assignments, assignments_time, discussions, announcements = settings

    assignments = 1 if assignments == "on" else 0
    discussions = 1 if discussions == "on" else 0
    announcements = 1 if announcements == "on" else 0

    conn = get_connection()
    cursor = conn.cursor()

    upsert_query = """
    INSERT INTO users (
        discord_id,
        canvas_key,
        assignments,
        assignments_time,
        discussions,
        announcements
    ) VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        canvas_key = VALUES(canvas_key),
        assignments = VALUES(assignments),
        assignments_time = VALUES(assignments_time),
        discussions = VALUES(discussions),
        announcements = VALUES(announcements)
    """

    values = (discord_id, canvas_id, assignments, assignments_time, discussions, announcements)
    cursor.execute(upsert_query, values)
    conn.commit()
    cursor.close()
    conn.close()

def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        discord_id VARCHAR(100) PRIMARY KEY,
        canvas_key VARCHAR(100),
        assignments BOOLEAN DEFAULT TRUE,
        assignments_time INT,
        discussions BOOLEAN DEFAULT TRUE,
        announcements BOOLEAN DEFAULT TRUE
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()