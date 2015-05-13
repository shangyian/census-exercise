import sys
sys.path.append('../')

from flask import Flask, jsonify, render_template, request, json, Response, Blueprint
from database import Database

app = Flask(__name__)
app.config.from_pyfile('census.settings')

db = Database(app.config['DATABASE_URI'],\
              app.config['MAIN_TABLE'],\
              app.config['COL_TO_AVG'],\
              app.config['VAR_LIMIT'])

"""
Renders the main page
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
Gets all fields available for the table, these are the
variables that we can toggle with
"""
@app.route('/_get_fields')
def get_fields():
    fields = map(lambda entry: entry[1], db.get_fields())
    return Response(json.dumps(fields),  mimetype='application/json')

"""
Gets the row data for a specific field (in this case it includes
the value, the row count and average age)
"""
@app.route('/_query_info')
def query_info():
    field = request.args.get('field', 0, type=str)
    if field == "null":
        field = "age"
    return Response(json.dumps(db.query_info(field)),  mimetype='application/json')

"""
Gets the hidden value count for a given field
"""
@app.route('/_get_hidden_count')
def get_hidden_count():
    field = request.args.get('field', 0, type=str)
    total_rows = int(db.field_var_count(field)[0])
    limit_value = int(app.config['VAR_LIMIT'])
    hidden_rows = total_rows - limit_value if total_rows > limit_value else 0
    return Response(json.dumps(hidden_rows),  mimetype='application/json')

"""
Gets the hidden row count for a given field
"""
@app.route('/_get_hidden_row_count')
def get_hidden_row_count():
    field = request.args.get('field', 0, type=str)
    return Response(json.dumps(int(db.hidden_row_count(field)[0])), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
