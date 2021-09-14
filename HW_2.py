import faker
from flask import Flask

app = Flask(__name__)

@app.route("/pipfile")
def get_pipfile():
    with open("Pipfile.lock", "r") as f:
        data = f.read()
    return data

@app.route("/random_students")
def get_random_students():
    f = faker.Faker("UK")
    name = [(f.first_name() + " " + f.last_name()) for _ in range(10)]
    return str(name)

app.run()