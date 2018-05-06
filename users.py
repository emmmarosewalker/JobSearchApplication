"""
Created on Mar 26, 2012

@author: steve
"""

from database import password_hash
from bottle import response, request
import uuid

# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'


def check_login(db, usernick, password):
    """returns True if password matches stored"""

    cur = db.cursor()

    sql = """SELECT COUNT(nick) FROM users WHERE nick=? AND password=?"""

    cur.execute(sql, (usernick, password_hash(password)))

    count = cur.fetchone()[0]

    if count > 0:
        return True

    return False

def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """
    cur = db.cursor()
    # First check for active sessions
    sql = """SELECT COUNT(sessionid), sessionid FROM sessions WHERE usernick=?"""
    cur.execute(sql, (usernick ,))

    result = cur.fetchone()
    count = result[0]

    if count > 0:
        session = result[1]
        return session

    # No existing session found, so we should create one
    # First check that user is a valid user
    sql = """SELECT COUNT(nick) FROM users WHERE nick=?"""
    cur.execute(sql, (usernick, ))

    count = cur.fetchone()[0]
    if count == 0:
        return None

    # Valid user nick found in users but no session id found in sessions. Create a new session id for the user.
    sql = """INSERT INTO sessions (sessionid, usernick) VALUES(?, ?)"""
    key = str(uuid.uuid4())
    cur.execute(sql, (key, usernick))

    db.commit()

    response.set_cookie(COOKIE_NAME, key)

    return key


def delete_session(db, usernick):
    """remove all session table entries for this user"""
    cur = db.cursor()

    sql = """DELETE FROM sessions WHERE usernick=?"""
    cur.execute(sql, (usernick ,))

    db.commit()


def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""

    session_cookie = request.get_cookie(COOKIE_NAME)

    cur = db.cursor()

    sql = """SELECT COUNT(usernick), usernick FROM SESSIONS where sessionid=?"""

    cur.execute(sql, (session_cookie ,))

    result = cur.fetchone()
    count = result[0]
    if count > 0: # a user session has been found
        usernick = result[1]
        return usernick

    # Else no session found so no name returned.
    return None


