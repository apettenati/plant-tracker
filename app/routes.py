from flask import Flask, request, jsonify, render_template, redirect, flash
import psycopg2
from configparser import ConfigParser
from .queries.plant import get_all_plants, add_plant, get_plant, update_plant, delete_plant 
from .queries.user import get_user
from .queries.water import get_last_watered, get_water_tracker, water_plant
from app import app

''' establish Postgres connection'''
config = ConfigParser()
config.read('config.ini')
user = config.get('postgres', 'user')
password = config.get('postgres', 'password')
database = config.get('postgres', 'database')
port = config.get('postgres', 'port')
host = config.get('postgres', 'host')


connection = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    port=port
)


# app = Flask(__name__)


@app.route('/')
def home():
    plants = get_all_plants(connection)
    return render_template('index.html', plants=plants)

@app.route('/plants', methods=['GET', 'POST', 'PUT', 'DELETE'])
def plants():
    '''get data for existing plant'''
    if request.method == 'GET':
        data = request.form
        plant_id = data.get('plant-id')
        plant = get_plant(connection, plant_id)
        if plant:
            return jsonify(plant)
        else:
            return f'Plant {plant_id} is not a valid plant'
    '''create new plant'''
    if request.method == 'POST':
        data = request.form
        plant_name = data.get('plant-name')
        adoption_date = data.get('adoption-date')
        pot_size = data.get('pot-size')
        purchase_location = data.get('purchase-location')
        purchase_price = data.get('purchase-price')
        plant = add_plant(connection, plant_name, adoption_date, pot_size, purchase_location, purchase_price)
        if plant:
            return jsonify(plant)
        else:
            return f'Plant was not added'
    '''edit existing plant'''
    if request.method == 'PUT':
        data = request.form.to_dict()
        plant = update_plant(connection, data)
        if plant:
            return jsonify(plant)
        else:
            return 'Plant {plant_id} was not updated'
    '''delete existing plant'''
    if request.method == 'DELETE':
        data = request.form
        plant_id = data.get('plant-id')
        # for plant in request.form.getlist('plant_checkbox'):
        plant_exists = get_plant(connection, plant_id)
        if plant_exists:
            delete_plant(connection, plant_id)
            # flash("Successfully Deleted!")
        # return redirect('/')
            return jsonify(plant_id)
        else:
            return f'Plant {plant_id} does not exist'
    

@app.route('/water', methods=['POST', 'GET', 'DELETE'])
def water():
    '''add timestamp for plant watering'''
    if request.method == 'POST':
        data = request.form
        plant_id = data.get('plant-id')
        plant = jsonify(water_plant(connection, plant_id))
        if plant:
            return plant
        else:
            return f'Plant {plant_id} does not exist'
    '''get water timestamps'''
    if request.method == 'GET':
        data = request.form
        plant_id = data.get('plant-id')
        if plant_id is None:
            return jsonify(get_water_tracker(connection))
        else:
            return jsonify(get_last_watered(connection, plant_id))

@app.route('/user')
def user():
    results = get_user(connection)
    print(results)
    return {'username': results[1]}


if __name__ == 'main':
    with connection:
        app.run()