import connexion
import os
import urllib2, urllib

import flask

from models.classes import *

github_secret = 'GITHUB_SECRET'
github_client = 'GITHUB_CLIENT'


def get_param_from_query(query, target):
    for p in query.split('&'):
        if 0 <= p.find('=') < len(p) - 1:
            p_key, p_value = p.split('=')

            if p_key.lower() == target.lower():
                return p_value

    return None


def get_user_from_key(api_key):
    key_entity = ndb.Key(ApiKey, api_key).get()

    if not key_entity:
        return None

    return key_entity.user.get()


def get_current_user():
    api_key = get_param_from_query(connexion.request.query_string, 'api_key')

    return get_user_from_key(api_key)


def current_user():
    user = get_current_user()

    if not user:
        return flask.Response(status=401)

    return user.to_obj()


def selected_user(user_id):
    if not user_id:
        return flask.Response(status=404)

    user_entity = ndb.Key(User, user_id.lower()).get()

    if user_entity:
        return user_entity.to_obj()
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
                             'rawUrl': raw_url,
                             'clientKeyParameter': client_key_parameter,
                             'clientKey': client_key,
                             'scopeParameter': scope_parameter,
                             'scope': scope,
                             'fullUrl': '{}?{}={}&{}={}'.format(raw_url, client_key_parameter, client_key,
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
                    new_key = ApiKey(id=ApiKey.get_new_key())
                    new_user = User(id=User.get_new_key())

                    new_user.api_key = new_key.key
                    new_user.email = user_email.key
                    new_key.user = new_user.key
                    user_email.user = new_user.key

                    new_user.put()
                    new_key.put()
                    user_email.put()

                return {'apiKey': user_email.user.get().api_key.id()}

        return 'not valid token'
    else:
        return 'not supported'


def book_get(limit):
    return 'book get response!'


def book_isbn_get(isbn):
    return 'book isbn get response!'


def book_isbn_put(isbn, book):
    return 'book put response!'


def book_isbn_post(isbn, book):
    return 'book post response!'
