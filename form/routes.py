from flask import Flask, render_template, request, flash, Response
from functools import wraps
from teamForm import teamForm
from flask_wtf.csrf import CsrfProtect
import os
from redisDB import *
from mail import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


app = Flask(__name__)
theDatabase = RedisDB()

#These next three functions can be used to password protect a page.
#Simply put a @requires_auth immediately above the def function() line.
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


@app.route('/', methods=['GET', 'POST'])
def home():
    teamFormInstance = teamForm(request.form)
    if request.method == 'GET':
        if theDatabase.getRegistrationStatus() == "open":
            return render_template('home.html', form=teamFormInstance)
        else:
            return render_template('closed.html')
    elif request.method == 'POST':
        if teamFormInstance.validate() == False:
            flash(
                "There was an error in the data you submitted. Please check all the fields and try again.")
            return render_template('home.html', form=teamFormInstance)
        else:
            formDict = teamFormInstance.convertToDictionary()
            key = theDatabase.saveToDB(formDict)
            dbData = theDatabase.getAllDataForSubmission(key)
            if dbData == formDict:
                sendConfirmation(app, teamFormInstance.teamEmail.data, teamFormInstance.CreateEmailBodyHTML(getTemplatePath(app)))
            else:
                flash("There was an error submitting the form. Please Try again. If you experience more issues please contact " + config.get("MailServer","MAIL_DEFAULT_SENDER"))
                return render_template('home.html', form=teamFormInstance)

            return render_template('success.html')


@app.route('/listentries')
@requires_auth
def listEntries():
    return render_template('listEntries.html', entries=theDatabase.getAllEntriesWithSubmissionNums())


@app.route('/listentriesbyname')
@requires_auth
def listEntriesByName():
    return render_template('listEntriesByName.html', entries=theDatabase.getAllNames())


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True, host='0.0.0.0', port=5001)
