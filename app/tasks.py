from app import app, db, celery
from .models import Message
from datetime import datetime, timezone


@celery.task()
def send_messages(current_user, receiver, message):
    m = Message(id=Message.query.count() + 1, uid_receiver=receiver.id, sender=current_user.name,
                date=datetime.now(timezone.utc), message=message)

    db.session.add(m)
    db.session.commit()
