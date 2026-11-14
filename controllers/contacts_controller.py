from models.contacts_model import ContactsModel


class ContactsController:
	def __init__(self, model=None):
		self.model = model or ContactsModel()

	def get_contacts(self):
		return self.model.get_contacts()

	def get_contact(self, contact_id):
		return self.model.get_contact(contact_id)

	def add_contact(self, contact):
		self.model.add_contact(contact)

	def update_contact(self, contact_id, contact):
		self.model.update_contact(contact_id, contact)

	def delete_contact(self, contact_id):
		self.model.delete_contact(contact_id)
