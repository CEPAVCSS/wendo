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
		columns = ", ".join(("id_contact",) + self.fields)
		return self.db.fetch_all(
			f"SELECT {columns} FROM contacts ORDER BY customer_name COLLATE NOCASE"
		)

	def get_contact(self, contact_id):
		columns = ", ".join(("id_contact",) + self.fields)
		rows = self.db.fetch_all(
			f"SELECT {columns} FROM contacts WHERE id_contact = ?",
			(contact_id,),
		)
		return rows[0] if rows else None

	def delete_contact(self, contact_id):
		self.db.execute("DELETE FROM contacts WHERE id_contact = ?", (contact_id,))

	def _prepare_values(self, contact, exclude_id=None):
		values = [str(contact.get(field) or "").strip() for field in self.fields]
		if not values[0]:
			raise ValueError("El nombre o la razón social es obligatorio.")

		for field, label in (("email", "correo electrónico"), ("cedula_rif", "cédula / RIF")):
			value = values[self.fields.index(field)]
			if not value:
				continue
			query = (
				f"SELECT 1 FROM contacts "
				f"WHERE LOWER(TRIM({field})) = LOWER(TRIM(?))"
			)
			params = [value]
			if exclude_id is not None:
				query += " AND id_contact <> ?"
				params.append(exclude_id)
			if self.db.fetch_all(query + " LIMIT 1", tuple(params)):
				raise DuplicateContactError(f"Ya existe un contacto con ese {label}.")

		for field in ("email", "cedula_rif"):
			index = self.fields.index(field)
			if not values[index]:
				values[index] = None
		return tuple(values)

	def add_contact(self, contact):
		values = self._prepare_values(contact)
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

	def update_contact(self, contact_id, contact):
		values = self._prepare_values(contact, exclude_id=contact_id)
		assignments = ", ".join(f"{field} = ?" for field in self.fields)
		try:
			self.db.execute(
				f"UPDATE contacts SET {assignments} WHERE id_contact = ?",
				values + (contact_id,),
			)
		except sqlite3.IntegrityError as error:
			raise DuplicateContactError(
				"El correo electrónico o la cédula / RIF ya está registrado."
			) from error
