[View Live Site](https://emmawalkerjobsversion1.herokuapp.com/)

# JobSearchApplication
This application is modelled around other job-search web apps such as seek. 

Users can log in to post jobs, which are stored in the db and dynamically displayed on the front page. 

# /views
Contains the templates for the application.
views/base.html is the header/footer that the other templates inherit from. 
views/index.html is the template for the front page.
All others fairly self-explanatory.

# database.py
Contains all the main database methods. Interface.py contains functional db methods.

# main.py
The main application module. Contains routes for the application.

# /static
Contains static files such as style.css and image files.
