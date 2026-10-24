import os
import ttkbootstrap as ttk
from PIL import Image, ImageTk
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
            )
        self.menu.pack(side="left", fill="y")
        
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

        #Logo de la aplicación
    
        self.path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "wendo-logo.png")
        with Image.open(self.path) as logo:
            logo.thumbnail((140, 90), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(logo, master=self.menu)
        ttk.Label(self.menu, image=self.logo_image,
            padding=8,
            bootstyle="@light", 
            background="#FFFFFF",
        ).pack(pady=(5, 10))
        
        # ttk.Label(self.menu, 
        #           text=self.App_title, 
        #           font=("Helvetica", 16, "bold"),
        #           foreground="#1E3A8A",
        #           background="#FFFFFF",
        #     ).pack(pady=10)   
                
        
        ttk.Button(self.menu, icon="search", text="Buscar", bootstyle="Menu.TButton", command=self.buscar, style="Menu.TButton").pack( pady=2, fill="x")
        ttk.Button(self.menu, icon="person", text="Contactos", bootstyle="Menu.TButton", command=self.contactos).pack( pady=2, fill="x")
        ttk.Button(self.menu, icon="truck", text="Proveedores", bootstyle="Menu.TButton", command=self.proveedores).pack( pady=2, fill="x")
        ttk.Button(self.menu, icon="cart", text="Pedidos", bootstyle="Menu.TButton", command=self.pedidos).pack( pady=2, fill="x")
        ttk.Button(self.menu, icon="check-circle", text="Tareas", bootstyle="Menu.TButton", command=self.tareas).pack(pady=2, fill="x")

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
  