from flask import jsonify
from flask import Flask
from webargs import fields
from webargs.flaskparser import use_kwargs
from db import execute_query
from utils import format_records

app = Flask(__name__)


@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code


@app.route("/unique_names")
def get_unique_names():
    records = execute_query('select count(distinct FirstName) from customers')[0]
    result = format_records(records)
    return result


@app.route('/tracks_count')
def get_tracks_count():
    records = execute_query('select count(TrackId) from tracks')[0]
    result = format_records(records)
    return result


@app.route('/customers')
@use_kwargs(
    {
        'text': fields.Str(
            required=False,
            missing=None,
        ),
    },
    location='query',
)
def get_customers(text):
    query = 'select * from customers'
    text_column_name = ['FirstName', 'LastName', 'Company', 'Address', 'City', 'State', 'Country', 'Email']
    if text:
        query += ' WHERE ' + ' OR '.join((f'{k} like ?', (text,)) for k in text_column_name)

    records = execute_query(query)
    result = format_records(records)
    return result

app.run()