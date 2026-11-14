from models.providers_model import ProvidersModel


class ProvidersController:
    def __init__(self, master=None, model=None):
        self.master = master
        self.model = model or ProvidersModel()

    def get_providers(self):
        return self.model.get_providers()

    def get_provider(self, provider_id):
        return self.model.get_provider(provider_id)

    def add_provider(self, provider):
        self.model.add_provider(provider)

    def update_provider(self, provider_id, provider):
        self.model.update_provider(provider_id, provider)

    def delete_provider(self, provider_id):
        self.model.delete_provider(provider_id)
