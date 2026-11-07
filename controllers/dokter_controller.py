from models.dokter_model import DokterModel

class DokterController:
    def __init__(self):
        self.model = DokterModel()

    def daftar_dokter(self):
        return self.model.get_all_dokter()