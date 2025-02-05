from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password =  db.Column(db.String(10), nullable=False)
    def serialize(self):
        return {"id": self.id, "name": self.name, "last_name":self.last_name, "email":self.email, "password": self.password}

class Planeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20),unique=True, nullable=False)
    clima = db.Column(db.String(50), nullable=False)
    residentes = db.Column(db.String(50), nullable=False)
    def serialize(self):
        return {"id": self.id, "nombre": self.nombre, "clima":self.clima, "residentes": self.residentes}
            

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), nullable=False)
    especie= db.Column(db.String(50), nullable=False)
    genero= db.Column(db.String(50), nullable=False)
    def serialize(self):
        return {"id": self.id, "name": self.name, "especie": self.especie, "genero": self.genero}
    
class Favoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id= db.Column(db.Integer, db.ForeignKey('planeta.id'), nullable=False)
    people_id= db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    def serialize(self):
        return {"id": self.id, "user_id": self.user_id, "planet_id": self.planet_id, "people": self.people_id}
    