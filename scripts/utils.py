import uuid
from datetime import datetime

def new_guid():
    return str(uuid.uuid4())

def now():
    return datetime.now().isoformat()