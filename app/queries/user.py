
def get_user(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * from users")
        user = cursor.fetchall()
        return user[0]