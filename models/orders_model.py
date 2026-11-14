import sqlite3

from models.conector.SQLiteConector import SQLiteConnector


class DuplicateOrderError(ValueError):
    pass


class OrdersModel:
    fields = (
        "order_number",
        "order_date",
        "order_type",
        "customer_name",
        "order_status",
        "order_amount",
    )

    def __init__(self, db=None):
        self.db = db or SQLiteConnector()

    def get_orders(self):
        columns = ", ".join(("id_order",) + self.fields)
        return self.db.fetch_all(
            f"SELECT {columns} FROM orders "
            "ORDER BY order_date DESC, id_order DESC"
        )

    def get_order(self, order_id):
        columns = ", ".join(("id_order",) + self.fields)
        rows = self.db.fetch_all(
            f"SELECT {columns} FROM orders WHERE id_order = ?",
            (order_id,),
        )
        return rows[0] if rows else None

    def add_order(self, order):
        values = [str(order.get(field) or "").strip() for field in self.fields]
        order_number = values[0]
        order_date = values[1]
        order_type = values[2]
        customer_name = values[3]
        order_status = values[4] or "Pendiente"
        order_amount = values[5]

        if not order_number:
            raise ValueError("El número de orden es obligatorio.")
        if order_type not in ("Compra", "Venta"):
            raise ValueError("Selecciona un tipo de pedido válido.")
        if not customer_name:
            raise ValueError("El asociado al pedido es obligatorio.")
        if order_status not in ("Pendiente", "Pagado", "Entregado", "Cancelado"):
            raise ValueError("Selecciona un estado válido.")

        try:
            amount = float(order_amount)
        except (TypeError, ValueError) as error:
            raise ValueError("El monto debe ser un número válido.") from error
        if amount <= 0:
            raise ValueError("El monto debe ser mayor que cero.")

        if self.db.fetch_all(
            "SELECT 1 FROM orders WHERE LOWER(TRIM(order_number)) = LOWER(TRIM(?)) LIMIT 1",
            (order_number,),
        ):
            raise DuplicateOrderError("Ya existe un pedido con ese número de orden.")

        try:
            self.db.execute(
                "INSERT INTO orders (order_number, order_date, order_type, "
                "customer_name, order_status, order_amount) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    order_number,
                    order_date,
                    order_type,
                    customer_name,
                    order_status,
                    amount,
                ),
            )
        except sqlite3.IntegrityError as error:
            raise DuplicateOrderError(
                "El número de orden ya está registrado."
            ) from error

    def update_status(self, order_id, order_status):
        if order_status not in ("Pendiente", "Pagado", "Entregado", "Cancelado"):
            raise ValueError("Selecciona un estado válido.")
        self.db.execute(
            "UPDATE orders SET order_status = ? WHERE id_order = ?",
            (order_status, order_id),
        )

    def delete_order(self, order_id):
        self.db.execute("DELETE FROM orders WHERE id_order = ?", (order_id,))
