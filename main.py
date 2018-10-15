from flask import Flask, request, redirect, render_template

import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True

# DISPLAY A FORM

@app.route('/signup')
def display_user_signup_form():
    return render_template('home.html')

# FUNCTIONS FOR CORRECT INPUT

def empty_value(x):
    if x:
        return True
    else:
        return False

def char_length(x):
    if len(x) > 2 and len(x) < 21:
        return True
    else:
        return False

def email_at_symbol(x):
    if x.count('@') >= 1:
        return True
    else:
        return False

def multiple_at(x):
    if x.count('@') <= 1:
        return True
    else:
        return False

def email_period(x):
    if x.count('.') >= 1:
        return True
    else:
        return False

def multiple_period(x):
    if x.count('.') <= 1:
        return True
    else:
        return False

#  ROUTE TO PROCESS FORM

@app.route("/signup", methods=['POST'])
def user_signup_complete():

    #  VARIABLES FROM THE FORMS INPUTS

    username = request.form['username']
    password = request.form['password']
    password_validate = request.form['password_validate']
    email = request.form['email']

    # EMPTY STRINGS FOR THE ERROR MESSAGES

    username_error = ""
    password_error = ""
    password_validate_error = ""
    email_error = ""

    #  ERROR MESSAGES 

    error_required = "Required field"
    error_password = "Please re-enter password"
    error_char_count = "must be between 3 and 20 characters"
    error_no_spaces = "must not contain spaces"

    # CHECKS IF PASSWORD IS CORRECT

    if not empty_value(password):
        password_error = error_required
        password = ''
        password_validate = ''
    elif not char_length(password):
        password_error = "Password " + error_char_count
        password = ''
        password_validate = ''
        password_validate_error = error_password
    else:
        if " " in password:
            password_error = "Password " + error_no_spaces
            password = ''
            password_validate = ''
            password_validate_error = error_password

    # THIS IS THE SECOND PASSWORD VALIDATION

    if password_validate != password:
        password_validate_error = "Passwords must match"
        password = ''
        password_validate = ''
        password_error = 'Passwords must match'
            

    # THIS IS THE USERNAME VALIDATION

    if not empty_value(username):
        username_error = error_required
        password = ''
        password_validate = ''
        password_error = error_password
        password_validate_error = error_password
    elif not char_length(username):
        username_error = "Username " + error_char_count
        password = ''
        password_validate = ''
        password_error = error_password
        password_validate_error = error_password
    else:
        if " " in username:
            username_error = "Username " + error_no_spaces
            password = ''
            password_validate = ''
            password_error = error_password
            password_validate_error = error_password

    

    # checks the email
    if empty_value(email):
        
        if not char_length(email):
            email_error = "Email " + error_char_count
            password = ''
            password_validate = ''
            password_error = error_password
            password_validate_error = error_password
        elif not email_at_symbol(email):
            email_error = "Email must contain the @ symbol"
            password = ''
            password_validate = ''
            password_error = error_password
            password_validate_error = error_password
        elif not multiple_at(email):
            email_error = "Email must contain only one @ symbol"
            password = ''
            password_validate = ''
            password_error = error_password
            password_validate_error = error_password
        elif not email_period(email):
            email_error = "Email must contain period"
            password = ''
            password_validate = ''
            password_error = error_password
            password_validate_error = error_password
        elif not multiple_period(email):
            email_error = "Email must contain only one period"
            password = ''
            password_validate = ''
            password_error = error_password
            password_validate_error = error_password
        else:
            if " " in email:
                email_error = "Email " + error_no_spaces
                password = ''
                password_validate = ''
                password_error = error_password
                password_validate_error = error_password

    
    # Direct to welcome.html or display error

    if not username_error and not password_error and not password_validate_error and not email_error:
        username = username
        return redirect('/welcome?username={0}'.format(username))
    else:
        return render_template('home.html', username_error=username_error, username=username, password_error=password_error, password=password, password_validate_error=password_validate_error, password_validate=password_validate, email_error=email_error, email=email)

# DWELCOME PAGE

@app.route('/welcome')
def valid_signup():
    username = request.args.get('username')
    return render_template('welcome.html', username=username)

app.run()