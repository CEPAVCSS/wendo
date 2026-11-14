from models.orders_model import OrdersModel


class OrdersController:
    def __init__(self, model=None):
        self.model = model or OrdersModel()

    def get_orders(self):
        return self.model.get_orders()

    def get_order(self, order_id):
        return self.model.get_order(order_id)

    def add_order(self, order):
        self.model.add_order(order)

    def update_status(self, order_id, order_status):
        self.model.update_status(order_id, order_status)

    def delete_order(self, order_id):
        self.model.delete_order(order_id)
