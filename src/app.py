import os
from flask import Flask, request, jsonify, url_for
from sqlalchemy import select
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from admin import setup_admin
from models import db, Characters, Planets, Vehicles, User, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

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

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'El usuario ya existe'}), 400
    
    new_user = User(email=email, password=password)  # Guardado en texto plano
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuario registrado exitosamente'}), 201

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "aitorsantos90@gmail.com" or password != "admin123":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

#endpoint para obtener todos los personajes
@app.route('/character', methods=['GET'])
def get_all_characters():
    data = db.session.scalars(select(Characters)).all()
    if not data:  
        return jsonify({"error": "No characters found"}), 404
    results = list(map(lambda item: item.serialize(), data))
    response_body = {
        "results":results
    }
    return jsonify(response_body), 200

#endpoint para obtener todos los planetas
@app.route('/planet', methods=['GET'])
def get_all_planets():
    data = db.session.scalars(select(Planets)).all()
    if not data:  
        return jsonify({"error": "No planets found"}), 404
    results = list(map(lambda item: item.serialize(), data))
    response_body = {
        "results":results
    }
    return jsonify(response_body), 200

#endpoint para obtener todos los vehiculos
@app.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    data = db.session.scalars(select(Vehicles)).all()
    if not data:  
        return jsonify({"error": "No vehicles found"}), 404
    results = list(map(lambda item: item.serialize(), data))
    response_body = {
        "results":results
    }
    return jsonify(response_body), 200

#endpoint para ontener un solo usuario
@app.route('/user/<int:id>', methods=['GET'])
def get_single_user(id):
    try:
        user = db.session.execute(select(User).filter_by(id=id)).scalar_one()
        response_body = {
            "result": user.serialize()
        }
        return jsonify(response_body), 200
    except:
        return jsonify({"msg": "user does not exist"}), 404

#endpoint para ontener un solo personaje
@app.route('/character/<int:id>', methods=['GET'])
def get_single_character(id):
    try:
        user = db.session.execute(select(Characters).filter_by(id=id)).scalar_one()
        response_body = {
            "result": user.serialize()
        }
        return jsonify(response_body), 200
    except:
        return jsonify({"msg": "character does not exist"}), 404
    
#endpoint para obtener un solo planeta
@app.route('/planet/<int:id>', methods=['GET'])
def get_single_planet(id):
    try:
        user = db.session.execute(select(Planets).filter_by(id=id)).scalar_one()
        response_body = {
            "result": user.serialize()
        }
        return jsonify(response_body), 200
    except:
        return jsonify({"msg": "planet does not exist"}), 404

#endpoint para obteren un solo vehicluo
@app.route('/vehicle/<int:id>', methods=['GET'])
def get_single_vehicle(id):
    try:
        user = db.session.execute(select(Vehicles).filter_by(id=id)).scalar_one()
        response_body = {
            "result": user.serialize()
        }
        return jsonify(response_body), 200
    except:
        return jsonify({"msg": "vechicle does not exist"}), 404

#endpoint para agregar un user
@app.route('/user', methods=['POST'])
def create_user():
    request_data = request.json
    if "email" not in request_data or "password" not in request_data:
        return jsonify({"error": "Email and password are required"}), 400   
    existing_user = User.query.filter_by(email=request_data["email"]).first()
    if existing_user:
        return jsonify({"error": "Email is already registered"}), 400   
    user = User(email=request_data["email"], password=request_data["password"])
    db.session.add(user)
    db.session.commit()
    response_body = {
        "msg": f"user with ID {user.id} created"
    }
    return jsonify(response_body), 200

#endpoint para agregar un character
@app.route('/character', methods=['POST'])
def create_character():
    request_data = request.json
    existing_character = Characters.query.filter_by(name=request_data["name"]).first()
    if existing_character:
            return jsonify({"error": "Character with this name already exists"}), 400
    user = Characters(name=request_data["name"], birth_year=request_data["birth_year"], height=request_data["height"], skin_color=request_data["skin_color"], eye_color=request_data["eye_color"])
    db.session.add(user)
    db.session.commit()
    response_body = {
        "msg": f"character with ID {user.id} created"
    }
    return jsonify(response_body), 200

