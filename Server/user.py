'''User class for login'''
from flask_login import UserMixin

class User(UserMixin):
    '''User class'''
    def __init__(self, uid):
        '''Initialize'''
        self._id = uid
        self._name = ''

    def get_name(self):
        '''Return user name'''
        return self._name

    def set_name(self, name):
        '''Set user name'''
        self._name = name

    def __repr__(self):
        '''Return representation of class'''
        return "%d/%s" % (self._id, self._name)

    def get_id(self):
        '''Return user id'''
        return unicode(self._id)
