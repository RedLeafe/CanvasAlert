from flask import Flask, render_template, redirect, request, url_for, session
from flask_session import Session
from urllib.parse import urlencode
from dotenv import load_dotenv
import os
import json
import requests
import db as db

app = Flask(__name__)

# Add this line to set the secret key
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")


# Load dotenv variables
load_dotenv()

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_OAUTH_AUTHORIZE_URL = "https://discord.com/api/oauth2/authorize"
DISCORD_OAUTH_TOKEN_URL = "https://discord.com/api/oauth2/token"
SCOPE = "identify email"



# Define a route for the homepage ("/")
HAS_DB = os.getenv("HAS_DB", "False").lower() == "true"

if HAS_DB:
   db.create_users_table()

@app.route('/')
def hello_world():
   user = session.get("user")
   if not user:
       # Redirect to Discord OAuth if not logged in
      return redirect(make_OAuth2_url("{}")) 
   return render_template('index.html', user=user)


def make_redirect(target: str):
   return redirect(target)

def make_OAuth2_url(state: str) -> str:
   params = {
      "client_id": DISCORD_CLIENT_ID,
      "redirect_uri": DISCORD_REDIRECT_URI,
      "response_type": "code",
      "scope": SCOPE,
      "state": state,
   }
   return f'{DISCORD_OAUTH_AUTHORIZE_URL}?{urlencode(params)}'

def get_discord_user_from_code(code: str) -> dict | None:
    """
    Exchange authorization code for an access token, then fetch user info.
    """
    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
        "scope": SCOPE,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_resp = requests.post(DISCORD_OAUTH_TOKEN_URL, data=data, headers=headers)
    if not token_resp.ok:
        return None
    token_json = token_resp.json()
    access_token = token_json.get("access_token")

    # Fetch Discord user
    user_resp = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    if not user_resp.ok:
        return None
    return user_resp.json()

@app.route('/Discord_OAuth')
def discord_oauth():
   raw_state = request.args.get("state", "{}")
   try:
      state = json.loads(raw_state)
   except json.JSONDecodeError:
      state = {}
   destination = state.get("destination", "/")

    # If user already logged in, redirect
   if session.get("user"):
      return make_redirect(destination)

    # Check for authorization code
   code = request.args.get("code")
   if not code:
      # Store state for callback
      session["oauth_state"] = raw_state
      # Redirect user to Discord's OAuth2 URL
      return make_redirect(make_OAuth2_url(raw_state))

   # Exchange code for user info
   discord_user = get_discord_user_from_code(code)
   if not discord_user:
      return "Failed to get user from code.", 400

   # Save to session and redirect
   session["user"] = discord_user
   return make_redirect(destination)

@app.route('/api', methods=['POST'])
def receive_form():
   discord_id = session.get("user").id
   canvas_id = request.form.get('canvas_id')
   assignments = request.form.get('assignments_toggle')
   assignments_time = request.form.get('assignment_time')
   discussions = request.form.get('discussions_toggle')
   announcements = request.form.get('announcements_toggle')

   db.updateSettings([discord_id, canvas_id, assignments, assignments_time, discussions, announcements])

   return redirect('/')


if __name__ == '__main__':
   app.run(debug=True)