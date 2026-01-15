# -----------------------------
# Python Version of Lesson Plan Updater
# -----------------------------

from googleapiclient.discovery import build
from google.oauth2 import service_account
import json

# -----------------------------
# Google Docs API setup
# -----------------------------
SCOPES = ['https://www.googleapis.com/auth/documents']
SERVICE_ACCOUNT_FILE = 'service_account.json'  # Path to your service account JSON file

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('docs', 'v1', credentials=creds)

DOCUMENT_ID = '1mJFVM8TiPce4kJ76P3NKuvn-NwRIZjYJzQt86rIRKJY'  # Your template Google Doc ID

# -----------------------------
# Function to replace placeholders in the Doc
# -----------------------------
def update_lesson_plan(lesson_plan_json):
    """
    Updates a Google Doc template with lesson plan data from a JSON object.
    
    lesson_plan_json: JSON object/dict containing the lesson plan
    """
    requests = []

    # Replace top-level fields
    for field in ["Teacher","Year/Class","Subject","Unit/Topic","Week number","Date"]:
        if field in lesson_plan_json:
            requests.append({
                'replaceAllText': {
                    'containsText': {'text': f'{{{{{field}}}}}', 'matchCase': True},
                    'replaceText': lesson_plan_json[field]
                }
            })

    # Replace class placeholders
    if "Classes" in lesson_plan_json:
        for class_key, class_obj in lesson_plan_json["Classes"].items():
            for placeholder, value in class_obj.items():
                if value:
                    requests.append({
                        'replaceAllText': {
                            'containsText': {'text': f'{{{{{placeholder}}}}}', 'matchCase': True},
                            'replaceText': value
                        }
                    })

    # Execute batch update
    result = service.documents().batchUpdate(
        docu
