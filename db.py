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

    query = """
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
    cursor.execute(query, values)
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

    create_table_query = """
    CREATE TABLE IF NOT EXISTS assignments (
        discord_id VARCHAR(100),
        assignment_name VARCHAR(255),
        due_date VARCHAR(100),
        PRIMARY KEY (discord_id, assignment_name),
        FOREIGN KEY (discord_id) REFERENCES users(discord_id)
    );
    """
    cursor.execute(create_table_query)

    create_table_query = """
    CREATE TABLE IF NOT EXISTS announcements (
        discord_id VARCHAR(100),
        announcement_name VARCHAR(255),
        PRIMARY KEY (discord_id, announcement_name),
        FOREIGN KEY (discord_id) REFERENCES users(discord_id)
    );
    """
    cursor.execute(create_table_query)

    create_table_query = """
    CREATE TABLE IF NOT EXISTS discussions (
        discord_id VARCHAR(100),
        discussion_name VARCHAR(255),
        PRIMARY KEY (discord_id, discussion_name),
        FOREIGN KEY (discord_id) REFERENCES users(discord_id)
    );
    """
    cursor.execute(create_table_query)

    conn.commit()
    cursor.close()
    conn.close()
    

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="canvas",
        charset="utf8mb4",
        collation="utf8mb4_unicode_520_ci"
    )

def selectAssignments(discord_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT assignment_name FROM assignments WHERE discord_id = %s"
    cursor.execute(query, (discord_id,))

    results = cursor.fetchall()
    assignment_names = [row[0] for row in results]

    cursor.close()
    conn.close()
    
    return assignment_names

def selectAnnouncements(discord_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT announcement_name FROM announcements WHERE discord_id = %s"
    cursor.execute(query, (discord_id,))

    results = cursor.fetchall()
    announcement_names = [row[0] for row in results]

    cursor.close()
    conn.close()
    
    return announcement_names

def selectDiscussions(discord_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT discussion_name FROM discussions WHERE discord_id = %s"
    cursor.execute(query, (discord_id,))

    results = cursor.fetchall()
    discussion_names = [row[0] for row in results]

    cursor.close()
    conn.close()
    
    return discussion_names

def updateAssignments(discord_id, assignment_name, assignments_time):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO assignments (discord_id, assignment_name, due_date)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
        due_date = VALUES(due_date)
    """
    cursor.execute(query, (discord_id, assignment_name, assignments_time))
    conn.commit()
    cursor.close()
    conn.close()


def updateAnnouncements(discord_id, announcement_name):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO announcements (discord_id, announcement_name)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE
        announcement_name = VALUES(announcement_name)
    """
    cursor.execute(query, (discord_id, announcement_name))
    conn.commit()
    cursor.close()
    conn.close()


def updateDiscussions(discord_id, discussion_name):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO discussions (discord_id, discussion_name)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE
        discussion_name = VALUES(discussion_name)
    """
    cursor.execute(query, (discord_id, discussion_name))
    conn.commit()
    cursor.close()
    conn.close()
