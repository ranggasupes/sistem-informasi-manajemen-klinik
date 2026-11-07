
import hashlib
import hmac

from models.user_model import UserModel


class AuthController:

    def __init__(self):
        self.user_model = UserModel()

    def login(self, username, password):

        if not username or not password:
            return False, "Username dan password harus diisi."

        user = self.user_model.get_user_by_username(username)

        if user is None:
            return False, "Username tidak ditemukan atau database bermasalah."

        password_hash = hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

        if not hmac.compare_digest(password_hash, user["password"]):
            return False, "Password yang dimasukkan salah."

        # Mengembalikan seluruh identitas pengguna
        user_login = {
            "id_user": user["id_user"],
            "username": user["username"],
            "role": user["role"]
        }

        return True, user_login
