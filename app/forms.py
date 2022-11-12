from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, IPAddress

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 30)], render_kw={'placeholder':'example@example.com'})
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 20)], render_kw={'placeholder': '**************'})
    submit = SubmitField()

class DeviceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(4,45)])
    ipv4 = StringField('IPv4 Address', validators=[DataRequired(), IPAddress(ipv4=True)])
    submit = SubmitField('Create')

class DeleteDeviceForm(FlaskForm):
    submit = SubmitField('Delete')

class TestDeviceForm(FlaskForm):
    submit = SubmitField('Test')