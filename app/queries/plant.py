from datetime import datetime
import psycopg2
from psycopg2 import sql


def get_all_plants(connection: psycopg2) -> list:
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM plants;")
        plants = cursor.fetchall()
        headers = [column[0] for column in cursor.description]
        if plants is not None:
            return [dict(zip(headers, row)) for row in plants]
            
def get_plant(connection: psycopg2, plant_id: int) -> dict:
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM plants WHERE plant_id=%s", 
                    (plant_id,))
        plant = cursor.fetchone()
        headers = [column[0] for column in cursor.description]
        if plant is not None:
            return dict(zip(headers, plant))

def create_plant(connection: psycopg2,
              plant_name: str,
              adoption_date: datetime=None,
              pot_size: float=None,
              purchase_location: str=None,
              purchase_price: float=None) -> int:
    # TODO: refactor to use sql module
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO plants 
            (plant_name, adoption_date, pot_size, purchase_location, purchase_price) 
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *;
            """, 
            (plant_name, adoption_date, pot_size, purchase_location, purchase_price)
        )
        connection.commit()
        plant = cursor.fetchone()
        headers = [column[0] for column in cursor.description]
        return dict(zip(headers, plant))

def update_plant(connection: psycopg2, data: dict) -> int:
    data = {key.replace("-", "_"): value for key, value in data.items()}
    query = """
        UPDATE plants
        SET {data}
        WHERE plant_id={id}
        RETURNING *;
    """
    sql_query = sql.SQL(query).format(
        data = sql.SQL(', ')
                  .join(sql.Composed([sql.Identifier(key), sql.SQL(' = '), sql.Placeholder(key)]) for key in data.keys()
        ),
        id=sql.Placeholder('plant_id')
    )
    
    with connection.cursor() as cursor:
        # print(cursor.mogrify(sql_query, data))
        cursor.execute(sql_query, data)
        connection.commit()
        plant = cursor.fetchone()
        headers = [column[0] for column in cursor.description]
        return dict(zip(headers, plant))

def delete_plant(connection: psycopg2, plant_id: int):
    with connection.cursor() as cursor:
        cursor.execute("""
                       DELETE FROM plants
                       WHERE plant_id=%s
                       RETURNING *;
                       """,
                    (plant_id,))
        connection.commit()
        return plant_id