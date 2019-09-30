from datetime import datetime

from mongoengine import Document, DynamicDocument, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, StringField,IntField, DictField,
    EmbeddedDocumentField, UUIDField
)


class Employee(EmbeddedDocument):
    uuid = UUIDField()
    first_name = StringField()
    last_name = StringField()


class Expenses(DynamicDocument):
    uuid = UUIDField()
    description = StringField()
    created_at = StringField()
    amount = IntField()
    currency = IntField()
    employee = EmbeddedDocumentField(Employee)
    meta = {
        'collection': 'expenses'
    }

