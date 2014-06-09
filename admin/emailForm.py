from flask.ext.wtf import Form
from wtforms.fields import TextField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, ValidationError, Email


class emailForm(Form):
    name = TextField("Name", [InputRequired("Please enter your name.")])
    email = TextField("Email", [InputRequired(
        "Please enter your email address."), Email("Please enter a valid email address.")])
    message = TextAreaField(
        "Message", [InputRequired("Please enter a message.")])

    send = SubmitField("Send")
