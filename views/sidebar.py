import ttkbootstrap as ttk

class Sidebar(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8, bootstyle="@neutral")

        self.App_title = "Wendo"

        self.background = "#FFFFFF"  # Color de fondo del sidebar
        ttk.Label(self, text=self.App_title.upper(), font=("Helvetica", 16, "bold"), background=self.background).pack(pady=10)
        ttk.Button(self, text="Buscar").pack( pady=2)
        ttk.Button(self, text="Contactos").pack( pady=2)
        ttk.Button(self, text="Proveedores").pack( pady=2)
        ttk.Button(self, text="Pedidos").pack( pady=2)
        ttk.Button(self, text="Tareas").pack(pady=2)
