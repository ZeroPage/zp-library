import random, string, json
from google.appengine.ext import ndb


class ApiKey(ndb.Model):
    key_length = 20

    user = ndb.KeyProperty(kind='User', required=True)


class Group(ndb.Model):
    book_view = ndb.BooleanProperty(default=False, indexed=False)
    book_edit = ndb.BooleanProperty(default=False, indexed=False)
    book_borrow = ndb.BooleanProperty(default=False, indexed=False)


class UserEmail(ndb.Model):
    user = ndb.KeyProperty(kind='User', required=True)


class User(ndb.Model):
    key_length = 6

    api_key = ndb.KeyProperty(ApiKey, required=True)
    email = ndb.KeyProperty(UserEmail, required=True)
    group = ndb.KeyProperty(Group, default=ndb.Key(Group, 'pending'))
    name = ndb.StringProperty(default='no name')


class Extra(ndb.Model):
    value = ndb.GenericProperty(indexed=False)


class BookExtra(ndb.Model):
    image_large = ndb.StringProperty()
    image_small = ndb.StringProperty()
    quantity = ndb.IntegerProperty()
    memo = ndb.StringProperty()


class BookAutomated(ndb.Model):
    updated_date = ndb.DateTimeProperty(auto_now=True)
    added_date = ndb.DateTimeProperty(auto_now_add=True)


class Book(ndb.Model):
    key_length = 6

    title = ndb.StringProperty(required=True)
    subTitle = ndb.StringProperty()
    content_version = ndb.StringProperty()
    authors = ndb.StringProperty(repeated=True)
    translators = ndb.StringProperty(repeated=True)
    publisher = ndb.StringProperty()
    published_date = ndb.DateProperty()
    description = ndb.StringProperty()
    page_count = ndb.IntegerProperty()
    language = ndb.StringProperty()

    extra = ndb.StructuredProperty(BookExtra, required=True)
    automated = ndb.StructuredProperty(BookAutomated, required=True)


def generate_key(model):
    while True:
        temp_key = ''.join(generate_char() for _ in range(model.key_length))

        if not ndb.Key(model, temp_key).get():
            return temp_key


def generate_char():
    return random.SystemRandom().choice(string.ascii_lowercase + string.digits)
