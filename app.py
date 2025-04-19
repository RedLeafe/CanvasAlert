from flask import Flask, render_template, redirect, request
import db as db

app = Flask(__name__)

db.create_users_table()

@app.route('/')
def hello_world():
   return render_template('index.html')

@app.route('/api', methods=['POST'])
def receive_form():
   discord_id = request.form.get('discord_id')
   canvas_id = request.form.get('canvas_id')
   assignments = request.form.get('assignments_toggle')
   assignments_time = request.form.get('assignment_time')
   discussions = request.form.get('discussions_toggle')
   announcements = request.form.get('announcements_toggle')

   db.updateSettings([discord_id, canvas_id, assignments, assignments_time, discussions, announcements])

   return redirect('/')


if __name__ == '__main__':
   app.run(debug=True)