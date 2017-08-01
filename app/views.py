from flask import render_template, redirect, url_for, session
from datetime import datetime,timedelta
from pam import pam
import subprocess

from . import app
from .forms import LoginForm, PasswordForm, WifiForm

def get_uptime():
  with open('/proc/uptime', 'r') as f:
    uptime_seconds = float(f.readline().split()[0])
    uptime_string = str(timedelta(seconds = uptime_seconds))
  return uptime_string

config = {
  'station': 'stationid',
  'location': 'loc',
  'alt': 100,
  'geoidsep': 100,
  'gsmfreq': 800,
  'gain': 20,
  'pass_set' : False,
  'uptime': get_uptime(),
  'datetime': str(datetime.now()),
}

@app.route('/')
def index():
  # TODO: get details from /etc/rtlsdr-ogn.conf
  form = LoginForm()
  config['logged_in'] = 'logged_in' in session
  print 'logged_in' in session
  return render_template('index.html', config=config, form=form)

@app.route('/login',methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    print 'validate_on_submit'
    if pam().authenticate(form.username.data, form.password.data):
      print 'good password'
      session['username'] = form.username.data
      session['logged_in'] = True
      return redirect(url_for('index'))
  print 'err'

  return render_template('login.html', form=form)

@app.route('/logout')
def logout():
  if 'logged_in' in session:
    session.pop('logged_in')
  return index();

@app.route('/password',methods=['GET','POST'])
def password():
  form = PasswordForm()
  status = ''

  if(form.validate_on_submit()):
    if pam().authenticate(session['username'], form.current_password.data):
      if form.new_password.data == form.new_password2.data:
        print 'Changing password to ' + form.new_password.data
        # TODO: run password change command
        status = 'Password changed'
      else:
        form.new_password.errors.append('New passwords must match')
    else:
      form.current_password.errors.append('Incorrect password')
  return render_template('password.html', form=form, status=status)

@app.route('/wifi',methods=['GET','POST'])
def wifi():
  form = WifiForm()

  #'/etc/wpa_supplicant/wpa_supplicant.conf'
  #'wpa_supplicant.conf'


  form.ssid = subprocess.check_output(['sed', 's/.*ssid=[^"]*"\([^"]*\)".*/\1/', 'wpa_supplicant.conf'])

  #form.password = `sed 's/.*password=[^"]*"\([^"]*\)".*/\1/' wpa_supplicant.conf`

  if form.validate_on_submit():
    pass
    # TODO: save details

  return render_template('wifi.html', form=form)

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
