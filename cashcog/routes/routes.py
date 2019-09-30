from cashcog import app
from cashcog.views.expenses import ExpensesView
from cashcog.views.validate import ValidateView


@app.route("/", methods=["GET"])
def send_index_page():
    return app.send_static_file('index.html')


app.add_url_rule(
    '/query/',
    view_func=ExpensesView.as_view("expeneses_view")
)
app.add_url_rule(
    '/validate/',
    view_func=ValidateView.as_view("validate_view")
)