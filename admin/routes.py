from flask import Flask, render_template, request, Response, redirect, url_for, make_response
from werkzeug.utils import secure_filename
from redisDB import *
from functools import wraps
from flask_mail import Mail, Message
from emailForm import emailForm
from flask_wtf.csrf import CsrfProtect
import flask
import sys
import os
import shutil
import csv
import StringIO
import string
from flask_wtf.csrf import CsrfProtect
reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/data')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        if(request.form['type']=="img"):
            files=request.files['file']
            filename = secure_filename(files.filename)
            files.save(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'static/img'),'GT_logo.png'))
            src = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'static/img'),'GT_logo.png')
            dst = os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'website/static/img'),'GT_logo.png')
            shutil.copyfile(src,dst)
#the previous line will need to be calibrated on deploy
        else:
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
    return render_template('map.html', pageName="Expo Map", emailForm=emailForm(), rainSerialized=theDatabase.getMapCanvas(map="rainMap"), normalSerialized=theDatabase.getMapCanvas(map="normalMap"))

@app.route('/projects', methods=['GET','POST'])
def projects():
    tablesTable()
    if(request.method=='POST'):
        if(request.form['type']=="DP"):
            theDatabase.delProj(request.form['projKey'])
        elif(request.form['type']=="tables"):
            files=request.files['file']
            processTables(files)
    return render_template('projects.html', entries=theDatabase.getAllEntriesWithSubmissionNums(), pageName="Projects", emailForm=emailForm())


@app.route('/semesters')
def semesters():
    return render_template('semesters.html', pageName="Semesters", emailForm=emailForm(), entries=theDatabase.getAllSemesters(), currentSemester = theDatabase.getCurrentSemester(), registration = theDatabase.getRegistrationButton())

@app.route('/semesters/registration')
def toggleRegistration():
    theDatabase.toggleRegistration();
    return redirect(flask.url_for('semesters'));

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

@app.route('/map/<mapType>/<serialized>')
def saveMap(mapType, serialized):
    theDatabase.setMapCanvas(mapSerialized = serialized, map = mapType)
    return redirect(flask.url_for('map'))

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

def tablesTable():
    tableFile = open(os.path.join(UPLOAD_FOLDER,"tables.csv"),'w')
    tableFile.write("ID,Project Name, Table Number\n")
    for entry in theDatabase.getAllEntriesWithSubmissionNums():
        if "table" in entry[0].keys():
            tableFile.write(str(entry[1]) + "," + entry[0]["projectName"]+ "," + entry[0]["table"] + "\n")
        else:
            tableFile.write(str(entry[1]) + "," + entry[0]["projectName"]+ "," + "\n")
    tableFile.close()

def processTables(csvFile):
    csvFile.save(os.path.join(UPLOAD_FOLDER,"upTables.csv"))
    csvfile = open(os.path.join(UPLOAD_FOLDER,"upTables.csv"), "r")
    csvfile.seek(0)
    firstRow = True
    for row in csvfile:
        if firstRow ==True:
            firstRow = False
            continue
        curRow = string.split(row,',')
        print str(curRow[0]) + "  " + str(curRow[2])
        theDatabase.setTableNum(curRow[0],curRow[2].strip())

@app.route('/addteam', methods=['GET', 'POST'])
def home():
    teamFormInstance = teamForm(request.form)
    if request.method == 'GET':
        return render_template('../form/templates/home.html', form=teamFormInstance)
    elif request.method == 'POST':
        if teamFormInstance.validate() == False:
            flash(
                "There was an error in the data you submitted. Please check all the fields and try again.")
            return render_template('../form/templates/home.html', form=teamFormInstance)
        else:
            formDict = teamFormInstance.convertToDictionary()
            key = theDatabase.saveToDB(formDict)
            dbData = theDatabase.getAllDataForSubmission(key)
            if dbData == formDict:
                sendConfirmation(app, teamFormInstance.teamEmail.data, teamFormInstance.CreateEmailBodyHTML(getTemplatePath(app)))
            else:
                flash("There was an error submitting the form. Please Try again. If you experience more issues please contact " + config.get("MailServer","MAIL_DEFAULT_SENDER"))
                return render_template('../form/templates/home.html', form=teamFormInstance)

            return render_template('../form/templates/success.html')


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
