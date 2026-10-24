import ttkbootstrap as ttk
from utils.utils import Utils

def agregar_proveedor(master=None):

    #---Ventana emergente para agregar un proveedor---#
    ventana_agregar = ttk.Toplevel(master)
    ventana_agregar.title("Agregar Proveedor")
    ventana_agregar.geometry("400x300")
    Utils.center_window(ventana_agregar)

    ventana_agregar.resizable(False, False)

    ttk.Label(ventana_agregar, text="Agregar Proveedor", font=("Helvetica", 16, "bold")).pack(pady=10)
    ttk.Button(ventana_agregar, text="Guardar", bootstyle="success", command=ventana_agregar.destroy).pack(pady=10)


def proveedor_view(master):

    from views.providers_view import ProvidersView
    
    view = ProvidersView(master, on_agregar=agregar_proveedor)
    view.pack(side="left", fill="y")
    
    return proveedor_view