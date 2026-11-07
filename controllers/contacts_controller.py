from models.contacts_model import ContactsModel


class ContactsController:
	def __init__(self, model=None):
		self.model = model or ContactsModel()

	def get_contacts(self):
		return self.model.get_contacts()

	def add_contact(self, contact):
		self.model.add_contact(contact)
