from flask import Flask, request
import psycopg2
from configparser import ConfigParser
from Postgres import get_user, add_plant, get_plant, update_plant, delete_plant

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

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello World'

@app.route('/plants', methods=['GET', 'POST', 'PUT', 'DELETE'])
def plants():
    if request.method == 'GET':
        data = request.form
        plant_id = data.get('plant-id')
        plant = get_plant(connection, plant_id)
        if plant:
            # id, plant_name, adoption_date, death_date, pot_size, purchase_location, purchase_price, user_id = plant
            # return f"""Here are the details for plant {id}:
            #         User ID: {user_id}
            #         Plant name: {plant_name}
            #         Adoption Date: {adoption_date}
            #         Death Date: {death_date}
            #         Pot Size: {pot_size}
            #         Purchase Location: {purchase_location}
            #         Purchase Price: {purchase_price}
            #         """
            return str(plant)
        else:
            return f'Plant {plant_id} is not a valid plant'
    if request.method == 'POST':
        data = request.form
        plant_name = data.get('plant-name')
        adoption_date = data.get('adoption-date')
        pot_size = data.get('pot-size')
        purchase_location = data.get('purchase-location')
        purchase_price = data.get('purchase-price')
        plant_id = add_plant(connection, plant_name, adoption_date, pot_size, purchase_location, purchase_price)
        if plant_id:
            return f"Plant {plant_id} was created successfully!"
        else:
            return f'Plant was not added'
    if request.method == 'PUT':
        #TODO
        plant = update_plant()
        return plant
    if request.method == 'DELETE':
        data = request.form
        plant_id = data.get('plant-id')
        plant_exists = get_plant(connection, plant_id)
        if plant_exists:
            plant = delete_plant(connection, plant_id)
            return plant
        else:
            return f'Plant {plant_id} does not exist'
    

@app.route('/user')
def user():
    results = get_user(connection)
    print(results)
    return {
     'username': results[1]
     }

if __name__ == 'main':
    with connection:
        app.run(debug=True)