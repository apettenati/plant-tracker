from datetime import datetime
import psycopg2
from psycopg2 import sql


def water_plant(connection: psycopg2, plant_id: int) -> int:
    sql_query = ("""
                 INSERT INTO water_tracker
                 (plant_id, timestamp)
                 VALUES (%s, %s)
                 RETURNING *;
                 """)
    
    with connection.cursor() as cursor:
        cursor.execute(sql_query, (plant_id, datetime.now()))
        connection.commit()
        result = str(cursor.fetchone()[0])
        return result


def get_water_tracker(connection: psycopg2) -> dict:
    sql_query = sql.SQL("""
                 SELECT json_agg({table_name})
                 FROM {table_name}
                 LIMIT {limit};
                 """).format(
                     table_name=sql.Identifier('water_tracker'),
                     limit=sql.Literal(100),
                 )

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        table = cursor.fetchall()
        return {'water_tracker': table}

def get_last_watered(connection: psycopg2, plant_id: int) -> dict:
    sql_query = sql.SQL("""
                 SELECT * 
                 FROM water_tracker
                 WHERE plant_id=%s
                 ORDER BY TIMESTAMP DESC;
                 """)

    with connection.cursor() as cursor:
        cursor.execute(sql_query, (plant_id,))
        plant = cursor.fetchall()
        return {'plant': plant}