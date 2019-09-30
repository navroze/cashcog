from marshmallow import Schema, fields, ValidationError
from cashcog.utils.currencies import CURRENCIES


def validate_status(status):
    if status != "approve" and status != "decline":
        raise ValidationError("Invalid status passed acceptable values are 'approve' or decline")


def validate_currency(currency):
    if currency.upper() not in CURRENCIES:
        raise ValidationError("Invalid currency passed")


class EmployeeSchema(Schema):
    uuid = fields.UUID(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)


class ExpenseSchema(Schema):
    uuid = fields.UUID(required=True)
    description = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    amount = fields.Integer(required=True)
    currency = fields.String(required=True)
    employee = fields.Nested(EmployeeSchema, required=True)


class QuerySchema(Schema):
    first_name = fields.String()
    last_name = fields.String()
    amount = fields.Integer()
    currency = fields.String(validate=validate_currency)


class ValidateSchema(Schema):
    uuid = fields.UUID(required=True)
    status = fields.String(required=True, validate=validate_status)
