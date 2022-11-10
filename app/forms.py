from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 20)], render_kw={'placeholder':'example@example.com'})
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 20)], render_kw={'placeholder': '**************'})
    # remember = BooleanField('Remember me')
    submit = SubmitField()