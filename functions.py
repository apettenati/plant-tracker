def get_user(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * from users")
        user = cursor.fetchall()
        return user[0]

def add_plant(connection, 
              plant_name, 
              adoption_date=None, 
              pot_size=None, 
              purchase_location=None, 
              purchase_price=None
              ):
    with connection.cursor() as cursor:
        cursor.execute("""INSERT INTO plants 
                    (plant_name, adoption_date, pot_size, purchase_location, purchase_price) 
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING plant_id;""", 
                    (plant_name, adoption_date, pot_size, purchase_location, purchase_price))
        plant_id = str(cursor.fetchone()[0])
        connection.commit()
        return plant_id

def get_plant(connection, plant_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM plants WHERE plant_id=%s", 
                    (plant_id,))
        plant = cursor.fetchone()
        headers = [column[0] for column in cursor.description]
        # if plant is not None:
        #     return plant 
        if plant is not None:
            return dict(zip(headers, plant))

def update_plant():
    return 'update plant'

def delete_plant(connection, plant_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM plants WHERE plant_id=%s;", 
                    (plant_id,))
        connection.commit()
        return (f"Plant {plant_id} removed successfully!")