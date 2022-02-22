from flask_user import UserMixin
from mongoengine import Document, BooleanField, StringField, ListField


class User(Document, UserMixin):
    active = BooleanField(default=True)

    # User authentication information
    username = StringField(default='')
    password = StringField()

    # User information
    first_name = StringField(default='')
    last_name = StringField(default='')

    # Relationships
    roles = ListField(StringField(), default=[])
