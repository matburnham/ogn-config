from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])

class PasswordForm(FlaskForm):
  current_password = PasswordField('Current password', validators=[DataRequired()])
  new_password = PasswordField('New password', validators=[DataRequired()])
  new_password2 = PasswordField('Confirm new password', validators=[DataRequired()])

class WifiForm(FlaskForm):
  ssid = StringField('SSID', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])

