"""
Database Model interface for the COMP249 Web Application assignment

@author: Emma Walker
"""

def unique_locations(db):
    """Returns a list of the unique locations in the database"""
    cur = db.cursor()

    sql = """SELECT DISTINCT location FROM positions ORDER BY LOWER(location)"""

    cur.execute(sql)

    result = cur.fetchall()

    list = [row[0] for row in result]

    return list


def position_list(db, limit=10):
    """Return a list of positions ordered by date
    db is a database connection
    return at most limit positions (default 10)

    Returns a list of tuples  (id, timestamp, owner, title, location, company, description)
    """
    cur = db.cursor()
    sql = """SELECT id, timestamp, owner, title, location, company, SUBSTR(description, 0, 150)
    FROM positions 
    ORDER BY timestamp desc
    LIMIT (?);
    """
    cur.execute(sql, (limit ,))
    results = cur.fetchall()

    pos_list = [row for row in results]

    return pos_list

def position_get(db, id):
    """Return the details of the position with the given id
    or None if there is no position with this id

    Returns a tuple (id, timestamp, owner, title, location, company, description)

    """
    cur = db.cursor()
    posList = []

    # Check if the ID matches an ID in the database
    sql = """SELECT count(id) FROM positions WHERE id=?"""
    cur.execute(sql, (id ,))
    data = cur.fetchone()[0]
    # If no match found, return None
    if data == 0:
        return None

    # Otherwise, ID was matched --> return position details
    sql = """SELECT id, timestamp, owner, title, location, company, description
    FROM positions WHERE id=?
    """

    cur.execute(sql, (id, ))
    c = cur.fetchone()

    pos_get = [row for row in c]

    return pos_get


def position_add(db, usernick, title, location, company, description):
    """Add a new post to the database.
    The date of the post will be the current time and date.
    Only add the record if usernick matches an existing user

    Return True if the record was added, False if not."""

    cur = db.cursor()

    # Check if usernick matches an existing user - if it doesn't, immediately return False
    sql = """SELECT count(nick) FROM users WHERE nick=?"""
    cur.execute(sql, (usernick ,))
    count = cur.fetchone()[0]
    if count == 0:
        return False

    # If we've got this far, we've counted at least one usernick match. Now insert new position.
    sql = """INSERT INTO positions (owner, title, location, company, description) VALUES (?, ?, ?, ?, ?)"""
    cur.execute(sql, (usernick, title, location, company, description))

    db.commit()

    return True




