from models.currency_model import CurrencyModel


class CurrencyController:
    def __init__(self, model=None):
        self.model = model or CurrencyModel()

    def get_rates(self):
        return self.model.get_rates()
