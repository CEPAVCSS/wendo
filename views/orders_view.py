import ttkbootstrap as ttk
from ttkbootstrap.constants import (
    BOTH,
    CENTER,
    E,
    END,
    LEFT,
    RIGHT,
    VERTICAL,
    W,
    X,
    Y,
    YES,
)
from ttkbootstrap.dialogs import Messagebox

from controllers.orders_controller import OrdersController
from models.orders_model import DuplicateOrderError
from utils.utils import Utils


class OrdersView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.pack(fill=BOTH, expand=YES)
        self.controller = OrdersController()
        self.orders = []
        self.current_type = "Todos"
        self.search_text = ""
        self.filter_buttons = {}

        self.container = ttk.Frame(self, padding=8)
        self.container.pack(side=LEFT, fill=Y)
        self.App_title = "Pedidos"
        ttk.Label(
            self.container,
            text=self.App_title,
            font=("Helvetica", 16, "bold"),
        ).pack(pady=10)
        self.count_label = ttk.Label(
            self.container,
            text="",
            font=("Helvetica", 9),
            bootstyle="secondary",
        )
        self.count_label.pack(pady=(0, 8))

        ttk.Button(
            self.container,
            text="Agregar Pedido",
            bootstyle="primary",
            command=self.agregar_pedido,
        ).pack(pady=4, fill=X)
        ttk.Button(
            self.container,
            text="Ver Pedidos",
            bootstyle="outline-secondary",
            command=self.refresh,
        ).pack(pady=4, fill=X)
        ttk.Button(
            self.container,
            text="Marcar Pagado / Pendiente",
            bootstyle="outline-success",
            command=self._toggle_paid,
        ).pack(pady=4, fill=X)
        ttk.Button(
            self.container,
            text="Eliminar Pedido",
            bootstyle="outline-danger",
            command=self._delete_order,
        ).pack(pady=4, fill=X)

        self.main_area = ttk.Frame(self, padding=12)
        self.main_area.pack(side=RIGHT, fill=BOTH, expand=YES)

        self.setup_filters()
        self.setup_treeview()
        self.refresh()

    def setup_filters(self):
        filter_frame = ttk.Frame(self.main_area, padding=(0, 0, 0, 10))
        filter_frame.pack(fill=X)

        ttk.Label(
            filter_frame,
            text="FILTROS:",
            font=("Helvetica", 9, "bold"),
            bootstyle="secondary",
        ).pack(side=LEFT, padx=(0, 10))

        for key, label in (("Todos", "Todos"), ("Venta", "Ventas"), ("Compra", "Compras")):
            button = ttk.Button(
                filter_frame,
                text=label,
                bootstyle="primary" if key == "Todos" else "secondary-outline",
                command=lambda current=key: self._set_type(current),
            )
            button.pack(side=LEFT, padx=2)
            self.filter_buttons[key] = button

        ttk.Label(filter_frame, text="Buscar:", bootstyle="secondary").pack(
            side=RIGHT, padx=(10, 4)
        )
        self.search_var = ttk.StringVar()
        self.search_var.trace_add("write", lambda *_args: self._on_search())
        ttk.Entry(
            filter_frame,
            textvariable=self.search_var,
            bootstyle="light",
            width=24,
        ).pack(side=RIGHT)

    def setup_treeview(self):
        tree_frame = ttk.Frame(self.main_area)
        tree_frame.pack(fill=BOTH, expand=YES)

        columns = ("check", "orden", "fecha", "tipo", "asociado", "monto", "estado")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            bootstyle="light",
        )

        headings = {
            "check": "☐",
            "orden": "N° ORDEN / REF",
            "fecha": "FECHA EMISIÓN",
            "tipo": "TIPO",
            "asociado": "ASOCIADO A",
            "monto": "MONTO",
            "estado": "ESTADO",
        }
        for column, text in headings.items():
            self.tree.heading(column, text=text)

        widths = {
            "check": (40, CENTER),
            "orden": (140, W),
            "fecha": (120, W),
            "tipo": (90, CENTER),
            "asociado": (240, W),
            "monto": (120, E),
            "estado": (110, CENTER),
        }
        for column, (width, anchor) in widths.items():
            self.tree.column(column, width=width, anchor=anchor)

        self.tree.tag_configure("pagado", background="#D1E7DD", foreground="#0F5132")
        self.tree.tag_configure("pendiente", background="#FFF3CD", foreground="#664D03")
        self.tree.tag_configure("entregado", background="#CFE2FF", foreground="#084298")
        self.tree.tag_configure("cancelado", background="#F8D7DA", foreground="#842029")

        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tree.bind("<Button-1>", self.on_click_cell)
        self.tree.bind("<Double-1>", lambda _event: self._toggle_paid())

    def _set_type(self, order_type):
        self.current_type = order_type
        for key, button in self.filter_buttons.items():
            button.configure(
                bootstyle="primary" if key == order_type else "secondary-outline"
            )
        self._populate_tree()

    def _on_search(self):
        self.search_text = self.search_var.get().strip().lower()
        self._populate_tree()

    def refresh(self):
        self.orders = self.controller.get_orders()
        self._update_filter_buttons()
        self._populate_tree()

    def _update_filter_buttons(self):
        counts = {
            "Todos": len(self.orders),
            "Venta": sum(1 for order in self.orders if order["order_type"] == "Venta"),
            "Compra": sum(1 for order in self.orders if order["order_type"] == "Compra"),
        }
        labels = {"Todos": "Todos", "Venta": "Ventas", "Compra": "Compras"}
        for key, button in self.filter_buttons.items():
            button.configure(text=f"{labels[key]} ({counts[key]})")
        self.count_label.configure(text=f"{len(self.orders)} pedido(s) registrado(s)")

    def _populate_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for order in self.orders:
            if self.current_type != "Todos" and order["order_type"] != self.current_type:
                continue
            searchable = " ".join(
                str(order[field] or "")
                for field in ("order_number", "customer_name", "order_status")
            ).lower()
            if self.search_text and self.search_text not in searchable:
                continue

            status = order["order_status"] or "Pendiente"
            try:
                amount = f"${float(order['order_amount'] or 0):,.2f}"
            except (TypeError, ValueError):
                amount = "$0.00"

            values = (
                "☐",
                order["order_number"] or "",
                order["order_date"] or "",
                order["order_type"] or "",
                order["customer_name"] or "",
                amount,
                status,
            )
            self.tree.insert(
                "",
                END,
                iid=str(order["id_order"]),
                values=values,
                tags=(status.lower(),),
            )

    def _selected_order_id(self):
        selection = self.tree.selection()
        if not selection:
            Messagebox.show_warning(
                "Selecciona un pedido de la tabla.",
                title="Sin selección",
                parent=self,
            )
            return None
        return int(selection[0])

    def _selected_order(self):
        order_id = self._selected_order_id()
        if order_id is None:
            return None
        return self.controller.get_order(order_id)

    def _toggle_paid(self):
        order = self._selected_order()
        if order is None:
            return
        new_status = "Pendiente" if order["order_status"] == "Pagado" else "Pagado"
        try:
            self.controller.update_status(order["id_order"], new_status)
        except Exception as error:
            Messagebox.show_error(str(error), title="No se pudo actualizar", parent=self)
            return
        self.refresh()

    def _delete_order(self):
        order = self._selected_order()
        if order is None:
            return
        confirmed = Messagebox.okcancel(
            f"¿Eliminar el pedido «{order['order_number']}»?",
            title="Eliminar pedido",
            alert=True,
            parent=self,
        )
        if confirmed != "OK":
            return
        try:
            self.controller.delete_order(order["id_order"])
        except Exception as error:
            Messagebox.show_error(str(error), title="No se pudo eliminar", parent=self)
            return
        self.refresh()

    def on_click_cell(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item_id = self.tree.identify_row(event.y)
            if column == "#1" and item_id:
                values = list(self.tree.item(item_id, "values"))
                values[0] = "☑" if values[0] == "☐" else "☐"
                self.tree.item(item_id, values=values)

    def agregar_pedido(self, master=None):
        dialog = ttk.Toplevel(title="Agregar Pedido")
        dialog.geometry("460x560")
        dialog.minsize(420, 520)
        Utils.center_window(dialog)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ttk.Label(
            dialog,
            text="Agregar Pedido",
            font=("Helvetica", 16, "bold"),
        ).pack(pady=(14, 8))

        form = ttk.Labelframe(dialog, text="Datos del pedido", padding=14)
        form.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self.order_number = ttk.StringVar()
        self.order_type = ttk.StringVar(value="Venta")
        self.customer_name = ttk.StringVar()
        self.order_amount = ttk.StringVar()
        self.order_status = ttk.StringVar(value="Pendiente")

        ttk.Label(form, text="N° Orden / Referencia").pack(anchor="w")
        ttk.Entry(form, textvariable=self.order_number).pack(
            fill="x", pady=(2, 8)
        )

        ttk.Label(form, text="Fecha de emisión").pack(anchor="w")
        order_date = ttk.DateEntry(form, date_format="%Y-%m-%d")
        order_date.pack(fill="x", pady=(2, 8))

        ttk.Label(form, text="Tipo").pack(anchor="w")
        ttk.Combobox(
            form,
            textvariable=self.order_type,
            values=("Venta", "Compra"),
            state="readonly",
        ).pack(fill="x", pady=(2, 8))

        ttk.Label(form, text="Asociado a").pack(anchor="w")
        ttk.Entry(form, textvariable=self.customer_name).pack(
            fill="x", pady=(2, 8)
        )

        ttk.Label(form, text="Monto").pack(anchor="w")
        ttk.Entry(form, textvariable=self.order_amount).pack(
            fill="x", pady=(2, 8)
        )

        ttk.Label(form, text="Estado").pack(anchor="w")
        ttk.Combobox(
            form,
            textvariable=self.order_status,
            values=("Pendiente", "Pagado", "Entregado", "Cancelado"),
            state="readonly",
        ).pack(fill="x", pady=(2, 8))

        actions = ttk.Frame(form)
        actions.pack(fill=X, pady=(10, 0))
        ttk.Button(
            actions,
            text="Guardar Pedido",
            bootstyle="success",
            command=lambda: self._save_order(dialog, order_date),
        ).pack(side=RIGHT)
        ttk.Button(
            actions,
            text="Cancelar",
            bootstyle="danger-outline",
            command=dialog.destroy,
        ).pack(side=RIGHT, padx=(0, 8))

    def _save_order(self, dialog, order_date):
        selected_date = order_date.get_date()
        order = {
            "order_number": self.order_number.get().strip(),
            "order_date": selected_date.strftime("%Y-%m-%d") if selected_date else "",
            "order_type": self.order_type.get(),
            "customer_name": self.customer_name.get().strip(),
            "order_status": self.order_status.get(),
            "order_amount": self.order_amount.get().strip(),
        }
        try:
            self.controller.add_order(order)
        except (ValueError, DuplicateOrderError) as error:
            Messagebox.show_warning(str(error), title="Revisa los datos", parent=dialog)
            return
        except Exception as error:
            Messagebox.show_error(
                f"No fue posible guardar el pedido.\n\n{error}",
                title="No se pudo guardar",
                parent=dialog,
            )
            return

        dialog.destroy()
        self.refresh()
