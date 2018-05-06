__author__ = 'Steve Cassidy'

from bottle import Bottle, template, static_file, request, response, redirect
import interface, re, users

app = Bottle()

@app.route('/')
def index(db):
    """Routes to the index page of the website"""
    info = {
        'title': 'Jobs.',
        'message': 'Welcome <br>to <span class="cyan">Jobs.</span>',
        # Decides whether a 'logged in as {user}' message is shown with a logout button, or a login link is shown if no one is logged in
        'login_name': users.session_user(db),
        # Returns an alphabetically ordered list of the current job locations available, to display next to the search box
        'locations': interface.unique_locations(db),
        # Get positions from the database interface and save in dict
        'positions': interface.position_list(db, 10)
    }

    # Remove HTML tags in 'positions' variable and add them to the desc list
    desc = []
    positions = interface.position_list(db, 10)
    for pos in positions:
        desc.append(re.sub("<.*?>", "", pos[6]))

    # Limit the number of chars in descriptions to 100 as per requirements
    i = 0
    while i < len(desc):
        desc[i][0:100]
        i += 1

    return template('index', info, desc = desc)

@app.route('/static/<filename:path>')
def static(filename):
    """Shows filepath for static file routing"""
    return static_file(filename=filename, root='static')

@app.route('/about')
def about(db):
    """Route for the about page. Returns an HTML template"""
    info = {
        'title' : 'About Jobs.',
        # Decides whether a 'logged in as {user}' message is shown with a logout button, or a login link is shown if no one is logged in
        'login_name': users.session_user(db)
    }
    return template('about', info)


@app.route('/positions/<dd>')
def individual_position(db, dd):
    """Returns an HTML templated page with the individual job posting's information"""
    # get position information from the database
    position = interface.position_get(db, dd)

    # store position information in a dictionary to make it easier to reference in template
    info = {
        'id' : position[0],
        'date': position[1],
        'owner' : position[2],
        'title' : position[3],
        'location' : position[4],
        'company' : position[5],
        'description' : position[6],
        # Decides whether a 'logged in as {user}' message is shown with a logout button, or a login link is shown if no one is logged in
        'login_name': users.session_user(db)
    }

    return template('position', info)


@app.post('/login')
def login(db):
    """ Form handler for login form. Fields submitted are nick and password, which are checked
    for a match with the db. If the login is validated, a session is created and the user is redirected to
    the index page, from which they can add job listings. If login fails, a login failed page is displayed which
    contains a login form
    """
    nick = request.forms.nick
    password = request.forms.password
    print("nick:" + nick)
    print("pw:" + password)

    info = {
        'title': 'Login Failed',
        'login_name': None
    }

    if users.check_login(db, nick, password):
        users.generate_session(db, nick)
        redirect('/', 302)
    else:
        return template('loginfailed', info)


@app.post('/post')
def postjob(db):
    """ Form handler for job postings. Saves all fields to variables to be used in the position_add database interface
    method. If the position wasn't successfully added, an error message is shown and the user is asked to try again.
    If all fields were added, the database adds the new position and redirects back to the homepage, where the
    new position appears.
    """
    title = request.forms.title
    company = request.forms.company
    location = request.forms.location
    description = request.forms.description
    username = users.session_user(db)

    if (not title or not company or not location or not description):
        return 'Error - one or more fields missing. Please <a href="/">go back</a> and try again.'

    if interface.position_add(db, username, title, location, company, description):
        redirect('/', 302) # The HTTP response status code 302 Found is a common way of performing URL redirection.
        return

    return 'Database error. Try again later.'


@app.post('/logout')
def logout(db):
    """Form handler for logout button. Gets the username from the current session and deletes it. Redirects to homepage"""
    username = users.session_user(db)
    users.delete_session(db, username)
    redirect('/', 302)


if __name__ == '__main__':
    from bottle.ext import sqlite
    from database import DATABASE_NAME
    import database

    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True, port=8010)
