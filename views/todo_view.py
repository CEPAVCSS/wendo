import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
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
        self.task_notebook = None
        self.task_tables = {}
        self.task_pages = {}
        self.selected_state = "Todas"

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

    def show_tasks(self, selected_state=None):
        if selected_state is None:
            selected_state = self.selected_state
        self.selected_state = selected_state

        if self.task_notebook:
            self.task_notebook.destroy()

        self.header, tasks = self.controller.get_tasks()
        columns = [
            {"text": "ID", "width": 0, "minwidth": 0, "stretch": False},
            {"text": self.header[0], "width": 180, "minwidth": 100, "stretch": True},
            {"text": self.header[1], "width": 130, "minwidth": 95, "stretch": True},
            {"text": self.header[2], "width": 110, "minwidth": 80, "stretch": True},
            {"text": self.header[3], "width": 260, "minwidth": 120, "stretch": True},
            {"text": self.header[4], "width": 130, "minwidth": 95, "stretch": True},
        ]
        self.task_notebook = ttk.Notebook(self.container, bootstyle="primary")
        self.task_notebook.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")
        self.task_tables = {}
        self.task_pages = {}

        states = (
            ("Todas", None),
            ("Pendientes", "Pendiente"),
            ("En progreso", "En progreso"),
            ("Completadas", "Completada"),
            ("Canceladas", "Cancelada"),
        )
        for label, status in states:
            page = ttk.Frame(self.task_notebook, padding=4)
            page.grid_columnconfigure(0, weight=1)
            page.grid_rowconfigure(0, weight=1)
            self.task_notebook.add(page, text=label)
            self.task_pages[label] = page

            visible_tasks = tasks if status is None else [
                task for task in tasks if task["status"] == status
            ]
            rowdata = [tuple(task) for task in visible_tasks]
            table = Tableview(
                page,
                coldata=columns,
                rowdata=rowdata,
                bootstyle="primary",
                autofit=False,
                autoalign=True,
                paginated=True,
                yscrollbar=True,
                iid_field=0,
            )
            table.tablecolumns[0].hide()
            table.grid(row=0, column=0, sticky="nsew")
            table.view.bind(
                "<Button-1>",
                lambda event, current_table=table: self._open_task_from_row(
                    event, current_table
                ),
                add="+",
            )
            self.task_tables[label] = table

        self.task_notebook.bind("<<NotebookTabChanged>>", self._on_task_tab_changed, add="+")
        if selected_state not in self.task_pages:
            selected_state = "Todas"
        self.task_notebook.select(self.task_pages[selected_state])
        self.selected_state = selected_state

    def _on_task_tab_changed(self, _event=None):
        if self.task_notebook:
            selected_tab = self.task_notebook.select()
            if selected_tab:
                self.selected_state = self.task_notebook.tab(selected_tab, "text")

    def agregar_tarea(self):
        self._open_task_form()

    def _open_task_from_row(self, event, task_table):
        table = task_table.view
        if table.identify_region(event.x, event.y) != "cell":
            return

        iid = table.identify_row(event.y)
        if not iid:
            return

        self._open_task_form(int(iid))
        return "break"

    def _open_task_form(self, task_id=None):
        task = self.controller.get_task(task_id) if task_id is not None else None
        if task_id is not None and task is None:
            self.show_tasks()
            return

        editing = task is not None
        dialog = ttk.Toplevel(title="Editar tarea" if editing else "Agregar tarea")
        dialog.geometry("420x520")
        dialog.minsize(360, 420)
        Utils.center_window(dialog)
        dialog.transient(self.winfo_toplevel())
        if editing:
            dialog.grab_set()

        form = ttk.Labelframe(
            dialog,
            text="Datos de la tarea",
            bootstyle="primary",
            padding=14,
        )
        form.pack(fill="both", expand=True, padx=12, pady=12)

        self.tarea = ttk.StringVar(value=task["tarea"] if editing else "")
        self.prioridad = ttk.StringVar(value=task["prioridad"] if editing else "Media")
        self.estado = ttk.StringVar(value=task["status"] if editing else "Pendiente")

        ttk.Label(form, text="Tarea").pack(anchor="w")
        ttk.Entry(form, textvariable=self.tarea).pack(fill="x", pady=(2, 8))
        ttk.Label(form, text="Fecha límite (YYYY-MM-DD)").pack(anchor="w")
        if editing:
            self.fecha = ttk.StringVar(value=task["fecha"] or "")
            ttk.Entry(form, textvariable=self.fecha).pack(fill="x", pady=(2, 8))
        else:
            self.fecha = ttk.DateEntry(form, date_format="%Y-%m-%d")
            self.fecha.pack(fill="x", pady=(2, 8))
        ttk.Label(form, text="Prioridad").pack(anchor="w")
        ttk.Combobox(
            form,
            textvariable=self.prioridad,
            values=("Alta", "Media", "Baja"),
            state="readonly",
        ).pack(fill="x", pady=(2, 8))

        if editing:
            ttk.Label(form, text="Estado").pack(anchor="w")
            ttk.Combobox(
                form,
                textvariable=self.estado,
                values=("Pendiente", "Completada", "En progreso", "Cancelada"),
                state="readonly",
            ).pack(fill="x", pady=(2, 8))

        ttk.Label(form, text="Descripción").pack(anchor="w")
        self.desc = ttk.Text(form, height=6, wrap="word")
        self.desc.pack(fill="both", expand=True, pady=(2, 10))
        if editing and task["descripcion"]:
            self.desc.insert("1.0", task["descripcion"])

        actions = ttk.Frame(form)
        actions.pack(fill="x")
        if editing:
            ttk.Button(
                actions,
                text="Borrar tarea",
                bootstyle="danger",
                command=lambda: self._delete_task_from_form(dialog, task_id),
            ).pack(side="left")
        ttk.Button(actions, text="Cancelar", command=dialog.destroy).pack(side="right", padx=(8, 0))
        ttk.Button(
            actions,
            text="Guardar cambios" if editing else "Crear tarea",
            bootstyle="primary",
            command=lambda: self._save_task(dialog, task_id),
        ).pack(side="right")

    def _save_task(self, dialog, task_id=None):
        if task_id is None:
            selected_date = self.fecha.get_date()
            fecha = selected_date.strftime("%Y-%m-%d") if selected_date else ""
        else:
            fecha = self.fecha.get().strip()

        task = {
            "tarea": self.tarea.get().strip(),
            "fecha": fecha,
            "prioridad": self.prioridad.get(),
            "descripcion": self.desc.get("1.0", "end-1c").strip(),
            "estado": self.estado.get(),
        }
        if not task["tarea"]:
            Messagebox.show_warning(
                "Escribe el nombre de la tarea.",
                title="Falta la tarea",
                parent=dialog,
            )
            return

        try:
            if task_id is None:
                self.controller.add_task(task)
            else:
                self.controller.update_task(task_id, task)
        except Exception as error:
            Messagebox.show_error(
                str(error), title="No se pudo guardar", parent=dialog
            )
            return

        dialog.destroy()
        self.show_tasks("Pendientes" if task_id is None else task["estado"])

    def _delete_task_from_form(self, dialog, task_id):
        task = self.controller.get_task(task_id)
        if task is None:
            dialog.destroy()
            self.show_tasks(self.selected_state)
            return
        confirmed = Messagebox.okcancel(
            f"¿Eliminar la tarea «{task['tarea']}»?",
            title="Eliminar tarea",
            alert=True,
            parent=self.winfo_toplevel(),
        )
        if confirmed == "OK":
            self.controller.delete_task(task_id)
            dialog.destroy()
            self.show_tasks(self.selected_state)
