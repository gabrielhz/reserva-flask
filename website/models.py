from . import db
from sqlalchemy.sql import func


class Restaurante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_restaurante = db.Column(db.String(150), unique=True)
    endereco = db.Column(db.String(300))


class Mesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ocupado = db.Column(db.Integer, default="0")
    reserva = db.Column(db.Integer, default="0")
    numero_mesa = db.Column(db.Integer)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurante.id'))
    restaurante = db.relationship('Restaurante')
