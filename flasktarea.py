from flask import Flask, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

cluster = MongoClient("mongodb+srv://yuli:1234@cluster0.pgbdwnj.mongodb.net/?retryWrites=true&w=majority")
db = cluster["SGC"]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/crear', methods=['POST'])
def crear():
    collection_name = request.form.get('collection')
    collection = db[collection_name]
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    if collection_name == "producto":
        tipo = request.form.get('tipo')
        cantidad = request.form.get('cantidad')
        producto = {"_id": id, "name": nombre, "cantidad": cantidad, "tipo":tipo}
        result = collection.insert_one(producto)
    elif collection_name in ["proovedor", "distribuidor"]:
        ubicacion = request.form.get('ubicacion')
        clasificacion = request.form.get('clasificacion')
        item = {"_id": id, "name": nombre, "ubicacion": ubicacion, "clasificacion":clasificacion}
        result = collection.insert_one(item)
    return 'Item creado con éxito', 200

@app.route('/eliminar', methods=['POST'])
def eliminar():
    collection_name = request.form.get('collection')
    collection = db[collection_name]
    id = request.form.get('id')
    result = collection.delete_one({"_id":id})
    return 'Item eliminado con éxito', 200

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/buscar', methods=['POST'])
def buscar():
    collection_name = request.form.get('collection')
    collection = db[collection_name]
    results = collection.find({})
    return render_template('results.html', results=results)

@app.route('/actualizar', methods=['POST'])
def actualizar():
    collection_name = request.form.get('collection')
    collection = db[collection_name]
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    result = collection.update_one({ "_id":id}, {"$set":{"name": nombre}})
    return 'Item actualizado con éxito', 200

@app.route('/eliminar_todo', methods=['POST'])
def eliminar_todo():
    password = request.form.get('password')
    if password == "admin123":
        collection = db["producto"]
        collection.delete_many({})
        collection = db["proovedor"]
        collection.delete_many({})
        collection = db["distribuidor"]
        collection.delete_many({})
        return 'Todos los items eliminados con éxito', 200
    else:
        return 'Contraseña incorrecta', 403
