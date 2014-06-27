from flask import Flask, render_template, request, Response, redirect
from redisDB import *
from functools import wraps
from flask_mail import Mail, Message
from emailForm import emailForm
from flask_wtf.csrf import CsrfProtect
import flask
import sys
import os
import shutil
reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)

#Initialize our global variables. Mail needs to be global so it's here, but
#no need to initialize it twice, and it has to be initialized after setting
#its config in the main method.
theDatabase = RedisDB()
theDatabase.init()
mail = None 

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
    return render_template('index.html', pageName="Index", emailForm=emailForm())

#This looks at the submission number parameter passed in the URL, and
#retrieves that entry from the database. It then passes that entry's information
#to the projectdetails page.
@app.route('/projectdetails/<submissionNum>')
def projectdetails(submissionNum):
    return render_template('projectdetails.html', submission=theDatabase.getOneSubmission(submissionNum), pageName="Project Details", emailForm=emailForm())


@app.route('/schedule', methods=['GET','POST'])
def schedule():
    if(request.method=='POST'):
        if(request.form['type']=="Sch"):
            theDatabase.editSchedule(request.form['editSchTip'])
        elif(request.form['type']=="busSch"):
            theDatabase.editBusSchedule(request.form['editBusSchTip'])
        elif(request.form['type']=="endSch"):
            theDatabase.editSchEnd(request.form['editEndSchTip'])
    return render_template('schedule.html', schedule=theDatabase.getSchedule(), busSchedule=theDatabase.getBusSchedule(), schEnd=theDatabase.getSchEnd(), pageName="Spring 2014 Expo Schedule", emailForm=emailForm())


@app.route('/social')
def social():
    return render_template('social.html', pageName="Social", emailForm=emailForm())


@app.route('/map')
def map():
    return render_template('map.html', pageName="Expo Map", emailForm=emailForm())

@app.route('/projects')
def projects():
    return render_template('projects.html', entries=theDatabase.getAllEntriesWithSubmissionNums(), pageName="Projects", emailForm=emailForm())


@app.route('/semesters')
def semesters():
    return render_template('semesters.html', pageName="Semesters", emailForm=emailForm(), entries=theDatabase.getAllSemesters(), currentSemester = theDatabase.getCurrentSemester())

@app.route('/semesters/<newSemester>/<newKey>')
def addsemesterWithKey(newSemester, newKey):
	theDatabase.setCurrentSemester(newSemester)
	theDatabase.setCurrentSeelioKey(newKey, newSemester)
	return redirect(flask.url_for('semesters'))
	
@app.route('/semesters/<newSemester>')
def addSemester(newSemester):
    theDatabase.setCurrentSemester(newSemester)
    return redirect(flask.url_for('semesters'))
	
@app.route('/semesters/delete/<semester>')
def removeSemester(semester):
    theDatabase.removeSemester(semester)        
    return redirect(flask.url_for('semesters'))

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if(request.method=='POST'):
	if(request.form['type']=="J"):
	        theDatabase.addJudTip(request.form['newTip'])
	elif(request.form['type']=="V"):
		theDatabase.addVisTip(request.form['newTip'])
	elif(request.form['type']=="S"):
		theDatabase.addStuTip(request.form['newTip'])
	elif(request.form['type']=="VE"):
		theDatabase.editVTip(request.form['editVTip'],request.form['vKey'])
	elif(request.form['type']=="SE"):
		theDatabase.editSTip(request.form['editSTip'],request.form['sKey'])
	elif(request.form['type']=="JE"):
		theDatabase.editJTip(request.form['editJTip'],request.form['jKey'])
	elif(request.form['type']=="JD"):
		theDatabase.delJTip(request.form['jKey'])
	elif(request.form['type']=="SD"):
		theDatabase.delSTip(request.form['sKey'])
	elif(request.form['type']=="VD"):
		theDatabase.delVTip(request.form['vKey'])
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
    app.run(debug=True, host='0.0.0.0', port=5003)
