from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class Book(Document):
    title = StringField(required=True)
    author = StringField()
    summary = StringField()
    added_on = DateTimeField(default=datetime.utcnow)