from flask import current_app
from datetime import datetime


@current_app.context_processor
def inject_now():
    return {"now": datetime.utcnow().year}
