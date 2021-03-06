from flask import Flask, render_template, request, Response, redirect, url_for
from redisDB import *
from functools import wraps
from flask_mail import Mail, Message
from emailForm import emailForm
from flask_wtf.csrf import CsrfProtect
import flask
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)

#Initialize our global variables. Mail needs to be global so it's here, but
#no need to initialize it twice, and it has to be initialized after setting
#its config in the main method.
theDatabase = RedisDB()
mail = None 
mapType = "NormalMap"

# These next three functions can be used to password-protect pages.
# Simply put an @requires_auth immediately above the def function() line.


def check_auth(username, password):
    return username == 'expospring2014' and password == 'haveaniceday'


def authenticate():
    return Response(
        'Your username or password was wrong.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

#Here's our main page. In a standard GET, we just return the page.
#POST is here because our email contact form, inherited by all pages, 
#works by POSTing to the main page. 
@app.route('/', methods=['GET', 'POST'])
def index():
    theEmailForm = emailForm(request.form)
    if(request.method == 'POST'):
        msg = Message(
            'expo.gatech.edu Contact Form', recipients=['capstone@gatech.edu'])
        msg.add_recipient("davidgsharpe7@gmail.com")
        msg.body = "Name: " + theEmailForm.name.data + "\n Email:" + \
            theEmailForm.email.data + "\n\n" + theEmailForm.message.data
        mail.send(msg)
    return render_template('index.html', pageName="Index", emailForm=emailForm(), semester = theDatabase.getCurrentSemester())
    
#This looks at the submission number parameter passed in the URL, and
#retrieves that entry from the database. It then passes that entry's information
#to the projectdetails page.
@app.route('/projectdetails/<submissionNum>')
def projectdetails(submissionNum):
    return render_template('projectdetails.html', submission=theDatabase.getOneSubmission(submissionNum), pageName="Project Details", emailForm=emailForm()) 

@app.route('/schedule')
def schedule():
    return render_template('schedule.html', schedule=theDatabase.getSchedule(), busSchedule=theDatabase.getBusSchedule(), schEnd=theDatabase.getSchEnd(), pageName="Spring 2014 Expo Schedule", emailForm=emailForm())


@app.route('/social')
def social():
    return render_template('social.html', pageName="Social", emailForm=emailForm())

#Will either load the rain map or normal map depending on the request arguments.
@app.route('/map')
def map():
    if (request.method=='GET'):
        if request.args.get('rainMap'):
            return theDatabse.getMapCanvas("rainMap")
        elif request.args.get("normalMap"):
            return theDatabase.getMapCanvas("normalMap")
    return render_template('map.html', pageName="Expo Map", emailForm=emailForm(), mapType=theDatabase.getMapType())


@app.route('/projects')
def projects():
    return redirect(url_for('projects') + "/" + theDatabase.getCurrentSemester())

#Loads the project for a specified semester and loads the favorites, if any, for the semester.
@app.route('/projects/<semester>')
def projectsSem(semester):
    cooks = request.cookies.get("favs")
    if cooks is not None:
        favUCooks = cooks.split(",")
        favCooks = []
        for a in favUCooks:
            favCooks.append(str(a))

        return render_template('projects.html', favs = favCooks, entries=theDatabase.getAllEntriesWithSubmissionNums(semester), pageName="Projects", emailForm=emailForm())
    return render_template('projects.html', favs = [], entries=theDatabase.getAllEntriesWithSubmissionNums(semester), pageName="Projects", emailForm=emailForm())

@app.route('/seeliogallery')
def seeliogallery():
    return redirect(url_for('seeliogallery') + "/" + theDatabase.getCurrentSemester())

@app.route('/seeliogallery/<semester>')
def seeliogallerySem(semester):
    return render_template('seeliogallery.html', pageName="Seelio", emailForm=emailForm(), sKey=theDatabase.getCurrentSeelioKey(semester))

@app.route('/tips')
def tips():
    return render_template('tips.html', vTips = theDatabase.getAllVTips(),sTips = theDatabase.getAllSTips(), jTips = theDatabase.getAllJTips(), pageName="Tips", emailForm=emailForm())
    
#This takes the search string passed in the URL, uses that to search
#the database, and then passes the results to projects.html the same
#way that /projects does. 
@app.route('/search/<searchString>')
def search(searchString):
    return render_template('projects.html', entries=theDatabase.search(searchString), pageName="Search Results", searchTitle="Search Results for: " + "\""+searchString +"\"", emailForm=emailForm())


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME='teamdroptables@gmail.com',
        MAIL_PASSWORD='correcthorsebatterystaple',
        MAIL_DEFAULT_SENDER='teamdroptables@gmail.com'
    )
    mail = Mail(app)
    app.run(debug=True, host='0.0.0.0', port=5002)
