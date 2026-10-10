import ttkbootstrap as ttk

class TodoView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.container = ttk.Frame(master, padding=8)
        self.container.pack(side="left", fill="y")
        self.App_title = "Lista de Tareas y Seguimiento operativo"

        #Titulo de la ventana
        ttk.Label(self.container, 
                  text=self.App_title, 
                  anchor="w",
                  justify="left",
                  font=("Helvetica", 16, "bold")).grid(row=0, column=0)

        ttk.Label(self.container, 
                  text="Gestión de pendientes, prioridades comerciales y fechas límites con resolución rápida", 
                  font=("Helvetica", 12)).grid(row=1, column=0)
          
        ttk.Button(self.container, text="Agregar Tarea", bootstyle="@neutral").grid(row=1, column=0, pady=2)
        ttk.Button(self.container, text="Ver Tareas", bootstyle="@neutral").grid(row=2, column=0, pady=2)