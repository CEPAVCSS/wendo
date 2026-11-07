import ttkbootstrap as ttk
from ttkbootstrap.widgets import Tableview
from controllers.todo_controller import TodoController
from utils.utils import Utils

class TodoView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.master = master
        self.container = ttk.Frame(master, padding=8)
        self.container.pack(fill="both", expand=True)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(3, weight=1)
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
        ttk.Button(self.container, 
                   text="Agregar Tarea Rápida", 
                   command=self.agregar_tarea,
                   bootstyle="primary").grid(row=1, column=1, pady=2)
        
        self.show_tasks()

    def show_tasks(self):
        # Datos de la tabla de tareas
        self.header, self.pending_tasks, self.complete_tasks = self.controller.get_tasks()
        columns = [
            {"text": self.header[0], "width": 180, "minwidth": 100, "stretch": True},
            {"text": self.header[1], "width": 130, "minwidth": 95, "stretch": True},
            {"text": self.header[2], "width": 110, "minwidth": 80, "stretch": True},
            {"text": self.header[3], "width": 260, "minwidth": 120, "stretch": True},
            {"text": self.header[4], "width": 130, "minwidth": 95, "stretch": True},
        ]
        self.tasks_table = Tableview(
            self.container,
            coldata=columns,
            rowdata=self.pending_tasks,
            bootstyle="primary",
            autofit=False,
            autoalign=True,
            paginated=True,
            yscrollbar=True,
        )
        self.tasks_table.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

    def agregar_tarea(self):
        self.ventana_agregar = ttk.Toplevel(title="Agregar Tarea")
        self.ventana_agregar.geometry("400x400")
        Utils.center_window(self.ventana_agregar)
        # self.ventana_agregar.resizable(False, False)


        # titulo ventana
        new_task = ttk.Labelframe(self.ventana_agregar,
                      text="Nueva Tarea",
                      bootstyle="primary",
                      padding=12)
        new_task.pack(fill="x", padx=10, pady=10)

        # Campos de entrada para la nueva tarea
        self.tarea = ttk.StringVar()
        ttk.Label(new_task, text="Tarea").pack(anchor="w")
        ttk.Entry(new_task, textvariable=self.tarea).pack(fill="x")

        ttk.Label(new_task, text="Fecha Límite (YYYY-MM-DD):").pack(anchor="w")
        self.fecha = ttk.DateEntry(new_task).pack(fill="x")

        ttk.Label(new_task, text="Prioridad").pack(anchor="w")
        self.prioridad = ttk.StringVar()
        ttk.Combobox(new_task,textvariable=self.prioridad, values=["Alta", "Media", "Baja"]).pack(fill="x")

        
        ttk.Label(new_task, text="Descripción").pack(anchor="w")
        self.desc = ttk.Text(new_task, height=5).pack(fill="x")

        ttk.Button(self.ventana_agregar, text="Crear Tarea", bootstyle="primary", command=self.crear_tarea).pack(fill="x", pady=3, padx=10)

    def crear_tarea(self):

        self.new_task = {
                    "tarea" : self.tarea.get(),
                    "fecha" : self.fecha.get_date(),
                    "prioridad" : self.prioridad.get(),
                    "descripcion" : self.desc.get("1.0", "end-1c")
                }

        # print(f"Creando tareas...{self.new_task}")
        self.controller.model.add_task(self.new_task)
        self.ventana_agregar.destroy()
        self.tasks_table.destroy()
        self.show_tasks()
