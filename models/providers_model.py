

class ProvidersModel:
    def __init__(self):
        self.providers = []  # Lista para almacenar los proveedores

    def add_provider(self, provider):
        self.providers.append(provider)  # Agrega un proveedor a la lista

    def get_providers(self):


        headers = ["Nombre", "Teléfono", "Email"]

        proveedores = [
                    ["Proveedor 1", "123456789", "proveedor1@example.com"],
                    ["Proveedor 2", "987654321", "proveedor2@example.com"],
                    ["Proveedor 3", "555555555", "proveedor3@example.com"],
                    ["Proveedor 4", "111111111", "proveedor4@example.com"],
                    ["Proveedor 5", "222222222", "proveedor5@example.com"]
                ]
        
        return headers, proveedores  # Devuelve la lista de proveedores