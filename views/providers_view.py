from re import sub
from tkinter import BOTH, YES

import ttkbootstrap as ttk
from utils.utils import Utils
from controllers.providers_controller import *
class ProvidersView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.master = master
        self.container = ttk.Frame(master, padding=8).pack(side="left", fill="y")
        self.App_title = "Proveedores"
        ttk.Label(self.container, text=self.App_title, font=("Helvetica", 16, "bold")).pack(pady=10)
        # ttk.Button(self.container, text="Agregar Proveedor", bootstyle="@neutral", command=lambda: self.agregar_proveedor(self.master)).pack(pady=2)
        # ttk.Button(self.container, text="Ver Proveedores", bootstyle="@neutral").pack(pady=2)



        # Notebook para mostrar las diferentes vistas
        self.notebook = ttk.Notebook(self.container)
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)


        # Tab que muestra la lista de proveedores
        lista_proveedores = ttk.Frame(self.notebook, padding=16)
        ttk.Label(lista_proveedores, text="Lista de Proveedores").pack()
        self.notebook.add(lista_proveedores, text="Lista de Proveedores")


        # Tab que permite agregar un nuevo proveedor
        agregar_proveedor_tab = ttk.Frame(self.notebook, padding=16)
        ttk.Label(agregar_proveedor_tab, text="Agregar Proveedor").pack()
        self.notebook.add(agregar_proveedor_tab, text="Agregar Proveedor")




    # def agregar_proveedor(self, master=None):
    #     #---Ventana emergente para agregar un proveedor---#
    #     ventana_agregar = ttk.Toplevel(master)
    #     ventana_agregar.title("Agregar Proveedor")
    #     ventana_agregar.geometry("400x300")
    #     Utils.center_window(ventana_agregar)

    #     ventana_agregar.resizable(False, False)

    #     ttk.Label(ventana_agregar, text="Agregar Proveedor", font=("Helvetica", 16, "bold")).pack(pady=10)
    #     ttk.Button(ventana_agregar, text="Guardar", bootstyle="success", command=ventana_agregar.destroy).pack(pady=10)


    # def proveedor_view(self, master):

    #     from views.providers_view import ProvidersView
        
    #     view = ProvidersView(master, on_agregar=self.agregar_proveedor)
    #     view.pack(side="left", fill="y")
        
    #     return self.proveedor_view