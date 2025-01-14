import requests

API_URL = "http://localhost:8000"
EMAIL = None
PASSWORD = None

def set_credentials(email, password):
    """Set the email and password for the user.
    
    Args:
        email (str): The email for the user.
        password (str): The password for the user.
    """
    EMAIL = email
    PASSWORD = password


def create_event(name, start, end, notes=None):
    """Create an event.
    
    Args:
        name (str): The name of the event.
        start (str): The start time for the event, must be formatted as 'YYYY-MM-DDTHH:MM:SS'.
        end (str): The end time for the event, must be formatted as 'YYYY-MM-DDTHH:MM:SS'.
        notes (str): Optional notes for the event.
    """
    if not EMAIL or not PASSWORD:
        raise Exception("Email and password must be set before creating an event.")
    
    data = {
        "email": EMAIL,
        "password": PASSWORD,
        "name": name,
        "start": start,
        "end": end
    }
    
    if notes:
        data["notes"] = notes
    
    response = requests.post(f"{API_URL}/event", json=data)
    
    if response.status_code != 200:
        raise Exception(f"Failed to create event: {response.text}")

    return "Event created successfully"


def get_events(start=None, end=None, search_string=None):
    """Get a list of events.
    
    Args:
        start (str): The start time to filter events by, must be formatted as 'YYYY-MM-DDTHH:MM:SS'.
        end (str): The end time to filter events by, must be formatted as 'YYYY-MM-DDTHH:MM:SS'.
        search_string (str): A string to search for in the event name or notes.
    """
    if not EMAIL or not PASSWORD:
        raise Exception("Email and password must be set before getting events.")
    
    data = {
        "email": EMAIL,
        "password": PASSWORD
    }
    
    if start:
        data["start"] = start
    if end:
        data["end"] = end
    if search_string:
        data["search_string"] = search_string
    
    response = requests.post(f"{API_URL}/events", json=data)
    
    if response.status_code != 200:
        raise Exception(f"Failed to get events: {response.text}")
    
    return response.json()