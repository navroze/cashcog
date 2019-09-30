import requests
import ast
import sys
from cashcog.serializers.expense_serializer import ExpenseSchema
from marshmallow import ValidationError, pprint
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/cashcog')


def validate_payload(payload):
    db = client.expenses_db
    try:
        schema = ExpenseSchema()
        schema.load(payload)
        payload["is_validated"] = True
        db.expenses.insert_one(payload)
    except ValidationError as ve:
        payload["errors"] = ve.messages
        pprint(ve)
        db.expenses_errors.insert_one(payload)


def main():
    print("Started consumer press Ctrl+C to terminate")
    try:
        r = requests.get('https://cashcog.xcnt.io/stream', stream=True)
        for line in r.iter_lines():
            decoded_line = line.decode('utf-8')
            payload = ast.literal_eval(decoded_line)
            validate_payload(payload)
    except KeyboardInterrupt:
        print("\nStopped consumer!")
        sys.exit()


if __name__ == '__main__':
    main()