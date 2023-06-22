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


@views.route('/restaurante/<int:restaurante_id>')
def restaurante(restaurante_id):
    patrimonio = Restaurante.query.get(restaurante_id)

    return render_template("item_info.html", restaurante=restaurante)
