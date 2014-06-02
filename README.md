THE QUICK AND DIRTY GUIDE TO DEPLOYING OUR FORM AND SITE

This guide assumes you're on Linux. If you're not, you may be able to do the same thing with homebrew packages on OS X or with various...whatevers on Windows. But seriously, use Linux.

1. Install REDIS and get it running according to the instructions on this page: http://redis.io/topics/quickstart (don't change the default port of 6379)
2. Set up a python virtual environment which contains flask, flask-wtf, flask-mail, and redis:
    sudo pip install virtualenv

    virtualenv flaskapp

    cd flaskapp

    . bin/activate

    pip install Flask flask-wtf flask-mail redis

3. Clone this repo, rename its folder to "app", and move it inside /flaskapp.
4. With your virtualenv activated (cd into /flaskapp and then type ". bin/activate", which should cause you to see (flaskapp) in front of your terminal line), run "screen python app/form/routes.py".
5. Disconnect from the screen by pressing Control+A, then pressing D. Run the site the same way - "screen python app/website/routes.py", then disconnect from that screen the same way. Repeat with "screen python app/admin/routes.py".
6. Navigate to localhost:5001 if you're running the form, localhost:5002 for the website, localhost:5003 for the admin page, and have fun. You can use redis-cli to check out the entries the form is creating in the database.

See Documentation/Developer Manual.txt for more detailed explanations of how this app is written.
 .
