import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

conn = mysql.connector.connect(
    host="localhost",
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database="canvas"
)

cursor = conn.cursor()

def getTable():
    cursor.execute("SELECT * FROM canvas")
    rows = cursor.fetchall()
    return rows

def getRow(discord_id):
    query = "SELECT * FROM canvas WHERE discord_id = ?"
    cursor.execute(query, (discord_id,))
    result = cursor.fetchone()
    return result

def getOne(column, discord_id)
    query = f"SELECT {column} FROM canvas WHERE discord_id = ?"
    cursor.execute(query, (discord_id,))
    result = cursor.fetchone()
    return result

def updateSettings(settings):
    discord_id = settings[0]
    canvas_id = settings[1]
    assignments = settings[2]
    assignments_time = settings[3]
    discussions = settings[4]
    announcements = settings[5]

    update_query = f"""
    UPDATE canvas
    SET
        canvas_key = '{canvas_id}',
        assignments = {assignments},
        assignments_time = {assignments_time},
        discussions = {discussions},
        announcements = {announcements}
    WHERE
        discord_id = '{discord_id}';
    """

    cursor.execute(update_query)
    conn.commit()

cursor.close()
conn.close()
