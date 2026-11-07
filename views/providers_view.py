from re import sub

import ttkbootstrap as ttk
from ttkbootstrap.widgets import Tableview
from utils.utils import Utils
from controllers.providers_controller import *
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry
class ProvidersView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.master = master
        self.controller = ProvidersController(master)
        
        self.container = ttk.Frame(master, padding=8).pack(side="left", fill="y")

        self.container.rowconfigure(2, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.App_title = "Proveedores"
        ttk.Label(self.container, text=self.App_title, font=("Helvetica", 16, "bold")).pack(pady=10)
        ttk.Button(self.container, text="Agregar Proveedor", bootstyle="@neutral", command=lambda: self.agregar_proveedor(self.master)).pack(pady=2)
        # ttk.Button(self.container, text="Ver Proveedores", bootstyle="@neutral").pack(pady=2)

        self.show_providers()

    def agregar_proveedor(self, master=None):

    #---Ventana emergente para agregar un proveedor---#
        ventana_agregar = ttk.Toplevel(master)
        ventana_agregar.title("Formulario de Agregar Proveedor")
        ventana_agregar.geometry("850x550")
        Utils.center_window(ventana_agregar)
        
        #---Sección de Información del Proveedor---#

        ttk.Label(ventana_agregar, text="Formulario de Proveedor", font=("Helvetica", 16, "bold")).pack(pady=10)


        labelframe_contacto = ttk.Labelframe(ventana_agregar, text="Información del Proveedor", padding=15)
        labelframe_contacto.pack(fill="both", expand=True, padx=15, pady=10)

        fila_1 = ttk.Frame(labelframe_contacto)
        fila_1.pack(fill="x", pady=(0, 5))

        fila_2 = ttk.Frame(labelframe_contacto)
        fila_2.pack(fill="x", pady=(0, 5))

        fila_3 = ttk.Frame(labelframe_contacto)
        fila_3.pack(fill="x", pady=(0, 5))

        fila_4 = ttk.Frame(labelframe_contacto)
        fila_4.pack(fill="x", pady=(0, 5))

        for fila in (fila_1, fila_2, fila_3, fila_4):
            fila.columnconfigure((0, 1), weight=1, uniform="col")

        posicion_botones = ttk.Frame(ventana_agregar)
        posicion_botones.pack(pady=15,)

        
# Campos de Datos del Proveedor.


        #---Columna Izquierda (RIF, Razón Social, Tipo de Contribuyente, Estado)---#

        columna_registro = ttk.Frame(fila_1)
        columna_registro.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Label(columna_registro, text="RIF (Registro de Información Fiscal)", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(5, 0))

        fila_rif = ttk.Frame(columna_registro)
        fila_rif.pack(anchor="w", fill="x", pady=(0, 8))

        combox_rif_tipo = ttk.Combobox(fila_rif, values=["V", "J", "E", "G", "C"], width=3, state="readonly")
        combox_rif_tipo.pack(side="left", padx=(0, 5))

        entry_rif = ttk.Entry(fila_rif, width=40)
        entry_rif.pack(side="left", fill="x", expand=True)

        columna_Razón_Social = ttk.Frame(fila_2)
        columna_Razón_Social.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Label(columna_Razón_Social, text="Razón Social / Nombre Completo", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(5, 0))
        ttk.Entry(columna_Razón_Social, width=40).pack(anchor="w", fill="x", pady=(0, 8))

        columna_contrib = ttk.Frame(fila_3)
        columna_contrib.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Label(columna_contrib, text="Tipo de Contribuyente (SENIAT)", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(5, 0))
        combo_contrib = ttk.Combobox(columna_contrib, values=["Ordinario", "Especial", "Formal", "No Sujeto"], state="readonly")
        combo_contrib.pack(anchor="w", fill="x", pady=(0, 8))

        columna_estado = ttk.Frame(fila_4)
        columna_estado.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Label(columna_estado, text="Estado / Región", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(5, 0))
        combo_estado = ttk.Combobox(columna_estado, values=["Distrito Capital", "Miranda", "Zulia", "Aragua", "Carabobo", "Lara", "Aragua", "Anzoátegui", "Yaracuy", "Bolívar", "Trujillo", "Táchira", "Nueva Esparta", "Sucre", "Portuguesa", "Mérida", "Amazonas", "Apure", "Barinas", "Cojedes", "Delta Amacuro", "Falcón", "Guárico", "Monagas", "La Guaira", "Otros"], state="readonly")
        combo_estado.pack(anchor="w", fill="x", pady=(0, 8))

        #---Quitar la selección de los combobox al hacer clic en otro lugar---#
        for combo in (combox_rif_tipo, combo_contrib, combo_estado):
            combo.bind("<<ComboboxSelected>>", lambda e: e.widget.selection_clear())

        #---Columna Derecha (Telefono, Correo, Persona de Contacto, Dirección Fiscal)---#

        columna_telefono = ttk.Frame(fila_1)
        columna_telefono.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        ttk.Label(columna_telefono, text="Teléfono:", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(5, 0))

        #---Validación solo números y simbolos---#
        def solo_numeros_y_simbolos(texto):
            return all(c.isdigit() or c in "-+# " for c in texto)

        validar_telefono = ventana_agregar.register(solo_numeros_y_simbolos)

        entry_telefono = ttk.Entry(columna_telefono, width=40, validate="key", validatecommand=(validar_telefono, "%P"))
        entry_telefono.pack(anchor="w", fill="x", pady=(0, 8))

    #---------------------------------------------------------------#

        columna_Correo = ttk.Frame(fila_2)
        columna_Correo.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        ttk.Label(columna_Correo, text="Correo Electrónico:", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(5, 0))
        ttk.Entry(columna_Correo, width=40).pack(anchor="w", fill="x", pady=(0, 8))

        columna_contacto = ttk.Frame(fila_3)
        columna_contacto.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        ttk.Label(columna_contacto, text="Persona de Contacto:", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(5, 0))
        ttk.Entry(columna_contacto, width=40).pack(anchor="w", fill="x", pady=(0, 8))

        columna_Direccion = ttk.Frame(fila_4)
        columna_Direccion.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        ttk.Label(columna_Direccion, text="Dirección Fiscal Detallada", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(5, 0))
        ttk.Entry(columna_Direccion, width=40).pack(anchor="w", fill="x", pady=(0, 8))

        #---Sección Inferior (Fecha de Registro y Botones)---#

        seccion_inferior = ttk.Frame(ventana_agregar)
        seccion_inferior.pack(fill="x", padx=15, pady=(5, 15))

        #---Fecha de Registro---#
        frame_fecha = ttk.Frame(seccion_inferior)
        frame_fecha.pack(side="left")
        ttk.Label(frame_fecha, text="Fecha de Registro:", font=("Helvetica", 9, "italic")).pack(side="left", padx=(0, 8))
        date_entry = DateEntry(frame_fecha, bootstyle="success", width=12)
        date_entry.pack(side="left")

        #---Botones (Guardar y Cancelar)---#
        posicion_botones = ttk.Frame(seccion_inferior)
        posicion_botones.pack(side="right")

        boton_guardar = ttk.Button(posicion_botones, text="Guardar Proveedor", bootstyle="success", command=ventana_agregar.destroy)
        boton_guardar.pack(side="left", padx=(0, 8))

        boton_cancelar = ttk.Button(posicion_botones, text="Cancelar", bootstyle="danger-outline", command=ventana_agregar.destroy)
        boton_cancelar.pack(side="left")

        #---Configuración de la ventana emergente---#
        ventana_agregar.resizable(False, False)



    def show_providers(self):

        headers, proveedores = self.controller.providers

        if not proveedores:
            ttk.Label(self.container, text="No hay proveedores disponibles.", font=("Helvetica", 12)).pack(pady=10)
        else:   
            tabla_proveedores = Tableview(self.container, 
                                          coldata=headers,
                                          rowdata=proveedores,
                                          bootstyle="info",
                                          autofit=True,
                                          autoalign=True,
                                          paginated=True,
                                          searchable=True,)
            
            tabla_proveedores.pack(pady=10)
