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


@views.route('/delete-restaurante', methods=['POST'])
def delete_restaurante():
    restaurante = json.loads(request.data)
    restauranteId = restaurante['patrimonioId']
    restaurante = Restaurante.query.get(restauranteId)
    if restaurante:
        # if patrimonio.user_id == current_user.id:
        db.session.delete(restaurante)
        db.session.commit()
    return jsonify({})


@views.route('/restaurante/<int:restaurante_id>', methods=['GET', 'POST'])
def restaurante(restaurante_id):
    restaurante = Restaurante.query.get(restaurante_id)
    mesas = Mesa.query.filter_by(
        restaurante_id=restaurante_id).all()

    if request.method == 'POST':
        numeroMesa = request.form.get('numeroMesa')

        mesa = Mesa.query.filter_by(
            numero_mesa=numeroMesa, restaurante_id=restaurante_id).first()

        if not mesa:
            if not numeroMesa or len(numeroMesa) < 1:
                flash('Número da mesa inválido!', category='error')
            else:
                new_mesa = Mesa(
                    numero_mesa=numeroMesa, restaurante_id=restaurante_id)
                db.session.add(new_mesa)
                db.session.commit()
                flash('Mesa Adicionada!', category='sucess')
                return redirect(url_for('views.restaurante', restaurante_id=restaurante_id))
        else:
            flash('Mesa já existente!', category='error')

    return render_template("restaurante.html", restaurante=restaurante, mesas=mesas)


@views.route('/deletar-mesa/<int:mesa_id>', methods=['GET', 'POST'])
def deletar_mesa(mesa_id):
    remover = request.form.get('remover')
    mesa = Mesa.query.get(mesa_id)

    if remover:
        db.session.delete(mesa)
        db.session.commit()

    return redirect(url_for('views.restaurante', restaurante_id=mesa.restaurante_id))


@views.route('/atualizar-mesa/<int:mesa_id>', methods=['GET', 'POST'])
def atualizar_mesa(mesa_id):
    valor = request.form.get('valor')
    mesa = Mesa.query.get(mesa_id)

    if valor == '1':
        mesa.ocupado = False
        mesa.reserva = False
    elif valor == '2':
        mesa.ocupado = True
        mesa.reserva = False
    elif valor == '3':
        mesa.ocupado = False
        mesa.reserva = True
    else:
        flash('Operação inválida!', category='error')

    db.session.commit()

    return redirect(url_for('views.restaurante', restaurante_id=mesa.restaurante_id))
