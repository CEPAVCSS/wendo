import ttkbootstrap as ttk
from tkinter import StringVar 
from ttkbootstrap.constants import BOTH, LEFT, YES, RIGHT, X, Y, CENTER, W, E, VERTICAL, END
from ttkbootstrap.widgets import Tableview
from utils.utils import Utils

class OrdersView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.pack(fill=BOTH, expand=YES)
        self.container = ttk.Frame(self, padding=8)
        self.container.pack(side=LEFT, fill=Y)
        self.App_title = "Pedidos"
        ttk.Label(self.container, text=self.App_title, font=("Helvetica", 16, "bold")).pack(pady=10)
        ttk.Button(self.container, text="Agregar Pedido", bootstyle="primary", command=self.agregar_pedido).pack(pady=4, fill=X)
        ttk.Button(self.container, text="Ver Pedidos", bootstyle="outline-secondary").pack(pady=4, fill=X)

        # ÁREA PRINCIPAL (DERECHA: FILTROS + TREEVIEW)
        self.main_area = ttk.Frame(self, padding=12)
        self.main_area.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Barra Superior de Filtros
        self.setup_filters()

        # Tabla / Treeview
        self.setup_treeview()

    def setup_filters(self):
        filter_frame = ttk.Frame(self.main_area, padding=(0, 0, 0, 10))
        filter_frame.pack(fill=X)

        ttk.Label(filter_frame, text="FILTROS:", font=("Helvetica", 9, "bold"), bootstyle="secondary").pack(side=LEFT, padx=(0, 10))

        # Botones estilo filtro
        ttk.Button(filter_frame, text="Todos (5)", bootstyle="primary-outline").pack(side=LEFT, padx=2)
        ttk.Button(filter_frame, text="Ventas (3)", bootstyle="secondary-outline").pack(side=LEFT, padx=2)
        ttk.Button(filter_frame, text="Compras (2)", bootstyle="secondary-outline").pack(side=LEFT, padx=2)

        # Buscador
        search_entry = ttk.Entry(filter_frame, bootstyle="light")
        search_entry.pack(side=RIGHT)
        search_entry.insert(0, "Filtrar por referencia...")

    def setup_treeview(self):
        # Frame contenedor para Treeview y Scrollbar
        tree_frame = ttk.Frame(self.main_area)
        tree_frame.pack(fill=BOTH, expand=YES)

        columns = ("check", "orden", "fecha", "tipo", "asociado", "monto", "metodo", "estado", "acciones")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            bootstyle="light"
        )

        # Cabeceras
        self.tree.heading("check", text="☐")
        self.tree.heading("orden", text="N° ORDEN / REF")
        self.tree.heading("fecha", text="FECHA EMISIÓN")
        self.tree.heading("tipo", text="TIPO")
        self.tree.heading("asociado", text="ASOCIADO A")
        self.tree.heading("monto", text="MONTO")
        self.tree.heading("metodo", text="MÉTODO PAGO")
        self.tree.heading("estado", text="ESTADO")

        # Anchos de columnas
        self.tree.column("check", width=40, anchor=CENTER)
        self.tree.column("orden", width=120, anchor=W)
        self.tree.column("fecha", width=110, anchor=W)
        self.tree.column("tipo", width=90, anchor=CENTER)
        self.tree.column("asociado", width=220, anchor=W)
        self.tree.column("monto", width=100, anchor=E)
        self.tree.column("metodo", width=120, anchor=W)
        self.tree.column("estado", width=110, anchor=CENTER)

        # Etiquetas (Tags) de colores para los estados
        self.tree.tag_configure("pagado", background="#D1E7DD", foreground="#0F5132")
        self.tree.tag_configure("pendiente", background="#FFF3CD", foreground="#664D03")
        self.tree.tag_configure("entregado", background="#CFE2FF", foreground="#084298")

        # Cargar Datos de prueba
        datos = [
            ("☐", "ORD-2024-8841", "22 Sep 2024", "Venta", "Inversiones Médicas Pacífico", "$12,850.00", "Transferencia", "Pagado",),
            ("☐", "OC-2024-1092", "20 Sep 2024", "Compra", "Suministros Industriales Norte", "$6,400.00", "Crédito 30 Días", "Pendiente",),
            ("☐", "ORD-2024-8840", "19 Sep 2024", "Venta", "Distribuidora Mayorista", "$14,200.00", "Transferencia", "Pendiente"),
            ("☐", "ORD-2024-8835", "18 Sep 2024", "Venta", "Tecnología e Informática Quantum", "$21,870.00", "Tarjeta Corp.", "Entregado")
        ]

        for item in datos:
            estado_tag = item[7].lower()
            self.tree.insert("", "end", values=item, tags=(estado_tag,))

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        # marcar/desmarcar casillas
        self.tree.bind("<Button-1>", self.on_click_cell)

    def on_click_cell(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            col = self.tree.identify_column(event.x)
            item_id = self.tree.identify_row(event.y)
            if col == "#1":  # Columna Checkbox
                valores = list(self.tree.item(item_id, "values"))
                valores[0] = "☑" if valores[0] == "☐" else "☐"
                self.tree.item(item_id, values=valores)

    def agregar_pedido(self, master=None):
            #---Ventana emergente para agregar un pedido---#
            ventana_agregar = ttk.Toplevel(master)
            ventana_agregar.title("Agregar Pedido")
            ventana_agregar.geometry("920x280")
            Utils.center_window(ventana_agregar)
    
            ventana_agregar.resizable(False, False)
    
            #Registro Rapido de los pedidos
            form_frame = ttk.Labelframe(ventana_agregar, text ="Formulario de Registro Rapido", padding=15, bootstyle="info")
            form_frame.pack(fill=BOTH, expand=YES, padx=15, pady=15)

            #Tipo de Movimiento 
            ttk.Label(form_frame, text= "TIPO DE MOVIMIENTO", font=("Helvetica", 8, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=(0, 5))

            tipo_var = ttk.StringVar(value="Venta")
            frame_tipo = ttk.Frame(form_frame)
            frame_tipo.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

            ttk.Radiobutton(frame_tipo, text="Venta", variable=tipo_var, value="Venta", bootstyle="outline-toolbutton").pack(side=LEFT, expand=True, fill=BOTH)
            ttk.Radiobutton(frame_tipo, text="Compra", variable=tipo_var, value="Compra", bootstyle="outline-toolbutton").pack(side=LEFT, expand=True, fill=BOTH)

            #Cliente/Proveedor
            ttk.Label(form_frame, text="ENTIDAD (CLIENTE / PROVEEDOR)", font=("Helvetica", 8, "bold")).grid(row=0, column=1, sticky="w", padx=5, pady=(0, 5))
            entry_entidad = ttk.Entry(form_frame)
            entry_entidad.insert(0, "Ej. Logística Global Andina S.A.")
            entry_entidad.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

            #Monto/Moneda
            ttk.Label(form_frame, text="MONTO & MONEDA", font=("Helvetica", 8, "bold")).grid(row=0, column=2, sticky="w", padx=5, pady=(0, 5))
            frame_monto = ttk.Frame(form_frame)
            frame_monto.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
        
            moneda = ttk.Combobox(frame_monto, values=["USD ($)", "EUR (€)", "BS (Bs.)"], width=8, state="readonly")
            moneda.current(0)
            moneda.pack(side=LEFT, padx=(0, 5))
        
            entry_monto = ttk.Entry(frame_monto)
            entry_monto.insert(0, "0.00")
            entry_monto.pack(side=LEFT, fill=X, expand=True)

            # Método de Pago
            ttk.Label(form_frame, text="MÉTODO DE PAGO", font=("Helvetica", 8, "bold")).grid(row=0, column=3, sticky="w", padx=5, pady=(0, 5))
            pago = ttk.Combobox(form_frame, values=["Transferencia Bancaria", "Efectivo", "Tarjeta de Crédito"], state="readonly")
            pago.current(0)
            pago.grid(row=1, column=3, sticky="ew", padx=5, pady=5)