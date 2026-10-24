

class TodoModel:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks(self):

        header = ["Tarea", "Fecha Límite", "Prioridad", "Descripcion"]
        complete_tasks = [
            ["Revisar correos electrónicos", "2024-06-15", "Alta", "Revisar y responder correos electrónicos importantes."],
            ["Preparar informe de ventas", "2024-06-20", "Media", "Preparar informe de ventas del trimestre."],
            ["Llamar a proveedor", "2024-06-18", "Baja", "Llamar al proveedor para confirmar entrega."],
            ["Actualizar base de datos de clientes", "2024-06-22", "Alta", "Actualizar información de clientes en la base de datos."],
            ["Reunión con equipo de marketing", "2024-06-19", "Media", "Reunión para discutir la estrategia de marketing."],
            ["Revisar presupuesto del proyecto", "2024-06-21", "Alta", "Revisar y aprobar el presupuesto del proyecto."],
            ["Enviar propuesta a cliente potencial", "2024-06-23", "Baja", "Enviar propuesta a cliente potencial."],
            ["Organizar archivo de documentos", "2024-06-24", "Media", "Organizar archivo de documentos."],
            ["Actualizar perfil de LinkedIn", "2024-06-25", "Baja", "Actualizar perfil de LinkedIn."],
            ["Planificar estrategia de redes sociales", "2024-06-26", "Alta", "Planificar estrategia de redes sociales."]
        ]
        pending_tasks = [
            ["Revisar correos electrónicos", "2024-06-15", "Alta", "Revisar y responder correos electrónicos importantes."],
            ["Preparar informe de ventas", "2024-06-20", "Media", "Preparar informe de ventas del trimestre."],
            ["Llamar a proveedor", "2024-06-18", "Baja", "Llamar al proveedor para confirmar entrega."],
            ["Reunión con equipo de marketing", "2024-06-19", "Media", "Reunión para discutir la estrategia de marketing."],
            ["Revisar presupuesto del proyecto", "2024-06-21", "Alta", "Revisar y aprobar el presupuesto del proyecto."],
            ["Enviar propuesta a cliente potencial", "2024-06-23", "Baja", "Enviar propuesta a cliente potencial."],
            ["Organizar archivo de documentos", "2024-06-24", "Media", "Organizar archivo de documentos."],
            ["Actualizar perfil de LinkedIn", "2024-06-25", "Baja", "Actualizar perfil de LinkedIn."],
            ["Planificar estrategia de redes sociales", "2024-06-26", "Alta", "Planificar estrategia de redes sociales."]
        ]

        return header, pending_tasks, complete_tasks