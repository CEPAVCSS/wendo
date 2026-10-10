import ttkbootstrap as ttk

class OrdersView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.container = ttk.Frame(master, padding=8).pack(side="left", fill="y")
        self.App_title = "Pedidos"
        ttk.Label(self.container, text=self.App_title, font=("Helvetica", 16, "bold")).pack(pady=10)
        ttk.Button(self.container, text="Agregar Pedido", bootstyle="@neutral").pack(pady=2)
        ttk.Button(self.container, text="Ver Pedidos", bootstyle="@neutral").pack(pady=2)