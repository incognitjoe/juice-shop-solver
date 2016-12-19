import json

import requests


def get_session(server, email, password, headers=None, oauth=False):
    """
    Log in with given username and password
    :param server: juice shop URL
    :param email: username as string
    :param password: password as string
    :param headers: Optional headers to send with the login request
    :param oauth: boolean. Exclude if False, if True include "oauth: true" in payload
    :return: Session
    """
    payload = {'email': email, 'password': password}
    if oauth:
        payload.update(oauth=True)
    payload = json.dumps(payload)
    return _do_login(server, payload, headers=headers)


def get_admin_session(server):
    """
    Log in legitimately as an admin. Password hash is publicly available, thanks Google.
    :param server: juice shop URL
    :return: Session
    """
    payload = json.dumps({'email': 'admin@juice-sh.op', 'password': 'admin123'})
    return _do_login(server, payload)


def _do_login(server, payload, headers=None):
    """
    Login through the REST API and return a Session with auth header and token in cookie
    :param server: juice shop URL
    :param payload: JSON payload required for auth
    :param headers: optional headers to use for the request. Sets content-type to JSON if omitted.
    :return: Session
    """
    session = requests.Session()
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    login = session.post('{}/rest/user/login'.format(server),
                         headers=headers,
                         data=payload)
    if not login.ok:
        raise RuntimeError('Error logging in. Content: {}'.format(login.content))
    token = login.json().get('token')
    session.cookies.set('token', token)
    session.headers.update({'Authorization': 'Bearer {}'.format(token)})
    return session


def create_user(server, email, password):
    """
    Create new user account through the API.
    :param server: juice shop URL.
    :param email: email address(unvalidated by server!)
    :param password: password
    """
    payload = json.dumps({'email': email, 'password': password, 'passwordRepeat': password})
    session = requests.Session()
    create = session.post('{}/api/Users'.format(server), headers={'Content-Type': 'application/json'}, data=payload)
    if not create.ok:
        raise RuntimeError('Error creating user {}'.format(email))


def whoami(server, session):
    """
    Check current user details
    :param server: juice shop URL
    :param session: Session
    :return: response body as dict
    """
    who = session.get('{}/rest/user/whoami'.format(server), headers={'Accept': 'application/json'})
    if not who.ok:
        raise RuntimeError('Error retrieving current user details')
    return who.json()


def get_current_user_id(server, session):
    """
    Retrieve current user's ID #
    :param server: juice shop URL
    :param session: Session
    :return: ID as int
    """
    return whoami(server, session).get('id')
