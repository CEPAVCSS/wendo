from re import sub
from tkinter import BOTH, YES

import ttkbootstrap as ttk
from ttkbootstrap.widgets import Tableview
from utils.utils import Utils
from controllers.providers_controller import *
class ProvidersView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.master = master
        self.controller = ProvidersController(master)
        self.container = ttk.Frame(master, padding=8).pack(side="left", fill="y")
        self.App_title = "Proveedores"
        ttk.Label(self.container, text=self.App_title, font=("Helvetica", 16, "bold")).pack(pady=10)
        # ttk.Button(self.container, text="Agregar Proveedor", bootstyle="@neutral", command=lambda: self.agregar_proveedor(self.master)).pack(pady=2)
        # ttk.Button(self.container, text="Ver Proveedores", bootstyle="@neutral").pack(pady=2)

        self.show_providers()

    def agregar_proveedor(self, master=None):
        #---Ventana emergente para agregar un proveedor---#
        ventana_agregar = ttk.Toplevel("master")
        ventana_agregar.title("Agregar Proveedor")
        ventana_agregar.geometry("400x300")
        Utils.center_window(ventana_agregar)

        ventana_agregar.resizable(False, False)

        ttk.Label(ventana_agregar, text="Agregar Proveedor", font=("Helvetica", 16, "bold")).pack(pady=10)
        ttk.Button(ventana_agregar, text="Guardar", bootstyle="success", command=ventana_agregar.destroy).pack(pady=10)


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
