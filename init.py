from datetime import datetime
import webapp2
from models.classes import *


class MainPage(webapp2.RequestHandler):
    def get(self):
        Group(
            id='anonymous',
            book_view=True
        ).put()

        Group(
            id='admin',
            book_view=True,
            book_edit=True,
            book_borrow=True
        ).put()

        Group(
            id='pending',
            book_view=True
        ).put()

        Group(
            id='user',
            book_view=True,
            book_borrow=True
        ).put()

        Extra(
            id='last_init',
            value=str(datetime.now())
        ).put()

        self.response.write('complete.')

APPLICATION = webapp2.WSGIApplication([
    ('.*', MainPage)
])
