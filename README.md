# Google Scheduler

A scheduling app that generates a 2-week Google Calendar schedule based on your activities.

## Setup

Get your own Google OAuth credentials:
- Go to console.cloud.google.com, create a project, enable the Google Calendar API
- Create an OAuth 2.0 Client ID (Desktop app) and download the JSON
- Save it as credentials.json in scheduler/server/

Install backend dependencies (activate your venv first):
```
pip3 install flask flask-restx flask-cors sqlalchemy google-auth google-auth-oauthlib google-api-python-client
```

Install frontend dependencies:
```
cd react_scheduler
npm install
```

## Running

Terminal 1 - Backend:
```
cd scheduler/server
python3 app.py
```

Terminal 2 - Frontend:
```
cd react_scheduler
npm start
```

App runs at http://localhost:3000. The first time you click Generate Schedule, you'll be prompted to sign in with Google.
