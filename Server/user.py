from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, uid):
        self.id = uid
        self.name = ''
   	
   	def get_name(self):
   		return self.name   
   		 
    def set_name(self, name):
    	self.name = name
        
    def __repr__(self):
        return "%d/%s" % (self.id, self.name)

    def get_id(self):
    	return unicode(self.id)
