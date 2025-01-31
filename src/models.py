from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, Boolean, Numeric


db = SQLAlchemy()
app = Flask(__name__)
app.url_map.strict_slashes = False
jwt = JWTManager(app)




class User(db.Model):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(120), nullable=False)
    password = mapped_column(String(80))
    is_active = mapped_column(Boolean)

    #relacion con Favorites usando cascade para eliminar automáticamente los favoritos cuando se elimine un usuario
    favorites = db.relationship('Favorites', backref='user', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    __tablename__ = "characters"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(120), nullable=False)
    birth_year = mapped_column(String(80))
    height = mapped_column(Numeric(4,2))
    skin_color = mapped_column(String(20))
    eye_color = mapped_column(String(20))

    def __repr__(self):
        return '<Characters %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "height": self.height,
            "skin_color": self.skin_color,
            "eye_color": self.skin_color
        }

class Planets(db.Model):
    __tablename__ = "planets"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(120), nullable=False)
    climate = mapped_column(String(80))
    diameter = mapped_column(Integer)
    population = mapped_column(Integer)
    terrain = mapped_column(String(20))

    def __repr__(self):
        return '<Planets %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "population": self.population,
            "terrain": self.terrain
        }

class Vehicles(db.Model):
    __tablename__ = "vehicles"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(120), nullable=False)
    model = mapped_column(String(80))
    cargo_capacity = mapped_column(Integer)
    length = mapped_column(Numeric(None,2))
    passengers = mapped_column(Integer)

    def __repr__(self):
        return '<Vehicles %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "cargo_capacity": self.cargo_capacity,
            "length": self.length,
            "passengers": self.passengers
        }


class Favorites(db.Model):
    __tablename__ = "favorites"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = mapped_column(Integer, db.ForeignKey('planets.id'), nullable=True)
    character_id = mapped_column(Integer, db.ForeignKey('characters.id'), nullable=True)
    vehicle_id = mapped_column(Integer, db.ForeignKey('vehicles.id'), nullable=True)

    # Relaciones con los otros modelos
    planet = db.relationship('Planets', backref='favorites', lazy=True)
    character = db.relationship('Characters', backref='favorites', lazy=True)
    vehicle = db.relationship('Vehicles', backref='favorites', lazy=True)

    def __repr__(self):
        return '<Favorites %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
            "vehicle_id": self.vehicle_id
        }

