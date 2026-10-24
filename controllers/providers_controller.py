import ttkbootstrap as ttk
from models.providers_model import ProvidersModel

class ProvidersController:
    def __init__(self, master):
        self.master = master
        self.view = None
        self.model = ProvidersModel()
        self.providers = self.model.get_providers()  # Obtener la lista de proveedores desde el modelo

    