#endpoint para agregar un planeta
@app.route('/planet', methods=['POST'])
def create_planet():
    request_data = request.json
    existing_character = Planets.query.filter_by(name=request_data["name"]).first()
    if existing_character:
            return jsonify({"error": "Planet with this name already exists"}), 400
    user = Planets(name=request_data["name"], climate=request_data["climate"], diameter=request_data["diameter"], population=request_data["population"], terrain=request_data["terrain"])
    db.session.add(user)
    db.session.commit()
    response_body = {
        "msg": f"planet with ID {user.id} created"
    }
    return jsonify(response_body), 200

#endpoint para agregar un vehiculo
@app.route('/vehicle', methods=['POST'])
def create_vehicle():
    request_data = request.json
    existing_vehicle = Vehicles.query.filter_by(name=request_data["name"]).first()
    if existing_vehicle:
            return jsonify({"error": "Vehicle with this name already exists"}), 400
    user = Vehicles(name=request_data["name"], model=request_data["model"], cargo_capacity=request_data["cargo_capacity"], length=request_data["length"], passengers=request_data["passengers"])
    db.session.add(user)
    db.session.commit()
    response_body = {
        "msg": f"vehicle with ID {user.id} created"
    }
    return jsonify(response_body), 200

#endpoint para borrar un usuario
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one_or_none()
        if not user:
            return jsonify({"error": "User not found"}), 404
        db.session.delete(user)
        db.session.commit()
        response_body = {
            "msg": f"User {user.email} with ID {user.id} was deleted, along with their favorites."
        }
        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#endpoint para borrar un personaje
@app.route('/character/<int:id>', methods=['DELETE'])
def delete_character(id):
    user = db.session.execute(db.select(Characters).filter_by(id=id)).scalar_one_or_none()
    if not user:
        return jsonify({"error": "Character not found"}), 404
    db.session.delete(user)
    db.session.commit()
    response_body = {
        "msg":f"character with {user.id}, named {user.name} deleted"
    }
    return jsonify(response_body), 200

#endpoint para borrar un planeta
@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    user = db.session.execute(db.select(Planets).filter_by(id=id)).scalar_one_or_none()
    if not user:
        return jsonify({"error": "Planet not found"}), 404
    db.session.delete(user)
    db.session.commit()
    response_body = {
        "msg":f"Planet with {user.id}, named {user.name} deleted"
    }
    return jsonify(response_body), 200

