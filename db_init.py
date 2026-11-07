from models.conector.SQLiteConector import *

class DbInit:
    def __init__(self):
        self.conn = SQLiteConnector()
        self.create_tables()

    def create_tables(self):

        # Crear tabla de tareas si no existe
        tasks = """CREATE TABLE IF NOT EXISTS tasks ( 
            id_task INTEGER PRIMARY KEY AUTOINCREMENT, 
            tarea TEXT, 
            fecha TEXT, 
            prioridad TEXT, 
            descripcion TEXT,
            status TEXT
            ) """

        orders = """CREATE TABLE IF NOT EXISTS orders (
            id_order INTEGER PRIMARY KEY AUTOINCREMENT, 
            order_number TEXT, 
            order_date TEXT,
            order_type TEXT,
            customer_name TEXT, 
            order_status TEXT,
            order_amount REAL )"""

        providers = """CREATE TABLE IF NOT EXISTS providers (
            id_provider INTEGER PRIMARY KEY AUTOINCREMENT, 
            rif_prefix TEXT,
            rif_number TEXT, 
            reason TEXT,
            provider_type TEXT,
            conatct_name TEXT,
            contact_phone TEXT,
            contact_email TEXT,
            state TEXT,
            city TEXT,
            address TEXT)"""

        contacts = """CREATE TABLE IF NOT EXISTS contacts (
            id_contact INTEGER PRIMARY KEY AUTOINCREMENT, 
            customer_name TEXT,
            cedula_rif TEXT UNIQUE,
            phone TEXT,
            email TEXT UNIQUE,
            status TEXT,
            segment TEXT,
            main_contact TEXT,
            address TEXT)"""

        table_list = [tasks, orders, providers, contacts]
        
        for table in table_list:
            self.conn.execute(table)

        self.conn.execute(
            """CREATE UNIQUE INDEX IF NOT EXISTS idx_contacts_email_unique
            ON contacts (LOWER(TRIM(email)))
            WHERE email IS NOT NULL AND TRIM(email) <> ''"""
        )
        self.conn.execute(
            """CREATE UNIQUE INDEX IF NOT EXISTS idx_contacts_cedula_unique
            ON contacts (LOWER(TRIM(cedula_rif)))
            WHERE cedula_rif IS NOT NULL AND TRIM(cedula_rif) <> ''"""
        )
        
