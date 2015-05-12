
import sys
sys.path.append('../')

from flask import Flask, jsonify, render_template, request, json, Response, Blueprint
from database import Database
app = Flask(__name__)

front_end = Blueprint('simple_page', __name__,
                      template_folder='templates')

db = Database()

@app.route('/')
def index():
    return render_template('index.html')

class Field:
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type

"""
Gets all fields available for the table, these are the
variables that we can toggle with
"""
@app.route('/_get_fields')
def get_fields():
    fields = map(lambda entry: entry[1], db.get_fields())
    return Response(json.dumps(fields),  mimetype='application/json')

@app.route('/_query_info')
def query_info():
    field = request.args.get('field', 0, type=str)
    if field == "null":
        field = "age"
    return Response(json.dumps(db.query_info(field)),  mimetype='application/json')

@app.route('/_get_variable_count')
def get_variable_count():
    field = request.args.get('field', 0, type=str)
    total_rows = int(db.field_var_count(field)[0])
    missing_rows = total_rows - 100 if total_rows > 100 else 0
    return Response(json.dumps(missing_rows),  mimetype='application/json')

if __name__ == '__main__':
    app.run()

get_variable_count()