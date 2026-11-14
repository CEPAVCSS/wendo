import queue
import threading
import ttkbootstrap as ttk
from datetime import date
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
from controllers.currency_controller import CurrencyController
from controllers.orders_controller import OrdersController
from controllers.providers_controller import ProvidersController
from models.orders_model import DuplicateOrderError
from utils.utils import Utils


class OrdersView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.pack(fill=BOTH, expand=YES)
        self.controller = OrdersController()
        self.providers_controller = ProvidersController()
        self.currency_controller = CurrencyController()
        self.rate_labels = {}
        self.rate_queue = queue.Queue()
        self.rate_names = {
            "USD": "USD",
            "EURO": "EURO",
            "PARALELO": "Paralelo",
            "PARALELO_EUR": "Paralelo EUR",
        }
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
            text="Ver / Editar Pedido",
            bootstyle="outline-secondary",
            command=self.ver_pedido,
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

        self.setup_currency_badge()
        self.setup_filters()
        self.setup_treeview()
        self.refresh()

    def setup_currency_badge(self):
        badge = ttk.Frame(self.main_area, padding=(10, 6), relief="solid", borderwidth=1)
        badge.pack(fill=X, pady=(0, 10))
        self.currency_badge = badge

        ttk.Label(
            badge,
            text="DIVISAS",
            font=("Helvetica", 8, "bold"),
            bootstyle="secondary",
        ).pack(side=LEFT, padx=(0, 12))

        for key, name in self.rate_names.items():
            label = ttk.Label(
                badge,
                text=f"{name}: ...",
                font=("Helvetica", 10, "bold"),
            )
            label.pack(side=LEFT, padx=(0, 16))
            self.rate_labels[key] = label

        self.rate_status = ttk.Label(
            badge,
            text="Actualizando...",
            font=("Helvetica", 8),
            bootstyle="secondary",
        )
        self.rate_status.pack(side=RIGHT)

        self._load_currency_rates()

    def _load_currency_rates(self):
        if hasattr(self, "rate_status"):
            try:
                self.rate_status.configure(text="Actualizando...")
            except Exception:
                return
        threading.Thread(target=self._fetch_currency_rates, daemon=True).start()
        self.after(100, self._poll_currency_rates)

    def _fetch_currency_rates(self):
        try:
            rates = self.currency_controller.get_rates()
        except Exception:
            rates = {}
        self.rate_queue.put(rates)

    def _poll_currency_rates(self):
        try:
            rates = self.rate_queue.get_nowait()
        except queue.Empty:
            try:
                self.after(100, self._poll_currency_rates)
            except Exception:
                pass
            return
        self._update_currency_rates(rates)

    def _update_currency_rates(self, rates):
        try:
            if not self.winfo_exists():
                return
        except Exception:
            return

        for key, name in self.rate_names.items():
            value = rates.get(key)
            text = f"{name}: {self._format_rate(value)}" if value is not None else f"{name}: N/D"
            try:
                self.rate_labels[key].configure(text=text)
            except Exception:
                return

        try:
            self.rate_status.configure(text="Actualizado" if rates else "Sin conexión")
        except Exception:
            pass

    @staticmethod
    def _format_rate(value):
        try:
            text = f"{float(value):,.2f}"
        except (TypeError, ValueError):
            return "N/D"
        return text.replace(",", "X").replace(".", ",").replace("X", ".")

    @staticmethod
    def _format_amount(value):
        try:
            text = f"{float(value or 0):,.2f}"
        except (TypeError, ValueError):
            text = "0.00"
        return text.replace(",", "X").replace(".", ",").replace("X", ".")

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

        columns = ("check", "orden", "fecha", "tipo", "asociado", "monto", "divisa", "estado")
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
            "divisa": "DIVISA",
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
            "divisa": (80, CENTER),
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
                for field in ("order_number", "customer_name", "order_status", "order_currency")
            ).lower()
            if self.search_text and self.search_text not in searchable:
                continue

            status = order["order_status"] or "Pendiente"
            amount = self._format_amount(order["order_amount"])
            currency = order["order_currency"] or "USD"

            values = (
                "☐",
                order["order_number"] or "",
                order["order_date"] or "",
                order["order_type"] or "",
                order["customer_name"] or "",
                amount,
                currency,
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
        self._open_order_form()

    def ver_pedido(self):
        order_id = self._selected_order_id()
        if order_id is not None:
            self._open_order_form(order_id)

    def _open_order_form(self, order_id=None):
        order = self.controller.get_order(order_id) if order_id is not None else None
        if order_id is not None and order is None:
            self.refresh()
            return

        editing = order is not None
        title = "Ver / Editar Pedido" if editing else "Agregar Pedido"
        dialog = ttk.Toplevel(title=title)
        dialog.geometry("460x600")
        dialog.minsize(420, 560)
        Utils.center_window(dialog)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ttk.Label(
            dialog,
            text=title,
            font=("Helvetica", 16, "bold"),
        ).pack(pady=(14, 8))

        form = ttk.Labelframe(dialog, text="Datos del pedido", padding=14)
        form.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self.order_number = ttk.StringVar(
            value=order["order_number"] if editing else ""
        )
        self.order_type = ttk.StringVar(
            value=order["order_type"] if editing else "Venta"
        )
        self.customer_name = ttk.StringVar(
            value=order["customer_name"] if editing else ""
        )
        self.order_amount = ttk.StringVar(
            value=str(order["order_amount"]) if editing else ""
        )
        self.order_currency = ttk.StringVar(
            value=(order["order_currency"] or "USD") if editing else "USD"
        )
        self.order_status = ttk.StringVar(
            value=order["order_status"] if editing else "Pendiente"
        )

        ttk.Label(form, text="N° Orden / Referencia").pack(anchor="w")
        ttk.Entry(form, textvariable=self.order_number).pack(
            fill="x", pady=(2, 8)
        )

        start_date = date.today()
        if editing and order["order_date"]:
            try:
                start_date = date.fromisoformat(order["order_date"])
            except ValueError:
                pass

        ttk.Label(form, text="Fecha de emisión").pack(anchor="w")
        order_date = ttk.DateEntry(
            form,
            date_format="%Y-%m-%d",
            start_date=start_date,
        )
        order_date.pack(fill="x", pady=(2, 8))

        ttk.Label(form, text="Tipo").pack(anchor="w")
        ttk.Combobox(
            form,
            textvariable=self.order_type,
            values=("Venta", "Compra"),
            state="readonly",
        ).pack(fill="x", pady=(2, 8))

        ttk.Label(form, text="Asociado a").pack(anchor="w")
        provider_row = ttk.Frame(form)
        provider_row.pack(fill=X, pady=(2, 8))
        self.provider_combo = ttk.Combobox(
            provider_row,
            textvariable=self.customer_name,
            values=self._provider_names(),
            state="normal",
            postcommand=self._filter_provider_values,
        )
        self.provider_combo.pack(side=LEFT, fill=X, expand=True)
        ttk.Button(
            provider_row,
            text="Buscar",
            bootstyle="outline-secondary",
            command=self._open_provider_search,
        ).pack(side=LEFT, padx=(6, 0))

        ttk.Label(form, text="Monto").pack(anchor="w")
        ttk.Entry(form, textvariable=self.order_amount).pack(
            fill="x", pady=(2, 8)
        )

        ttk.Label(form, text="Divisa").pack(anchor="w")
        ttk.Combobox(
            form,
            textvariable=self.order_currency,
            values=("USD", "EURO", "Bs"),
            state="readonly",
        ).pack(fill="x", pady=(2, 8))

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
            text="Guardar cambios" if editing else "Guardar Pedido",
            bootstyle="success",
            command=lambda: self._save_order(dialog, order_date, order_id),
        ).pack(side=RIGHT)
        ttk.Button(
            actions,
            text="Cancelar",
            bootstyle="danger-outline",
            command=dialog.destroy,
        ).pack(side=RIGHT, padx=(0, 8))

    def _save_order(self, dialog, order_date, order_id=None):
        selected_date = order_date.get_date()
        order = {
            "order_number": self.order_number.get().strip(),
            "order_date": selected_date.strftime("%Y-%m-%d") if selected_date else "",
            "order_type": self.order_type.get(),
            "customer_name": self.customer_name.get().strip(),
            "order_status": self.order_status.get(),
            "order_amount": self.order_amount.get().strip(),
            "order_currency": self.order_currency.get(),
        }
        try:
            if order_id is None:
                self.controller.add_order(order)
            else:
                self.controller.update_order(order_id, order)
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

    def _provider_names(self):
        return [
            provider["reason"]
            for provider in self.providers_controller.get_providers()
            if provider["reason"]
        ]

    def _filter_provider_values(self):
        names = self._provider_names()
        typed = self.customer_name.get().strip().lower()
        if typed:
            matches = [name for name in names if typed in name.lower()]
            if matches:
                names = matches
        self.provider_combo.configure(values=names)

    def _open_provider_search(self):
        providers = self.providers_controller.get_providers()
        if not providers:
            Messagebox.show_warning(
                "No hay proveedores registrados. Agrega uno primero.",
                title="Sin proveedores",
                parent=self,
            )
            return

        dialog = ttk.Toplevel(title="Buscar proveedor")
        dialog.geometry("640x460")
        dialog.minsize(560, 380)
        Utils.center_window(dialog)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ttk.Label(
            dialog,
            text="Seleccionar proveedor",
            font=("Helvetica", 15, "bold"),
        ).pack(pady=(12, 6))

        search_var = ttk.StringVar()
        search_entry = ttk.Entry(dialog, textvariable=search_var, bootstyle="light")
        search_entry.pack(fill=X, padx=14, pady=(0, 8))

        tree_frame = ttk.Frame(dialog, padding=(14, 0))
        tree_frame.pack(fill=BOTH, expand=YES)

        columns = ("razon", "rif", "telefono", "contacto")
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            bootstyle="light",
            selectmode="browse",
        )
        for column, text in (
            ("razon", "RAZÓN SOCIAL"),
            ("rif", "RIF"),
            ("telefono", "TELÉFONO"),
            ("contacto", "CONTACTO"),
        ):
            tree.heading(column, text=text)
        tree.column("razon", width=240, anchor=W)
        tree.column("rif", width=100, anchor=W)
        tree.column("telefono", width=110, anchor=W)
        tree.column("contacto", width=150, anchor=W)

        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        provider_map = {str(provider["id_provider"]): provider for provider in providers}

        def populate(*_args):
            text = search_var.get().strip().lower()
            for item in tree.get_children():
                tree.delete(item)
            for provider in providers:
                rif = "".join(
                    part
                    for part in (provider["rif_prefix"], provider["rif_number"])
                    if part
                )
                searchable = " ".join(
                    str(part or "")
                    for part in (
                        provider["reason"],
                        rif,
                        provider["contact_phone"],
                        provider["contact_email"],
                        provider["conatct_name"],
                        provider["state"],
                        provider["city"],
                    )
                ).lower()
                if text and text not in searchable:
                    continue
                tree.insert(
                    "",
                    END,
                    iid=str(provider["id_provider"]),
                    values=(
                        provider["reason"] or "",
                        rif,
                        provider["contact_phone"] or "",
                        provider["conatct_name"] or "",
                    ),
                )

        def select(*_args):
            selection = tree.selection()
            if not selection:
                Messagebox.show_warning(
                    "Selecciona un proveedor de la lista.",
                    title="Sin selección",
                    parent=dialog,
                )
                return
            provider = provider_map[selection[0]]
            self.customer_name.set(provider["reason"] or "")
            dialog.destroy()

        search_var.trace_add("write", populate)
        tree.bind("<Double-1>", select)
        tree.bind("<Return>", select)
        populate()
        search_entry.focus_set()

        actions = ttk.Frame(dialog)
        actions.pack(fill=X, padx=14, pady=12)
        ttk.Button(
            actions,
            text="Seleccionar",
            bootstyle="success",
            command=select,
        ).pack(side=RIGHT)
        ttk.Button(
            actions,
            text="Cancelar",
            bootstyle="danger-outline",
            command=dialog.destroy,
        ).pack(side=RIGHT, padx=(0, 8))

        