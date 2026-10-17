import ttkbootstrap as ttk
from ttkbootstrap.widgets import Tableview
from controllers.todo_controller import TodoController

class TodoView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.container = ttk.Frame(master, padding=8)
        self.container.pack(side="left", fill="y")
        self.App_title = "Lista de Tareas y Seguimiento operativo"
        self.controller = TodoController(self.container)

        #badge
        ttk.Label(self.container, 
                  text="PRODUCTIVIDAD DIARIA", 
                  bootstyle="primary", 
                  font=("Helvetica", 7, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 10))

        #Titulo de la ventana
        ttk.Label(self.container, 
                  text=self.App_title, 
                  anchor="w",
                  justify="left",
                  font=("Helvetica", 16, "bold")).grid(row=1, column=0, sticky="w")

        ttk.Label(self.container, 
                  text="Gestión de pendientes, prioridades comerciales y fechas límites con resolución rápida", 
                  anchor="w",
                  justify="left",
                  font=("Helvetica", 12)).grid(row=2, column=0, sticky="w")


        # Botón para agregar una nueva tarea
        ttk.Button(self.container, text="Agregar Tarea Rápida", bootstyle="primary").grid(row=1, column=1, pady=2)
        
        
        # Datos de la tabla de tareas
        self.header, self.pending_tasks, self.complete_tasks = self.controller.tasks

        table = Tableview(
        self.container,
        coldata=self.header,
        rowdata=self.pending_tasks,
        bootstyle="primary",
        autofit=True,
        autoalign=True,
      
        paginated=True,).grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")
        self.container.grid_rowconfigure(3, weight=1)

       
          
        # ttk.Button(self.container, text="Agregar Tarea", bootstyle="@neutral").grid(row=1, column=0, pady=2)
        # ttk.Button(self.container, text="Ver Tareas", bootstyle="@neutral").grid(row=2, column=0, pady=2)