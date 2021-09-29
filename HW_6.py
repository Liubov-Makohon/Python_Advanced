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


# 1.
@app.route('/genres_durations')
def get_genre_durations():
    query = 'select g.Name, sum(t.Milliseconds/1000) as duration ' \
            'from genres as g ' \
            'join tracks as t ' \
            'on g.GenreId = t.GenreId ' \
            'group by g.Name'
    records = execute_query(query)
    result = format_records(records)
    return result


# 2.
@app.route('/greatest_hits')
@use_kwargs(
    {
        'count': fields.Int(
            required=False,
            missing=None,
        ),
    },
    location='query',
)
def get_greatest_hits(count):
    query = 'SELECT t.Name, ii.UnitPrice * sum(ii.Quantity) as Profit, sum(ii.Quantity) as Quantity ' \
            'FROM tracks as t ' \
            'JOIN invoice_items as ii ' \
            'ON t.TrackId = ii.TrackId ' \
            'GROUP BY t.TrackId ' \
            'ORDER BY Quantity desc '

    if count:
        query += ' limit ?'

    records = execute_query(query, (count,))
    result = format_records(records)
    return result

# 3.
@app.route('/greatest_artists')
@use_kwargs(
    {
        'count': fields.Int(
            required=False,
            missing=None,
        ),
    },
    location='query',
)
def get_greatest_artists(count):
    query = 'SELECT art.Name' \
            'FROM invoice_items as ii' \
            'JOIN tracks as t ' \
            'ON ii.TrackId = t.TrackId' \
            'JOIN albums as alb ' \
            'ON t.AlbumId = alb.AlbumId' \
            'JOIN artists as art ' \
            'ON alb.ArtistId = art.ArtistId' \
            'GROUP BY art.ArtistId' \
            'ORDER BY sum(ii.Quantity) DESC'

    if count:
        query += ' limit ?'

    records = execute_query(query, (count,))
    result = format_records(records)
    return result


app.run()


# 5.
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.point = Point(x, y)

    def contains(self, point):
        sqrt_distance = (self.x-point.x)**2 + (self.y-point.y)**2
        return sqrt_distance <= (self.radius)**2

