"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Planeta, User, People, Favoritos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users_list():
    user_db = User.query.all()
    response_body = [(user.serialize()) for user in user_db]
    return jsonify(response_body), 200

@app.route('/User/<int:User_id>', methods=['GET'])
def get_user(User_id):
    user = User.query.get(User_id)
    if not user:
        return jsonify({"msg": "no encontramos al usuario"}), 400
    return jsonify(user.serialize()), 200

@app.route('/Planeta/<int:Planeta_id>', methods=['GET'])
def get_planeta(Planeta_id):
    planeta= Planeta.query.get(Planeta_id)
    if not planeta:
        return jsonify({"msg": "no encontramos el planeta con ese id"}), 400
    return jsonify(planeta.serialize()), 200

@app.route('/People/<int:People_id>', methods=['GET'])
def get_people(People_id):
    people= People.query.get(People_id)
    if not people:
        return jsonify({"msg": "no encontramos al personaje"}), 400
    return jsonify(people.serialize())

@app.route('/Favoritos', methods=['POST'])
def add_favorito():
    data= request.get_json()
    user_id = data.get('user_id')
    planeta_id = data.get('planeta_id')
    people_id = data.get('people_id')

    if not user_id or (not planeta_id and not people_id):
        return jsonify({"error": "user_id y (planeta_id o people_id) son requeridos"}), 400
    nuevo_favorito = Favoritos(user_id = user_id, planeta_id = planeta_id, people_id = people_id)
    db.session.add(nuevo_favorito)
    db.session.commit()
    return jsonify({"msg": "Favorito agregado correctamente"}), 200

@app.route('/Favoritos', methods=['DELETE'])
def eliminar_favorito():
    data = request.get_json()
    user_id = data.get('user_id')
    planeta_id = data.get('planeta_id')
    people_id = data.get('people_id')

    if not user_id or (not planeta_id and not people_id):
        return jsonify({"error": "user_id y (planeta_id o people_id) son requeridos"}), 400
    
    favorito = Favoritos.query.filter_by(user_id = user_id, planeta_id = planeta_id, people_id = people_id).first()
    if not favorito:
        return jsonify({"error": "favorito no encontrado"}), 400
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"msg": "Favorito eliminado correctamente"}), 200


@app.route('/People/<int:People_id>', methods=['DELETE'])
def delete_people(people_id):
    people = People .query.get(people_id)
    if people:
        db.session.commit()
        return jsonify('personaje borrado exitosamente'), 200
    return jsonify('el personaje no existe ne la base de datos'),404

@app.route('/Planeta/<int:Planet_id>', methods=['DELETE'])
def delete_planeta(planeta_id):
    planeta = Planeta.query.get(planeta_id)
    if planeta:
        db.session.commit()
        return jsonify('planeta borrado'), 200
    return jsonify('no se econtro al planeta'),404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
