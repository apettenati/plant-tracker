from datetime import datetime
import psycopg2
from psycopg2 import sql


def get_plant(connection: psycopg2, plant_id: int) -> dict:
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM plants WHERE plant_id=%s", 
                    (plant_id,))
        plant = cursor.fetchone()
        headers = [column[0] for column in cursor.description]
        if plant is not None:
            return dict(zip(headers, plant))


def add_plant(connection: psycopg2, 
              plant_name: str, 
              adoption_date: datetime=None, 
              pot_size: float=None, 
              purchase_location: str=None, 
              purchase_price: float=None
              ) -> int:
    # TODO: refactor to use sql module
    with connection.cursor() as cursor:
        cursor.execute("""INSERT INTO plants 
                    (plant_name, adoption_date, pot_size, purchase_location, purchase_price) 
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING plant_id;""", 
                    (plant_name, adoption_date, pot_size, purchase_location, purchase_price))
        plant_id = str(cursor.fetchone()[0])
        connection.commit()
        return plant_id


def update_plant(connection: psycopg2, data: dict) -> int:
    data = {key.replace("-", "_"): value for key, value in data.items()}
    sql_query = sql.SQL("UPDATE plants SET {data} WHERE plant_id={id} RETURNING plant_id;").format(
        data =sql.SQL(', ').join(
            sql.Composed([sql.Identifier(key), sql.SQL(' = '), sql.Placeholder(key)]) for key in data.keys()
            ),
            id=sql.Placeholder('plant_id')
            )
    
    with connection.cursor() as cursor:
        print(cursor.mogrify(sql_query, data))
        cursor.execute(sql_query, data)
        connection.commit()
        plant_id = str(cursor.fetchone()[0])
        return plant_id


def delete_plant(connection: psycopg2, plant_id: int):
    #FIXME: can't delete when referenced on water table
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM * WHERE plant_id=%s;", 
                    (plant_id,))
        connection.commit()
        return plant_id