from flask.views import MethodView
from flask import request, jsonify
from marshmallow import ValidationError
from cashcog.serializers.expense_serializer import QuerySchema
from cashcog import db


def convert_to_db_query(query_params, db_query):

    if 'first_name' in query_params:
        db_query["employee.first_name"] = query_params["first_name"]

    if 'last_name' in query_params:
        db_query["employee.last_name"] = query_params["last_name"]

    if 'amount' in query_params:
        db_query["amount"] = query_params["amount"]

    if 'currency' in query_params:
        db_query["currency"] = query_params["currency"]


def parse_response(expenses):
    response = []
    for expense in expenses:
        expense_obj = {
            "uuid": expense["uuid"],
            "first_name": expense["employee"]["first_name"],
            "last_name": expense["employee"]["last_name"],
            "description": expense["description"],
            "currency": expense["currency"],
            "amount": expense["amount"]
        }
        response.append(expense_obj)
    return response


class ExpensesView(MethodView):

    def get(self):
        try:
            query_params = request.values.to_dict()
            db_query = {"$and": [{"status": {"$exists": False}}]}
            schema = QuerySchema()
            if query_params:
                query_params = schema.load(query_params)
                convert_to_db_query(query_params, db_query)
            project_query = {
                "uuid": 1,
                "employee.first_name": 1,
                "employee.last_name": 1,
                "description": 1,
                "amount": 1,
                "currency": 1
            }
            expenses = db.expenses.find(db_query, project_query)
            result = parse_response(expenses)
            if len(result) <= 0:
                return jsonify({"data": result}), 404
            return jsonify({"data": result}), 200
        except ValidationError as ve:
            return jsonify({"errors": ve.messages}), 400
        except Exception as e:
            print(e)
            return jsonify({"errors": "Something went wrong"}), 400