#endpoint para borrar un vehiculo
@app.route('/vehicle/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    user = db.session.execute(db.select(Vehicles).filter_by(id=id)).scalar_one_or_none()
    if not user:
        return jsonify({"error": "Vehicle not found"}), 404
    db.session.delete(user)
    db.session.commit()
    response_body = {
        "msg":f"Vehicle with {user.id}, named {user.name} deleted"
    }
    return jsonify(response_body), 200

#endpoint para obtener todos los favoritos de un usuario
@app.route('/user/<int:user_id>/favorite', methods=['GET'])
def get_user_favorites(user_id):
    try:
        # Obtener los planetas favoritos del usuario (planet_id no es nulo)
        favorite_planets = db.session.scalars(select(Favorites).filter_by(user_id=user_id).filter(Favorites.planet_id != None)).all()
        favorite_characters = db.session.scalars(select(Favorites).filter_by(user_id=user_id).filter(Favorites.character_id != None)).all()
        favorite_vehicles = db.session.scalars(select(Favorites).filter_by(user_id=user_id).filter(Favorites.vehicle_id != None)).all()

        # Extraer solo los nombres de los planetas, personajes y vehículos favoritos
        favorite_planets_names = [planet.planet.name for planet in favorite_planets if planet.planet]  # Verifica que exista la relación
        favorite_characters_names = [character.character.name for character in favorite_characters if character.character]  # Verifica que exista la relación
        favorite_vehicles_names = [vehicle.vehicle.name for vehicle in favorite_vehicles if vehicle.vehicle]  # Verifica que exista la relación

        response_body = {
            "favorite_planets": favorite_planets_names,
            "favorite_characters": favorite_characters_names,
            "favorite_vehicles": favorite_vehicles_names
        }

        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Agregar un personaje a favoritos de un usuario 
@app.route('/favorite/character/<int:user_id>/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    try:
        character = db.session.execute(select(Characters).filter_by(id=character_id)).scalar_one_or_none()
        if not character:
            return jsonify({"error": f"Character with ID {character_id} not found."}), 404
        existing_favorite = db.session.execute(select(Favorites).filter_by(user_id=user_id, character_id=character_id)).scalar_one_or_none()
        if existing_favorite:
            return jsonify({"error": "This character is already in your favorites."}), 400

        #añadir el personaje a los favoritos
        new_favorite = Favorites(user_id=user_id, character_id=character_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({"msg": f"Character {character_id} added to user {user_id}'s favorites."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Agregar un planeta a favoritos de un usuario 
@app.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    try:
        #verificar si el planeta ya está en los favoritos
        existing_favorite = db.session.execute(select(Favorites).filter_by(user_id=user_id, planet_id=planet_id)).scalar_one_or_none()
        if existing_favorite:
            return jsonify({"error": "This planet is already in your favorites."}), 400

        #añadir el planeta a los favoritos
        new_favorite = Favorites(user_id=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({"msg": f"Planet {planet_id} added to user {user_id}'s favorites."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Agregar un vehiculo a favoritos de un usuario 
@app.route('/favorite/vehicle/<int:user_id>/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(user_id, vehicle_id):
    try:
        #verificar si el vehiculo ya está en los favoritos
        existing_favorite = db.session.execute(select(Favorites).filter_by(user_id=user_id, vehicle_id=vehicle_id)).scalar_one_or_none()
        if existing_favorite:
            return jsonify({"error": "This vehicle is already in your favorites."}), 400

        #añadir el vehiculo a los favoritos
        new_favorite = Favorites(user_id=user_id, vehicle_id=vehicle_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({"msg": f"Vehicle {vehicle_id} added to user {user_id}'s favorites."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


#eliminar un personaje de favoritos de un usuario
@app.route('/favorite/character/<int:user_id>/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    try:
        # Verificar si el personjaje está en los favoritos
        favorite = db.session.execute(select(Favorites).filter_by(user_id=user_id, character_id=character_id)).scalar_one_or_none()
        if not favorite:
            return jsonify({"error": "Character not found in your favorites."}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"msg": f"Character {character_id} removed from user {user_id}'s favorites."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#eliminar planeta de favoritos de un usuario
@app.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    try:
        # Verificar si el planeta está en los favoritos
        favorite = db.session.execute(select(Favorites).filter_by(user_id=user_id, planet_id=planet_id)).scalar_one_or_none()
        if not favorite:
            return jsonify({"error": "Planet not found in your favorites."}), 404

        # Eliminar el planeta de los favoritos
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"msg": f"Planet {planet_id} removed from user {user_id}'s favorites."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#eliminar vehiculo de favoritos de un usuario
@app.route('/favorite/vehicle/<int:user_id>/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(user_id, vehicle_id):
    try:
        # Verificar si el vehiculo está en los favoritos
        favorite = db.session.execute(select(Favorites).filter_by(user_id=user_id, vehicle_id=vehicle_id)).scalar_one_or_none()
        if not favorite:
            return jsonify({"error": "Vehicle not found in your favorites."}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"msg": f"Vehicle {vehicle_id} removed from user {user_id}'s favorites."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
