
from config.database import Database


class UserModel:

    def get_user_by_username(self, username):
        connection = Database.get_connection()

        if connection is None:
            return None

        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT id_user, username, password, role
                FROM users
                WHERE username = %s
                LIMIT 1
            """

            cursor.execute(query, (username,))
            user = cursor.fetchone()

            return user

        except Exception as e:
            print(f"Error mengambil data user: {e}")
            return None

        finally:
            if cursor:
                cursor.close()

            connection.close()
    def get_all_users(self):
        connection = Database.get_connection()
        if connection is None:
            return []
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error mengambil data user: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
