from .conector.SQLiteConector import *

class TodoModel:
    """
        Agregar la tarea a la base de datos
        Estados de las Tareas: Pendiente, Completada, En progreso, Cancelada  
        Metodos disponibles:
        - add_task: Agrega una nueva tarea a la base de datos
        - get_tasks: Obtiene todas las tareas de la base de datos, separadas por estado (pendientes y completadas)
        - delete_task: Elimina una tarea de la base de datos
        - update_task: Actualiza una tarea en la base de datos 
    """
    def __init__(self):
        self.tasks = []
        self.db = SQLiteConnector()


    def add_task(self, task):

        sql = "INSERT INTO tasks (tarea, fecha, prioridad, descripcion, status) VALUES (?, ?, ?, ?, ?)"
        params = (task["tarea"], task["fecha"], task["prioridad"], task["descripcion"], "Pendiente")
        self.db.execute(sql, params)

    def get_tasks(self):

        header = ["Tarea", "Fecha Límite", "Prioridad", "Descripcion", "Estado"]

        columns = "tarea, fecha, prioridad, descripcion, status"
        complete_tasks = self.db.fetch_all(
            f"SELECT {columns} FROM tasks WHERE status = ?",
            ("Completada",),
        )
        pending_tasks = self.db.fetch_all(
            f"SELECT {columns} FROM tasks WHERE status = ?",
            ("Pendiente",),
        )

        return header, pending_tasks, complete_tasks

    def delete_task(self, task_id):
        sql = "DELETE FROM tasks WHERE id = ?"
        params = (task_id,)
        self.db.execute(sql, params)

    def update_task(self, task_id, updated_task):
        sql = "UPDATE tasks SET title = ?, due_date = ?, priority = ?, description = ?, status = ? WHERE id = ?"
        params = (updated_task["tarea"], updated_task["fecha"], updated_task["prioridad"], updated_task["descripcion"], updated_task["estado"], task_id)
        self.db.execute(sql, params)

