import re
from flask import Blueprint, redirect, render_template, request, session, url_for
from app.db_utils import connect_db, get_cursor
from werkzeug.security import check_password_hash, generate_password_hash

auth_blp = Blueprint("auth", __name__,template_folder='templates', static_folder='static')
@auth_blp.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        session.permanent = True
        email = request.form['email']
        password = request.form['password']
        conn = connect_db()
        cursor = get_cursor(conn)
        cursor.execute('SELECT * FROM taikhoan WHERE email = % s ', (email,))
        account = cursor.fetchone()
        conn.commit()
        # print(account)
        if account and check_password_hash(account[3], password):
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[2]
            session['role_id'] = account[4]
            msg = 'Logged in successfully !'
            return redirect(url_for('view.home'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('auth/login.html', msg=msg, title='Login Page')
@auth_blp.route('/resetpass', methods=['GET', 'POST'])
def resetpass():
    msg = ''
    if request.method == 'POST' and 'password' in request.form:
        new_password = request.form['password']
        email = request.form['email']
        conn = connect_db()
        cursor = get_cursor(conn)
        cursor.execute('UPDATE taikhoan SET `password` = % s where `email` = % s;',
                       (generate_password_hash(new_password), email, ))
        msg = 'You have changed password successfully'
        conn.commit()
        return render_template('login')
    return render_template('reset_password.html', msg=msg, title='Reset Password Page')
@auth_blp.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']

        email = request.form['email']
        conn = connect_db()
        cursor = get_cursor(conn)

        cursor.execute('SELECT * FROM taikhoan WHERE email = % s', (email, ))
        account = cursor.fetchall()
        if account:
            msg = 'Email already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        elif not (repassword == password):
            msg = 'Invalid password, please try again'
        else:
            password_hash = generate_password_hash(password)
            cursor.execute('INSERT INTO taikhoan VALUES (NULL, %s, %s, %s, 2, 0)',
                           (email, username, password_hash, ))
            conn.commit()
            msg = 'You have successfully registered !'
            return render_template('home.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)

@auth_blp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('password', None)
    return redirect(url_for('view.home'))