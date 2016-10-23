from flask import Flask, render_template, jsonify

from pymongo import MongoClient

app = Flask(__name__)


@app.route('/')
def hello_world():
    """Saluda al usuario"""
    return render_template('index.html')


@app.route('/greet/<name>')
def greet(name):
    "Saluda al usuario con su nombre"
    return render_template('greet.html', name=name.capitalize())


@app.route('/greet/<name>.json')
def greet_json(name):
    """Devuelve el nombre en la ruta en un json"""
    return jsonify(**{
        "greet": name,
    })

# Para conectarnos a MongoDB
client = MongoClient()


@app.route('/user')
def get_user():
    """Devuelve todos los documentos de la
    coleccion 'users' de la base de datos 'test'"""
    users = list(client.
                 test.users
                 .find({}, {"_id": False, "name": True})
                 .limit(100))
    return jsonify(**{
        "data": users,
    })


# Maneja solo peticiones con método 'POST'
@app.route('/user/<name>', methods=['POST'])
def add_user(name):
    """Permite insertar un documento en la coleccion 'users'
    de la base de datos 'test'"""
    new_user = client.test.users.insert_one({"name": name})
    return jsonify(**{
        "done": True,
        "id": new_user.inserted_id,
    })
