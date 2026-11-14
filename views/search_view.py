



#Autor = "Chris"
# fecha = "2026-11-12"




import ttkbootstrap as ttk
from ttkbootstrap.widgets import DateEntry

class SearchView(ttk.Frame):
    def __init__(self, master, on_clientes=None):
        super().__init__(master, padding=8)
        self.master = master
        self.on_clientes = on_clientes or self.abrir_reportes
        self.pack(fill="both", expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        main_container = ttk.Frame(self)
        main_container.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        search_frame = ttk.Frame(main_container)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        search_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="🔍", font=("Segoe UI", 12)).grid(
            row=0, column=0, padx=(0, 8)
        )
        self.search_entry = ttk.Entry(search_frame, bootstyle="secondary")
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        self.search_entry.insert(0, "Escribe para buscar reportes...")
        self.search_entry.bind("<FocusIn>", self.limpiar_placeholder)

        ttk.Button(
            search_frame,
            text="Buscar",
            bootstyle="outline-neutral",
            command=self.ejecutar_busqueda,
        ).grid(row=0, column=2)

        actions_frame = ttk.Frame(main_container)
        actions_frame.grid(row=1, column=0, sticky="w")

        self.todo_el_sistema_btn = ttk.Button(
            actions_frame,
            icon="grid",
            text="Todo el Sistema",
            bootstyle="outline-neutral",
            command=self.abrir_reportes,
        )
        self.todo_el_sistema_btn.grid(row=0, column=0, padx=(0, 4))

        self.clientes_btn = ttk.Button(
            actions_frame,
            icon="person",
            text="Clientes",
            bootstyle="outline-neutral",
            command=self.on_clientes,
        )
        self.clientes_btn.grid(row=0, column=1, padx=4)

        self.proveedores_btn = ttk.Button(
            actions_frame,
            icon="truck",
            text="Proveedores",
            bootstyle="outline-neutral",
            command=self.abrir_reportes,
        )
        self.proveedores_btn.grid(row=0, column=2, padx=4)

        self.pedidos_y_facturas_btn = ttk.Button(
            actions_frame,
            icon="cart",
            text="Pedidos y Facturas",
            bootstyle="outline-neutral",
            command=self.abrir_reportes,
        )
        self.pedidos_y_facturas_btn.grid(row=0, column=3, padx=4)

        filters_frame = ttk.Frame(main_container)
        filters_frame.grid(row=2, column=0, sticky="w", pady=(8, 0))

        self.periodos_btn = ttk.Button(
            filters_frame,
            icon="calendar",
            text="Periodos",
            bootstyle="outline-neutral",
            command=self.mostrar_periodo,
        )
        self.periodos_btn.grid(row=0, column=0, sticky="w", padx=(0, 4))

        self.periodo_frame = ttk.Frame(main_container)
        ttk.Label(self.periodo_frame, text="Fecha:").grid(row=0, column=0, padx=(0, 6))
        self.fecha_periodo = DateEntry(self.periodo_frame, date_format="%Y-%m-%d")
        self.fecha_periodo.grid(row=0, column=1)

        ttk.Button(
            self.periodo_frame,
            text="Aplicar",
            bootstyle="outline-neutral",
            command=self.abrir_reportes,
        ).grid(row=0, column=2, padx=(6, 0))



        self.estados_btn = ttk.Button(
            filters_frame,
            icon="toggle-on",
            text="Estados",
            bootstyle="outline-neutral",
            command=self.abrir_reportes,
        )
        self.estados_btn.grid(row=0, column=1, sticky="w", padx=(4, 0))

        indicadores_frame = ttk.Frame(main_container)
        indicadores_frame.grid(row=3, column=0, sticky="w", pady=(8, 0))

        self.contactos_activos_btn = ttk.Labelframe(
            indicadores_frame,
            text="",
            bootstyle="secondary",
            padding=(10, 2, 10, 10),
        )
        self.contactos_activos_btn.grid(row=0, column=0, sticky="n", padx=(0, 4))

        ttk.Label(
            self.contactos_activos_btn,
            text="👥 Contactos Activos",
            bootstyle="secondary",
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        ttk.Label(
            self.contactos_activos_btn,
            text="67,632",
            foreground="#17141f",
            bootstyle="secondary",
            font=("Segoe UI", 18, "bold"),
        ).grid(row=1, column=0, sticky="w")

        ttk.Label(
            self.contactos_activos_btn,
            text="+3.5",
            bootstyle="success-inverse",
            font=("Segoe UI", 6, "bold"),
            padding=(6, 3),
        ).grid(row=1, column=1, padx=(4, 0))

        ttk.Label(
            self.contactos_activos_btn,
            text="982 Clientes\n  234 Proveedores",
            foreground="#17141f",
            bootstyle="secondary",
            font=("Segoe UI", 8, "bold"),
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))

        self.volumen_de_transaccionado_btn = ttk.Labelframe(
            indicadores_frame,
            text="",
            bootstyle="secondary",
            padding=(10, 2, 10, 10),
        )

        ttk.Label(
            self.volumen_de_transaccionado_btn,
            text="📊 Volumen de Transacciones",
            bootstyle="secondary",
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        volumen_valor_frame = ttk.Frame(self.volumen_de_transaccionado_btn)
        volumen_valor_frame.grid(row=1, column=0, sticky="w")

        ttk.Label(
            volumen_valor_frame,
            text="$65,653",
            foreground="#17141f",
            bootstyle="secondary",
            font=("Segoe UI", 18, "bold"),
        ).grid(row=0, column=0)

        ttk.Label(
            volumen_valor_frame,
            text="+14,5 bancarizados",
            bootstyle="success-inverse",
            font=("Segoe UI", 6, "bold"),
            padding=(6, 3),
        ).grid(row=0, column=1, padx=(4, 0))

        self.volumen_de_transaccionado_btn.grid(row=0, column=1, sticky="n", padx=(4, 0))

        ttk.Label(
            self.volumen_de_transaccionado_btn,
            text="98,4 bancarizados",
            bootstyle="secondary",
            foreground="#4602ff",
            font=("Segoe UI", 8, "bold"),
        ).grid(row=2, column=0, sticky="w", pady=(8, 0))

        self.pendientes_Liquidacion_btn = ttk.Labelframe(
            indicadores_frame,
            text="",
            bootstyle="secondary",
            padding=(10, 2, 10, 10),
        )
        self.pendientes_Liquidacion_btn.grid(row=0, column=2, sticky="n", padx=4)

        ttk.Label(
            self.pendientes_Liquidacion_btn,
            text="⏳ Pendientes de Liquidación",
            bootstyle="secondary",
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        ttk.Label(
            self.pendientes_Liquidacion_btn,
            text="$13,6332",
            foreground="#ff1e00",
            bootstyle="secondary",
            font=("Segoe UI", 18, "bold"),
        ).grid(row=1, column=0, columnspan=2, sticky="w")

        vencimiento_frame = ttk.Frame(self.pendientes_Liquidacion_btn)
        vencimiento_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))

        ttk.Label(
            vencimiento_frame,
            text="Vencimiento promedio: 12 días",
            bootstyle="secondary",
            font=("Segoe UI", 8, "bold"),
        ).grid(row=0, column=0)

        ttk.Label(
            vencimiento_frame,
            text="!",
            foreground="#ff1e00",
            font=("Segoe UI", 18, "bold"),
            bootstyle="secondary",
        ).grid(row=0, column=1, padx=(6, 0))




        self.cumplimiento_operativo_btn = ttk.Labelframe(
            indicadores_frame,
            text="",
            bootstyle="secondary",
            padding=(10, 2, 10, 10),
        )
        self.cumplimiento_operativo_btn.grid(row=0, column=3, sticky="n", padx=4)

        ttk.Label(
            self.cumplimiento_operativo_btn,
            text="Cumplimiento Operativo",
            bootstyle="secondary",
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        ttk.Label(
            self.cumplimiento_operativo_btn,
            text="98,4%",
            foreground="#000000",
            bootstyle="secondary",
            font=("Segoe UI", 18, "bold"),
        ).grid(row=1, column=0, sticky="w")































    def limpiar_placeholder(self, event):
        if self.search_entry.get() == "Escribe para buscar reportes...":
            self.search_entry.delete(0, "end")

    def ejecutar_busqueda(self):
        texto = self.search_entry.get().strip()
        if texto and texto != "Escribe para buscar reportes...":
            print(f"Buscando: {texto}")

    def abrir_reportes(self):
        print("Abriendo sección de reportes...")

    def mostrar_periodo(self):
        if self.periodo_frame.winfo_manager():
            self.periodo_frame.grid_remove()
        else:
            self.periodo_frame.grid(
                row=2, column=1, sticky="w", padx=(8, 0)
            )
