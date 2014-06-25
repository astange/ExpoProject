import os

from flask import Flask
from flask.ext.mail import Mail
from flask.ext.mail import Message
import configparser

from settings import APP_CONFIG


app = Flask(__name__)

# Mail server defaults
_mailServer = 'localhost'
_mailPort = 25
_mailUseTSL = False
_mailUseSSL = False
_mailDebug = app.debug
_mailUsername = None
_mailPassword = None
_mailDefaultSender = None
_defaultMailSender = None
_mailSuppressSend = app.testing
_mailMaxEmails = None

# Confirmation Email
_subject = ""
_adminSubject = ""
_bodyTemplateFile = ""


# Parse the Config File
config = configparser.ConfigParser(allow_no_value = True)
fileName = os.path.join(APP_CONFIG, 'mail.cfg')
config.read(fileName)
configSet = False


def sendConfirmation(app, teamEmail):
    if not configSet :
        setConfigOptions(app)
    mail = Mail(app)
    msg = Message(subject=_subject, sender=_mailDefaultSender, recipients=[teamEmail], bcc=_mailDefaultSender)
    msg.body = getEmailTemplate()
    mail.send(msg)


def getEmailTemplate():
    try :
        file = open(_bodyTemplateFile, "r")
        return file.read()
    except IOError as e :
        print "I/O error({0}): {1} : Tried to open file ""{2}""".format(e.errno, e.strerror, _bodyTemplateFile)
        return "Thank you for registering for the GT Expo"


def setConfigOptions(app) :
    global configSet
    configSet = True


    # MAIL SERVER OPTIONS
    if (config.has_option("MailServer","MAIL_SERVER")) :
        global _mailServer
        _mailServer = config.get("MailServer","MAIL_SERVER")
        _mailServer = _mailServer.encode('utf-8')
        app.config.update(MAIL_SERVER = _mailServer)
    if (config.has_option("MailServer","MAIL_PORT")) :
        global _mailPort
        _mailPort = config.getint("MailServer", "MAIL_PORT")
        app.config.update(MAIL_PORT = _mailPort)
    if (config.has_option("MailServer","MAIL_USE_TSL")) :
        global _mailUseTSL
        _mailUseTSL = config.getboolean("MailServer","MAIL_USE_TSL")
        app.config.update(MAIL_USE_TSL = _mailUseTSL)
    if (config.has_option("MailServer","MAIL_USE_SSL")) :
        global _mailUseSSL
        _mailUseSSL = config.getboolean("MailServer", "MAIL_USE_SSL")
        app.config.update(MAIL_USE_SSL = _mailUseSSL)
    if (config.has_option("MailServer","MAIL_DEBUG")) :
        global _mailDebug
        _mailDebug = config.getboolean("MailServer","MAIL_DEBUG")
        app.config.update(MAIL_DEBUG = _mailDebug)
    if (config.has_option("MailServer","MAIL_USERNAME")) :
        global _mailUsername
        _mailUsername = config.get("MailServer","MAIL_USERNAME")
        _mailUsername = _mailUsername.encode('utf-8')
        app.config.update(MAIL_USERNAME = _mailUsername)
    if (config.has_option("MailServer","MAIL_PASSWORD")) :
        global _mailPassword
        _mailPassword = config.get("MailServer","MAIL_PASSWORD")
        _mailPassword = _mailPassword.encode('utf-8')
        app.config.update(MAIL_PASSWORD = _mailPassword)
    if (config.has_option("MailServer","MAIL_DEFAULT_SENDER")) :
        global _mailDefaultSender
        _mailDefaultSender = config.get("MailServer","MAIL_DEFAULT_SENDER")
        _mailDefaultSender = _mailDefaultSender.encode('utf-8')
        app.config.update(MAIL_DEFAULT_SENDER = _mailDefaultSender)
    if (config.has_option("MailServer","MAIL_SUPPRESS_SEND")) :
        global _mailSuppressSend
        _mailSuppressSend = config.getboolean("MailServer","MAIL_SUPPRESS_SEND")
        app.config.update(MAIL_SUPPRESS_SEND = _mailSuppressSend)
    if (config.has_option("MailServer","MAIL_MAX_EMAILS")) :
        global _mailMaxEmails
        _mailMaxEmails = config.getint("MailServer","MAIL_MAX_EMAILS")
        app.config.update(MAIL_MAX_EMAILS = _mailMaxEmails)

    #CONFIRMATION EMAIL OPTIONS
    if (config.has_option("ConfirmationEmail","CONFIRM_BODY_TEMPLATE_FILE")) :
        global _bodyTemplateFile
        tmp = config.get("ConfirmationEmail","CONFIRM_BODY_TEMPLATE_FILE").encode('utf-8')
        _bodyTemplateFile = os.path.join(APP_CONFIG, tmp)
    if config.has_option("ConfirmationEmail","CONFIRM_SUBJECT") :
        global _subject
        _subject = config.get("ConfirmationEmail","CONFIRM_SUBJECT").encode('utf-8')
    if config.has_option("ConfirmationEmail", "CONFIRM_SUBJECT_ADMIN") :
        global _adminSubject
        _adminSubject = config.get("ConfirmationEmail", "CONFIRM_SUBJECT_ADMIN")
