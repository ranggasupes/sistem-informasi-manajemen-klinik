
from config.database import Database


class DokterModel:

    def get_all_dokter(self):
        connection = Database.get_connection()

        if connection is None:
            return []

        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM dokter")
            return cursor.fetchall()

        except Exception as e:
            print(f"Error mengambil data dokter: {e}")
            return []

        finally:
            if cursor:
                cursor.close()
            connection.close()

    def get_by_user_id(self, id_user):
        connection = Database.get_connection()

        if connection is None:
            return None

        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    d.id_dokter,
                    d.id_user,
                    d.id_poli,
                    d.nama_dokter,
                    d.spesialisasi,
                    d.no_telepon,
                    p.nama_poli
                FROM dokter d
                JOIN poli p
                    ON d.id_poli = p.id_poli
                WHERE d.id_user = %s
                LIMIT 1
            """

            cursor.execute(query, (id_user,))
            return cursor.fetchone()

        except Exception as e:
            print(f"Error mengambil profil dokter: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            connection.close()
