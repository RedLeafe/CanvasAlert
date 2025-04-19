# CanvasAlert

A hackathon project that lets you log in with Discord, connect your Canvas account via API token, and receive Discord alerts for new Canvas announcements or upcoming assignments.

---

## Demo

Watch our demo here:
[Watch the demo video](./CanvasAlertDemo.mp4)


---

## Features

- **Discord OAuth2 Login**  
  Securely log in with your Discord account.
- **Canvas API Integration**  
  Input your Canvas API token once to grant access.
- **Hourly Cron Job**  
  Checks every hour for:
  - New announcements
  - Upcoming assignments due within your chosen time window
- **Discord Alerts**  
  Sends you a direct message on Discord whenever something new appears.

---

## Tech Stack

- **Backend**: Python (Flask)
- **Database**: MySQL  
- **Scheduler**: cron
- **Authentication**: Discord OAuth2  
- **Canvas API**: REST  
- **Hosting**: To be determined

---
