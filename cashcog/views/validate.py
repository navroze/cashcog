from flask.views import MethodView
from flask import request, jsonify
from marshmallow import ValidationError
from cashcog.serializers.expense_serializer import ValidateSchema
from cashcog import db


class ValidateView(MethodView):

    def post(self):
        try:
            request_data = request.json
            schema = ValidateSchema()
            schema.load(request_data)
            find_query = {
                "uuid": request_data["uuid"]
            }
            update_query = {
                "$set": {
                    "status": request_data["status"]
                }
            }
            result = db.expenses.update_one(find_query, update_query)
            if result.matched_count == 0:
                return jsonify(({"success": False, "message": "Could not find expense"})), 404
            if result.modified_count == 1:
                return jsonify(({"success": True, "status": request_data["status"]})), 200
            return jsonify({"success": False}), 200
        except ValidationError as ve:
            return jsonify({"errors": ve.messages}), 400
