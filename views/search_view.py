import ttkbootstrap as ttk
from ttkbootstrap.constants import (
    BOTH,
    CENTER,
    END,
    LEFT,
    RIGHT,
    VERTICAL,
    W,
    X,
    Y,
    YES,
)

from controllers.search_controller import SearchController


class SearchView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.pack(fill=BOTH, expand=YES)
        self.controller = SearchController()
        self.current_category = "Todo"
        self.search_text = ""
        self.card_values = {}
        self.card_captions = {}
        self.filter_buttons = {}

        self._build_header()
        self._build_cards()
        self._build_search_bar()
        self._build_filters()
        self._build_results()
        self.refresh()

    def _build_header(self):
        ttk.Label(
            self,
            text="Búsqueda global",
            font=("Helvetica", 18, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            self,
            text="Resumen del negocio y búsqueda en contactos, proveedores, pedidos y tareas",
            font=("Helvetica", 10),
            bootstyle="secondary",
        ).pack(anchor="w", pady=(0, 10))

    def _build_cards(self):
        cards = ttk.Frame(self)
        cards.pack(fill=X, pady=(0, 12))
        for column in range(3):
            cards.columnconfigure(column, weight=1, uniform="card")

        specs = (
            ("contacts", "Contactos", "primary"),
            ("providers", "Proveedores", "info"),
            ("orders", "Pedidos", "warning"),
            ("tasks", "Tareas", "success"),
            ("orders_amount", "Monto en pedidos", "primary"),
            ("paid_orders", "Pedidos pagados", "success"),
        )
        for index, (key, title, accent) in enumerate(specs):
            card = ttk.Frame(
                cards,
                padding=12,
                bootstyle="light",
                borderwidth=1,
                relief="solid",
            )
            card.grid(
                row=index // 3,
                column=index % 3,
                sticky="nsew",
                padx=4,
                pady=4,
            )
            ttk.Label(
                card,
                text=title.upper(),
                font=("Helvetica", 8, "bold"),
                bootstyle=accent,
            ).pack(anchor="w")
            value = ttk.Label(card, text="0", font=("Helvetica", 20, "bold"))
            value.pack(anchor="w", pady=(2, 0))
            caption = ttk.Label(
                card,
                text="",
                font=("Helvetica", 8),
                bootstyle="secondary",
            )
            caption.pack(anchor="w")
            self.card_values[key] = value
            self.card_captions[key] = caption

    def _build_search_bar(self):
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=X, pady=(0, 8))

        self.search_var = ttk.StringVar()
        self.search_var.trace_add("write", lambda *_args: self._on_search())
        entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            bootstyle="light",
        )
        entry.pack(side=LEFT, fill=X, expand=True)
        entry.bind("<Return>", lambda _event: self.execute_search())

        ttk.Button(
            search_frame,
            text="Buscar",
            bootstyle="primary",
            command=self.execute_search,
        ).pack(side=LEFT, padx=(8, 0))
        ttk.Button(
            search_frame,
            text="Limpiar",
            bootstyle="outline-secondary",
            command=self._clear_search,
        ).pack(side=LEFT, padx=(8, 0))

    def _build_filters(self):
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill=X, pady=(0, 8))

        ttk.Label(
            filter_frame,
            text="FILTROS:",
            font=("Helvetica", 9, "bold"),
            bootstyle="secondary",
        ).pack(side=LEFT, padx=(0, 10))

        categories = (
            ("Todo", "Todo"),
            ("Contactos", "Contactos"),
            ("Proveedores", "Proveedores"),
            ("Pedidos", "Pedidos"),
            ("Tareas", "Tareas"),
        )
        for key, label in categories:
            button = ttk.Button(
                filter_frame,
                text=label,
                bootstyle="primary" if key == "Todo" else "secondary-outline",
                command=lambda current=key: self._set_category(current),
            )
            button.pack(side=LEFT, padx=2)
            self.filter_buttons[key] = button

        self.results_label = ttk.Label(filter_frame, text="", bootstyle="secondary")
        self.results_label.pack(side=RIGHT)

    def _build_results(self):
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=BOTH, expand=YES)

        columns = ("tipo", "titulo", "detalle", "estado")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            bootstyle="light",
        )

        headings = {
            "tipo": "TIPO",
            "titulo": "NOMBRE / REFERENCIA",
            "detalle": "DETALLE",
            "estado": "ESTADO",
        }
        for column, text in headings.items():
            self.tree.heading(column, text=text)

        widths = {
            "tipo": (110, CENTER),
            "titulo": (200, W),
            "detalle": (400, W),
            "estado": (120, CENTER),
        }
        for column, (width, anchor) in widths.items():
            self.tree.column(column, width=width, anchor=anchor)

        self.tree.tag_configure("inactivo", background="#E2E3E5", foreground="#6C757D")
        self.tree.tag_configure("contacto", background="#D1E7DD", foreground="#0F5132")
        self.tree.tag_configure("proveedor", background="#CFE2FF", foreground="#084298")
        self.tree.tag_configure("pedido", background="#FFF3CD", foreground="#664D03")
        self.tree.tag_configure("tarea", background="#E2D9F3", foreground="#432874")

        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

    def _set_category(self, category):
        self.current_category = category
        for key, button in self.filter_buttons.items():
            button.configure(
                bootstyle="primary" if key == category else "secondary-outline"
            )
        self.execute_search()

    def _on_search(self):
        self.search_text = self.search_var.get().strip()
        self.execute_search()

    def _clear_search(self):
        self.search_var.set("")

    def refresh(self):
        stats = self.controller.get_dashboard_stats()
        self._update_cards(stats)
        self.execute_search()

    def _update_cards(self, stats):
        self.card_values["contacts"].configure(text=str(stats["contacts"]))
        self.card_captions["contacts"].configure(
            text=f"{stats['active_contacts']} activo(s)"
        )

        self.card_values["providers"].configure(text=str(stats["providers"]))
        self.card_captions["providers"].configure(text="Registrados")

        self.card_values["orders"].configure(text=str(stats["orders"]))
        self.card_captions["orders"].configure(
            text=f"{stats['pending_orders']} pendiente(s)"
        )

        self.card_values["tasks"].configure(text=str(stats["tasks"]))
        self.card_captions["tasks"].configure(
            text=f"{stats['pending_tasks']} pendiente(s)"
        )

        self.card_values["orders_amount"].configure(
            text=f"${float(stats['orders_amount'] or 0):,.2f}"
        )
        self.card_captions["orders_amount"].configure(text="Total registrado")

        self.card_values["paid_orders"].configure(text=str(stats["paid_orders"]))
        self.card_captions["paid_orders"].configure(
            text=f"de {stats['orders']} pedido(s)"
        )

    def execute_search(self):
        results = self.controller.search(self.search_text, self.current_category)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for result in results:
            tag = result["type"].lower()
            if (
                result["type"] == "Contacto"
                and result["status"].strip().lower() == "inactivo"
            ):
                tag = "inactivo"
            self.tree.insert(
                "",
                END,
                values=(
                    result["type"],
                    result["title"],
                    result["detail"],
                    result["status"],
                ),
                tags=(tag,),
            )

        if results:
            self.results_label.configure(text=f"{len(results)} resultado(s)")
        else:
            self.results_label.configure(text="Sin resultados")
