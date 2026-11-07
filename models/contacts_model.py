import sqlite3

from models.conector.SQLiteConector import SQLiteConnector


class DuplicateContactError(ValueError):
	pass


class ContactsModel:
	fields = (
		"customer_name",
		"cedula_rif",
		"phone",
		"email",
		"status",
		"segment",
		"main_contact",
		"address",
	)

	def __init__(self, db=None):
		self.db = db or SQLiteConnector()

	def get_contacts(self):
		columns = ", ".join(self.fields)
		return self.db.fetch_all(
			f"SELECT {columns} FROM contacts ORDER BY customer_name COLLATE NOCASE"
		)

	def add_contact(self, contact):
		values = [str(contact.get(field) or "").strip() for field in self.fields]
		if not values[0]:
			raise ValueError("El nombre o la razón social es obligatorio.")

		for field, label in (("email", "correo electrónico"), ("cedula_rif", "cédula / RIF")):
			value = values[self.fields.index(field)]
			if value and self.db.fetch_all(
				f"SELECT 1 FROM contacts WHERE LOWER(TRIM({field})) = LOWER(TRIM(?)) LIMIT 1",
				(value,),
			):
				raise DuplicateContactError(f"Ya existe un contacto con ese {label}.")

		for field in ("email", "cedula_rif"):
			index = self.fields.index(field)
			if not values[index]:
				values[index] = None
		values = tuple(values)

		columns = ", ".join(self.fields)
		placeholders = ", ".join("?" for _ in self.fields)
		try:
			self.db.execute(
				f"INSERT INTO contacts ({columns}) VALUES ({placeholders})",
				values,
			)
		except sqlite3.IntegrityError as error:
			raise DuplicateContactError(
				"El correo electrónico o la cédula / RIF ya está registrado."
			) from error
