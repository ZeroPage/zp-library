import utils
import os
import urllib2, urllib

import flask

from models.classes import *

github_secret = 'GITHUB_SECRET'
github_client = 'GITHUB_CLIENT'


def current_user():
    user = utils.get_current_user()

    if not user:
        return flask.Response(status=401)

    return {
        'email': user.email.id() if user.email else '',
        'group': user.group.id()
    }


def selected_user(user_id):
    if not user_id:
        return flask.Response(status=404)

    user_entity = ndb.Key(User, user_id.lower()).get()

    if user_entity:
        return user_entity.to_dict()
    else:
        return flask.Response(status=404)


def auth_source():
    auth_methods = []

    if os.getenv(github_secret) and os.getenv(github_client):
        raw_url = 'https://github.com/login/oauth/authorize'
        client_key_parameter = 'client_id'
        client_key = os.getenv('GITHUB_CLIENT')
        scope_parameter = 'scope'
        scope = 'user:email'

        auth_methods.append({'source': 'github',
                             'raw_url': raw_url,
                             'client_key_parameter': client_key_parameter,
                             'client_key': client_key,
                             'scope_parameter': scope_parameter,
                             'scope': scope,
                             'full_url': '{}?{}={}&{}={}'.format(raw_url, client_key_parameter, client_key,
                                                                 scope_parameter, scope)})

    return auth_methods


def auth_key(source, token):
    if source == 'github':
        url = 'https://github.com/login/oauth/access_token?client_id={}&client_secret={}&code={}'.format(
                os.getenv(github_client), os.getenv(github_secret), token
        )
        values = {}
        data = urllib.urlencode(values)

        req = urllib2.Request(url, data)
        res = urllib2.urlopen(req)
        res_data = res.read()

        for p in res_data.split('&'):
            p_key, p_value = p.split('=')

            if p_key == 'access_token':
                email_req = urllib2.Request('https://api.github.com/user/emails?access_token={}'.format(p_value))
                email_res = urllib2.urlopen(email_req)

                emails = json.loads(email_res.read())

                primary_email = ''
                for email in emails:
                    if email['primary']:
                        primary_email = email['email'].lower()

                user_email = ndb.Key(UserEmail, primary_email).get()

                if not user_email:
                    user_email = UserEmail(id=primary_email)
                    new_key = ApiKey(id=generate_key(ApiKey))
                    new_user = User(id=generate_key(User))

                    new_user.api_key = new_key.key
                    new_user.email = user_email.key
                    new_key.user = new_user.key
                    user_email.user = new_user.key

                    new_user.put()
                    new_key.put()
                    user_email.put()

                return {'api_key': user_email.user.get().api_key.id()}

        return 'not valid token'
    else:
        return 'not supported'


def book_get(limit):
    current_group = utils.get_current_group()

    if not current_group.book_view:
        return flask.Response(status=403, response='no permission')

    books = Book.query().order(-Book.automated.added_date).fetch(limit)

    results = [{book.key.id(): book.to_dict()} for book in books]

    return results


def book_id_get(id):
    current_group = utils.get_current_group()

    if not current_group.book_view:
        return flask.Response(status=403, response='no permission')

    selected_book = ndb.Key(Book, id.lower()).get()

    if selected_book:
        return {selected_book.key.id(): selected_book.to_dict()}
    else:
        return flask.Response(status=404, response='not found')


def book_id_put(id, book):
    return 'book put response!'


def book_id_post(id, book):
    current_group = utils.get_current_group()

    if not current_group.book_edit:
        return flask.Response(status=403, response='no permission')

    if not (len(id) == 13 and id.isdigit()):
        return flask.Response(status=400, response='id must be 13 digits integer')

    if isinstance(book_id_get(id), dict):
        return flask.Response(status=400, response='already exists')

    del book['automated']
    new_book = Book(id=id, **book)
    new_book.automated = BookAutomated()

    new_book.put()

    return {id: new_book.to_dict()}
