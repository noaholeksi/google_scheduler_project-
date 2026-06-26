# import datetime
# import os.path

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# # If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/calendar"]

# def add_events(service, events):
#     calendar_id = 'primary'
#     for event in events:
#         event_scheduled = service.events().insert(calendarId = calendar_id, body = event).execute()

# def clear_events(service):
#     print("clearing")
#     now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time
#     events_result = (service.events().list(
#                 calendarId="primary",
#                 timeMin=now,
#                 singleEvents=True,
#                 orderBy="startTime",
#             ).execute())
#     events = events_result.get("items", [])

#     ids_to_delete = []
#     for event in events:
#         if event['description'] == "****":
#             ids_to_delete.append(event['id'])
#             print(f"deleting {event['summary']}")
    
#     for id in ids_to_delete:
#         try: 
#             service.events().delete(calendarId='primary', eventId= id).execute()
#         except Exception as e:
#             print(f"theres been an errer: {e}")




# def view_10(service):
#     print("Getting the upcoming 10 events")
#     now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time
#     events_result = (service.events().list(
#                 calendarId="primary",
#                 timeMin=now,
#                 maxResults=10,
#                 singleEvents=True,
#                 orderBy="startTime",
#             ).execute())
#     events = events_result.get("items", [])

#     if not events:
#         print("No upcoming events found.")
#         return

#         # Prints the start and name of the next 10 events
#     for event in events:
#         start = event["start"].get("dateTime", event["start"].get("date"))
#         print(start, event["summary"])

# def run_calendar_api(events, length = 14):
#     """Shows basic usage of the Google Calendar API.
#     Prints the start and name of the next 10 events on the user's calendar.
#     """
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             try:
#                 creds.refresh(Request())
#             except Exception as e:
#                 print(f"Error refreshing credentials: {e}")
#                 return
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     try:
#         service = build("calendar", "v3", credentials=creds)
        

#         clear_events(service)                                
#         add_events(service, events)  
#         #       
        

#     except HttpError as error:
#         print(f"An error occurred: {error}")

# if __name__ == "__main__":
#     run_calendar_api()
import datetime
import os.path
import logging
import traceback

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# configure logging to stdout with debug level
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s"
)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def clear_events(service):
    logging.debug("Entering clear_events")
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC
    try:
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        items = events_result.get("items", [])
    except Exception:
        logging.exception("Failed to list events")
        raise

    ids_to_delete = []
    for ev in items:
        try:
            if ev['description'] == "****":
                ids_to_delete.append(ev['id'])
                logging.info(f"Marked for deletion: {ev.get('summary','<no title>')}")
        except KeyError:
            logging.error("Missing 'description' key in event: %r", ev)

    for eid in ids_to_delete:
        try:
            service.events().delete(calendarId='primary', eventId=eid).execute()
            logging.info(f"Deleted event {eid}")
        except Exception:
            logging.exception(f"Failed to delete event {eid}")


def add_events(service, events):
    logging.debug("Entering add_events with %d events", len(events))
    for event in events:
        try:
            logging.debug("Inserting event: %r", event)
            service.events().insert(calendarId='primary', body=event).execute()
            logging.info("Inserted event: %s", event.get('summary'))
        except Exception:
            logging.exception("Error inserting event")


def view_10(service):
    print("Getting the upcoming 10 events")
    now = datetime.datetime.now().isoformat() + "Z"
    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])


def run_calendar_api(events, length=14):
    logging.debug("Starting run_calendar_api")
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                logging.exception(f"Error refreshing credentials: {e}")
                return
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        clear_events(service)
        add_events(service, events)
    except HttpError as error:
        logging.exception(f"An API error occurred: {error}")
        raise
    except Exception as e:
        logging.error(f"Unhandled exception in run_calendar_api: {e}")
        logging.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    # TODO: build or load a real 'events' list before calling
    example_events = []
    run_calendar_api(example_events)
