

class TodoModel:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks(self):

        header = ["Tarea", "Fecha Límite", "Prioridad"]
        complete_tasks = [
            ["Revisar correos electrónicos", "2024-06-15", "Alta"],
            ["Preparar informe de ventas", "2024-06-20", "Media"],
            ["Llamar a proveedor", "2024-06-18", "Baja"],
            ["Actualizar base de datos de clientes", "2024-06-22", "Alta"],
            ["Reunión con equipo de marketing", "2024-06-19", "Media"],
            ["Revisar presupuesto del proyecto", "2024-06-21", "Alta"],
            ["Enviar propuesta a cliente potencial", "2024-06-23", "Baja"],
            ["Organizar archivo de documentos", "2024-06-24", "Media"],
            ["Actualizar perfil de LinkedIn", "2024-06-25", "Baja"],
            ["Planificar estrategia de redes sociales", "2024-06-26", "Alta"]
        ]
        pending_tasks = [
            ["Revisar correos electrónicos", "2024-06-15", "Alta"],
            ["Preparar informe de ventas", "2024-06-20", "Media"], 
            ["Llamar a proveedor", "2024-06-18", "Baja"],
            ["Actualizar base de datos de clientes", "2024-06-22", "Alta"],
            ["Reunión con equipo de marketing", "2024-06-19", "Media"],
            ["Revisar presupuesto del proyecto", "2024-06-21", "Alta"],
            ["Enviar propuesta a cliente potencial", "2024-06-23", "Baja"],
            ["Organizar archivo de documentos", "2024-06-24", "Media"],
            ["Actualizar perfil de LinkedIn", "2024-06-25", "Baja"],
            ["Planificar estrategia de redes sociales", "2024-06-26", "Alta"]
        ]

        return header, pending_tasks, complete_tasks