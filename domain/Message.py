

class Message:
	
	def __init__(self, message, contact_id=None, first_name=None, last_name=None):
		self.message = message
		self.contact_id = contact_id
		self.first_name = first_name
		self.last_name = last_name