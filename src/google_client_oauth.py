from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from src.main import shift_to_event
SCOPES = ["https://www.googleapis.com/auth/calendar"]
creds = Credentials.from_service_account_file(
    "project1.json",
    scopes=SCOPES
)

service = build("calendar", "v3", credentials=creds)
CALENDAR_ID = "9aa815b6ebb5f9037c87770a0d501a785660bd413e6d680f28e9777d8d77e2ca@group.calendar.google.com"

def event_exists(service, calendar_id, source_id):
    events = service.events().list(
        calendarId=calendar_id,
        q=source_id
    ).execute()

    return len(events.get("items", [])) > 0

def shift_in_schedule(name, schedule):
    list1=[]
    for shift in schedule[name]:
        event = shift_to_event(shift)
        print(event)
        source_id = event["description"].split("source_id:")[1]

        if event_exists(service, CALENDAR_ID, source_id):
            print("Skipping existing:", source_id)
            list1.append("Skipping existing: "+ source_id)
            continue

        service.events().insert(
            calendarId=CALENDAR_ID,
            body=event
        ).execute()

        print("Inserted:", source_id)
        list1.append("Inserted: "+ source_id)

    return list1