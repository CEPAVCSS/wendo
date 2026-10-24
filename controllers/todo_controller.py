from models.todo_model import TodoModel

class TodoController:
    def __init__(self, container):
        self.view = container
        self.model = TodoModel()
        self.tasks = self.model.get_tasks()


