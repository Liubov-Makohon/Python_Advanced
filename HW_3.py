import random
import string

import requests
from flask import jsonify

from flask import Flask
from marshmallow import validate
from webargs import fields
from webargs.flaskparser import use_kwargs


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

@app.route("/password")
@use_kwargs(
    {
        "length": fields.Int(
            missing=10,
            validate=[validate.Range(min=1, max=100)]),
        "specials": fields.Bool(
            missing=False,
            validate=[validate.Range(min=0, max=1)]),
        "digits": fields.Bool(
            missing=False,
            validate=[validate.Range(min=0, max=1)]),
    },
    location="query",)

def get_password(length, specials, digits):
    password_characters = string.ascii_lowercase + string.ascii_uppercase

    if specials == True:
        password_characters += '!"№;%:?*$()_+.'

    if digits == True:
        password_characters += string.digits

    return ''.join(random.choices(password_characters, k=length))

@app.route("/bitcoin_rate")
@use_kwargs(
    {
        "currency": fields.Str(
            missing="USD",
            validate=[validate.Regexp('[A-Z]+')]),
    },
    location="query",)

def get_bitcoin_rate(currency):
    url = "https://bitpay.com/api/rates"
    res = requests.get(url)
    result = res.json()
    for entry in result:
        if currency in entry["code"]:
            return str(entry["rate"])


app.run()

