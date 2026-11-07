from models.todo_model import TodoModel

class TodoController:
    def __init__(self, container):
        self.view = container
        self.model = TodoModel()

    def get_tasks(self):
        return self.model.get_tasks()


    


