from flask import request, jsonify, render_template, redirect, flash, url_for
import psycopg2
from configparser import ConfigParser
from app.queries.plant import get_all_plants, create_plant, get_plant, update_plant, delete_plant 
from app.queries.user import get_user
from app.queries.water import get_last_watered, get_water_tracker, water_plant
from app import app
from app.forms import AddPlantForm

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


@app.route('/')
def index():
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

@app.route('/add-plant', methods=['GET', 'POST'])
def add_plant():
    form = AddPlantForm()
    if form.validate_on_submit():
        plant = create_plant(connection, form.plant_name.data, form.adoption_date.data, form.pot_size.data, form.purchase_location.data, form.purchase_price.data)
        if plant:
            flash('New plant submitted')
            return redirect(url_for('index'))
    return render_template('add_plant.html', title='Add Plant', form=form)


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