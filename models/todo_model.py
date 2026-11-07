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

        columns = "id_task, tarea, fecha, prioridad, descripcion, status"
        tasks = self.db.fetch_all(
            f"SELECT {columns} FROM tasks ORDER BY id_task DESC"
        )
        return header, tasks

    def get_task(self, task_id):
        tasks = self.db.fetch_all(
            "SELECT id_task, tarea, fecha, prioridad, descripcion, status "
            "FROM tasks WHERE id_task = ?",
            (task_id,),
        )
        return tasks[0] if tasks else None

    def delete_task(self, task_id):
        self.db.execute("DELETE FROM tasks WHERE id_task = ?", (task_id,))

    def update_task(self, task_id, updated_task):
        sql = (
            "UPDATE tasks SET tarea = ?, fecha = ?, prioridad = ?, "
            "descripcion = ?, status = ? WHERE id_task = ?"
        )
        params = (
            updated_task["tarea"],
            updated_task["fecha"],
            updated_task["prioridad"],
            updated_task["descripcion"],
            updated_task["estado"],
            task_id,
        )
        self.db.execute(sql, params)

