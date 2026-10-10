import ttkbootstrap as ttk
import views.search_view as SV
import views.contacts_view as CV
import views.providers_view as SupV
import views.orders_view as OV
import views.todo_view as TV

class Sidebar(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)

        self.App_title = "Wendo"
        self.menu = ttk.Frame(
            master, 
            padding=8,
            bootstyle="@light",
            width=200
            ).pack(side="left", fill="y")
        
        self.topBar = ttk.Frame(
            master, 
            padding=8,
            bootstyle="@light",
            height=50
            ).pack(side="top", fill="x")

        self.content = ttk.Frame(
            master, 
            padding=8,
            borderwidth=8,
            bootstyle="bordered"
            ).pack(side="top", fill="both", expand=True)

        ttk.Label(self.menu, text=self.App_title, font=("Helvetica", 16, "bold")).pack(pady=10)
        
        ttk.Button(self.menu, text="Buscar", bootstyle="@neutral", command=self.buscar).pack( pady=2, fill="x")
        ttk.Button(self.menu, text="Contactos", bootstyle="@neutral", command=self.contactos).pack( pady=2, fill="x")
        ttk.Button(self.menu, text="Proveedores", bootstyle="@neutral", command=self.proveedores).pack( pady=2, fill="x")
        ttk.Button(self.menu, text="Pedidos", bootstyle="@neutral", command=self.pedidos).pack( pady=2, fill="x")
        ttk.Button(self.menu, text="Tareas", bootstyle="@neutral", command=self.tareas).pack(pady=2, fill="x")

    def buscar(self):
        # Implementar la funcionalidad de búsqueda aquí
        self.limpiar_contenido()
        SV.SearchView(master=self.content)

    def contactos(self):
        # Implementar la funcionalidad de búsqueda aquí
        self.limpiar_contenido()
        CV.ContactsView(master=self.content)

    def proveedores(self):
        # Implementar la funcionalidad de búsqueda aquí
        self.limpiar_contenido()
        SupV.ProvidersView(master=self.content)

    def pedidos(self):
        # Implementar la funcionalidad de búsqueda aquí
        self.limpiar_contenido()
        OV.OrdersView(master=self.content)

    def tareas(self):
        # Implementar la funcionalidad de búsqueda aquí
        self.limpiar_contenido()
        TV.TodoView(master=self.content)


    def limpiar_contenido(self):
        for child in self.content.winfo_children():
            child.destroy()
  