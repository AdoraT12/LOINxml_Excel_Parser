import uuid
from datetime import datetime

GUID_NAMESPACE = uuid.UUID(
    "8f1b8c34-8d59-4ef6-a2ef-0d6f3a3c9c11"
)

def new_guid():
    return str(uuid.uuid4())

def stable_guid(name):
    return str(uuid.uuid5(GUID_NAMESPACE, name))

def now():
    return datetime.now().isoformat()