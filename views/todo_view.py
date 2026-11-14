import ttkbootstrap as ttk
from ttkbootstrap.constants import (
    BOTH,
    CENTER,
    END,
    LEFT,
    RIGHT,
    VERTICAL,
    W,
    X,
    Y,
    YES,
)
from ttkbootstrap.dialogs import Messagebox

from controllers.todo_controller import TodoController
from utils.utils import Utils


class TodoView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.pack(fill=BOTH, expand=YES)
        self.master = master
        self.controller = TodoController(self)
        self.tasks = []
        self.selected_state = "Todas"
        self.search_text = ""
        self.filter_buttons = {}

        self.container = ttk.Frame(self, padding=8)
        self.container.pack(side=LEFT, fill=Y)
        self.App_title = "Tareas"
        ttk.Label(
            self.container,
            text=self.App_title,
            font=("Helvetica", 16, "bold"),
        ).pack(pady=10)
        self.count_label = ttk.Label(
            self.container,
            text="",
            font=("Helvetica", 9),
            bootstyle="secondary",
        )
        self.count_label.pack(pady=(0, 8))

        ttk.Button(
            self.container,
            text="Agregar Tarea Rápida",
            bootstyle="primary",
            command=self.agregar_tarea,
        ).pack(pady=4, fill=X)
        ttk.Button(
            self.container,
            text="Ver Tareas",
            bootstyle="outline-secondary",
            command=self.refresh,
        ).pack(pady=4, fill=X)
        ttk.Button(
            self.container,
            text="Editar Tarea",
            bootstyle="outline-primary",
            command=self._edit_selected_task,
        ).pack(pady=4, fill=X)
        ttk.Button(
            self.container,
            text="Eliminar Tarea",
            bootstyle="outline-danger",
            command=self._delete_selected_task,
        ).pack(pady=4, fill=X)

        self.main_area = ttk.Frame(self, padding=12)
        self.main_area.pack(side=RIGHT, fill=BOTH, expand=YES)

        self.setup_filters()
        self.setup_treeview()
        self.refresh()

    def setup_filters(self):
        filter_frame = ttk.Frame(self.main_area, padding=(0, 0, 0, 10))
        filter_frame.pack(fill=X)

        ttk.Label(
            filter_frame,
            text="FILTROS:",
            font=("Helvetica", 9, "bold"),
            bootstyle="secondary",
        ).pack(side=LEFT, padx=(0, 10))

        states = (
            ("Todas", "Todas"),
            ("Pendiente", "Pendientes"),
            ("En progreso", "En progreso"),
            ("Completada", "Completadas"),
            ("Cancelada", "Canceladas"),
        )
        self.state_labels = dict(states)
        for key, label in states:
            button = ttk.Button(
                filter_frame,
                text=label,
                bootstyle="primary" if key == "Todas" else "secondary-outline",
                command=lambda current=key: self.show_tasks(current),
            )
            button.pack(side=LEFT, padx=2)
            self.filter_buttons[key] = button

        ttk.Label(filter_frame, text="Buscar:", bootstyle="secondary").pack(
            side=RIGHT, padx=(10, 4)
        )
        self.search_var = ttk.StringVar()
        self.search_var.trace_add("write", lambda *_args: self._on_search())
        ttk.Entry(
            filter_frame,
            textvariable=self.search_var,
            bootstyle="light",
            width=24,
        ).pack(side=RIGHT)

    def setup_treeview(self):
        tree_frame = ttk.Frame(self.main_area)
        tree_frame.pack(fill=BOTH, expand=YES)

        columns = ("tarea", "fecha", "prioridad", "descripcion", "estado")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            bootstyle="light",
        )

        headings = {
            "tarea": "TAREA",
            "fecha": "FECHA LÍMITE",
            "prioridad": "PRIORIDAD",
            "descripcion": "DESCRIPCIÓN",
            "estado": "ESTADO",
        }
        for column, text in headings.items():
            self.tree.heading(column, text=text)

        widths = {
            "tarea": (220, W),
            "fecha": (120, CENTER),
            "prioridad": (100, CENTER),
            "descripcion": (300, W),
            "estado": (120, CENTER),
        }
        for column, (width, anchor) in widths.items():
            self.tree.column(column, width=width, anchor=anchor)

        self.tree.tag_configure("pendiente", background="#FFF3CD", foreground="#664D03")
        self.tree.tag_configure("en progreso", background="#CFE2FF", foreground="#084298")
        self.tree.tag_configure("completada", background="#D1E7DD", foreground="#0F5132")
        self.tree.tag_configure("cancelada", background="#F8D7DA", foreground="#842029")

        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tree.bind("<Double-1>", self._open_task_from_row)

    def refresh(self):
        self.show_tasks(self.selected_state)

    def show_tasks(self, selected_state=None):
        if selected_state is None:
            selected_state = self.selected_state
        self.selected_state = selected_state

        self.tasks = self.controller.get_tasks()[1]
        self._update_filter_buttons()

        for key, button in self.filter_buttons.items():
            button.configure(
                bootstyle="primary" if key == selected_state else "secondary-outline"
            )

        self._populate_tree()

    def _update_filter_buttons(self):
        counts = {"Todas": len(self.tasks)}
        for task in self.tasks:
            status = task["status"] or "Pendiente"
            counts[status] = counts.get(status, 0) + 1
        for key, button in self.filter_buttons.items():
            button.configure(text=f"{self.state_labels[key]} ({counts.get(key, 0)})")
        self.count_label.configure(text=f"{len(self.tasks)} tarea(s) registrada(s)")

    def _on_search(self):
        self.search_text = self.search_var.get().strip().lower()
        self._populate_tree()

    def _populate_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for task in self.tasks:
            status = task["status"] or "Pendiente"
            if self.selected_state != "Todas" and status != self.selected_state:
                continue
            searchable = f"{task['tarea'] or ''} {task['descripcion'] or ''}".lower()
            if self.search_text and self.search_text not in searchable:
                continue

            values = (
                task["tarea"] or "",
                task["fecha"] or "",
                task["prioridad"] or "",
                task["descripcion"] or "",
                status,
            )
            self.tree.insert(
                "",
                END,
                iid=str(task["id_task"]),
                values=values,
                tags=(status.lower(),),
            )

    def _selected_task_id(self):
        selection = self.tree.selection()
        if not selection:
            Messagebox.show_warning(
                "Selecciona una tarea de la tabla.",
                title="Sin selección",
                parent=self,
            )
            return None
        return int(selection[0])

    def _edit_selected_task(self):
        task_id = self._selected_task_id()
        if task_id is not None:
            self._open_task_form(task_id)

    def _delete_selected_task(self):
        task_id = self._selected_task_id()
        if task_id is None:
            return
        self._confirm_delete_task(task_id)

    def agregar_tarea(self):
        self._open_task_form()

    def _open_task_from_row(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        iid = self.tree.identify_row(event.y)
        if not iid:
            return
        self._open_task_form(int(iid))

    def _open_task_form(self, task_id=None):
        task = self.controller.get_task(task_id) if task_id is not None else None
        if task_id is not None and task is None:
            self.refresh()
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
        ttk.Button(actions, text="Cancelar", command=dialog.destroy).pack(
            side="right", padx=(8, 0)
        )
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
        self.show_tasks("Pendiente" if task_id is None else task["estado"])

    def _delete_task_from_form(self, dialog, task_id):
        if self._confirm_delete_task(task_id):
            dialog.destroy()

    def _confirm_delete_task(self, task_id):
        task = self.controller.get_task(task_id)
        if task is None:
            self.refresh()
            return False
        confirmed = Messagebox.okcancel(
            f"¿Eliminar la tarea «{task['tarea']}»?",
            title="Eliminar tarea",
            alert=True,
            parent=self.winfo_toplevel(),
        )
        if confirmed != "OK":
            return False
        try:
            self.controller.delete_task(task_id)
        except Exception as error:
            Messagebox.show_error(str(error), title="No se pudo eliminar", parent=self)
            return False
        self.refresh()
        return True
