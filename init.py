from datetime import datetime
import webapp2
from models.classes import *

INIT_GROUP_ADMIN = 'admin'
INIT_GROUP_USER = 'user'
INIT_GROUP_PENDING = 'pending'
INIT_GROUP_ANONYMOUS = 'anonymous'

INIT_EXTRA_LAST_INIT = 'last_init'


class MainPage(webapp2.RequestHandler):
    def get(self):
        Group(
            id=INIT_GROUP_ANONYMOUS,
            book_view=True
        ).put()

        Group(
            id=INIT_GROUP_ADMIN,
            book_view=True,
            book_edit=True,
            book_borrow=True
        ).put()

        Group(
            id=INIT_GROUP_PENDING,
            book_view=True
        ).put()

        Group(
            id=INIT_GROUP_USER,
            book_view=True,
            book_borrow=True
        ).put()

        Extra(
            id=INIT_EXTRA_LAST_INIT,
            value=str(datetime.now())
        ).put()

        self.response.write('complete.')

APPLICATION = webapp2.WSGIApplication([
    ('.*', MainPage)
])
