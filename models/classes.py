import random, string, json
from google.appengine.ext import ndb


class ApiKey(ndb.Model):
    user = ndb.KeyProperty(kind='User', required=True)

    @staticmethod
    def get_new_key():
        while True:
            temp_key = generate_key(20)
            if not ndb.Key(ApiKey, temp_key).get():
                return temp_key


class Group(ndb.Model):
    book_view = ndb.BooleanProperty(default=False, indexed=False)
    book_edit = ndb.BooleanProperty(default=False, indexed=False)
    book_borrow = ndb.BooleanProperty(default=False, indexed=False)


class UserEmail(ndb.Model):
    user = ndb.KeyProperty(kind='User', required=True)


class User(ndb.Model):
    api_key = ndb.KeyProperty(ApiKey, required=True)
    email = ndb.KeyProperty(UserEmail, required=True)
    group = ndb.KeyProperty(Group, default=ndb.Key(Group, 'pending'))
    name = ndb.StringProperty(default='no name')

    @staticmethod
    def get_new_key():
        while True:
            temp_key = generate_key(6)
            if not ndb.Key(ApiKey, temp_key).get():
                return temp_key


class Extra(ndb.Model):
    value = ndb.GenericProperty(indexed=False)


class Book(ndb.Model):
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
    image_small = ndb.StringProperty()
    image_large = ndb.StringProperty()
    added_date = ndb.DateTimeProperty()
    updated_date = ndb.DateTimeProperty()
    quantity = ndb.IntegerProperty()
    memo = ndb.StringProperty


def generate_key(key_length):
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(key_length))
