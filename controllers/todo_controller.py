from models.todo_model import TodoModel

class TodoController:
    def __init__(self, container):
        self.view = container
        self.model = TodoModel()

    def get_tasks(self):
        return self.model.get_tasks()

    def get_task(self, task_id):
        return self.model.get_task(task_id)

    def add_task(self, task):
        self.model.add_task(task)

    def update_task(self, task_id, task):
        current_task = self.model.get_task(task_id)
        if current_task is None:
            raise ValueError("No se encontró la tarea que intentas actualizar.")

        current_status = current_task["status"]
        if current_status in ("Completada", "Cancelada") and task["estado"] != current_status:
            raise ValueError(
                f"No se puede cambiar el estado de una tarea {current_status.lower()}."
            )

        self.model.update_task(task_id, task)

    def delete_task(self, task_id):
        self.model.delete_task(task_id)





