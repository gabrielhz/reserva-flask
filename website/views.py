from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from datetime import datetime
from .models import Restaurante, Mesa
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    restaurantes = Restaurante.query.all()

    return render_template("home.html", restaurantes=restaurantes)


@views.route('/add-restaurante', methods=['GET', 'POST'])
def add_restaurante():
    if request.method == 'POST':
        nomeRestaurante = request.form.get('nomeRestaurante')
        enderecoRestaurante = request.form.get('enderecoRestaurante')

        restaurante = Restaurante.query.filter_by(
            nome_restaurante=nomeRestaurante).first()
        if restaurante:
            flash('Restaurante já registrado!', category='error')
        else:
            new_restaurante = Restaurante(
                nome_restaurante=nomeRestaurante, endereco=enderecoRestaurante)
            db.session.add(new_restaurante)
            db.session.commit()
            flash('Restaurante Adicionado!', category='sucess')
            return redirect(url_for('views.home'))

    return render_template('add_restaurante.html')


@views.route('/restaurante/<int:restaurante_id>')
def restaurante(restaurante_id):
    restaurante = Restaurante.query.get(restaurante_id)

    return render_template("restaurante.html", restaurante=restaurante)
