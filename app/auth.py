import re
from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from app.db_utils import connect_db, get_cursor
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from app.sql import *
auth_blp = Blueprint(
    "auth", __name__, template_folder='templates', static_folder='static')


@auth_blp.before_request
def make_session_permanent():
    session.permanent = True
    auth_blp.permanet_session_lifetime = timedelta(minutes=5)


@auth_blp.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        session.permanent = True
        email = request.form['email']
        password = request.form['password']
        conn = connect_db()
        cursor = get_cursor(conn)
        try:
            cursor.execute(
                'SELECT * FROM taikhoan WHERE email = % s ', (email,))
            conn.commit()
        except:
            conn.rollback()
        account = cursor.fetchone()
        conn.close()        
        if account and check_password_hash(account[3], password):
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[2]
            session['role_id'] = account[4]
            msg = 'Logged in successfully !'
            if (session['role_id'] == 0):
                return redirect(url_for('admin.admin_home'))
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
        repeat_password = request.form['repassword']
        if (repeat_password ==  new_password):
            conn = connect_db()
            cursor = get_cursor(conn)
            cursor.execute(account['reset_password'],
                        (generate_password_hash(new_password), email, ))
            msg = 'You have changed password successfully'
            conn.commit()
            return redirect(url_for('auth.login'))

        else:
            msg = 'Passwords do not match !'
    return render_template('auth/reset_password.html', msg=msg, title='Reset Password Page')


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
    return render_template('auth/register.html', msg=msg)


@auth_blp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    account_id = session['id']
    msg = 'Wating'
    # Query data from dabases to show on web
    conn = connect_db()
    cursor = get_cursor(conn)
    try:
        cursor.execute(user['get_account_info'], (account_id,))
        cursor.commit()
    except:
        conn.rollback()
    info = cursor.fetchone()
    info = {'account_id': info[0], 'email': info[1], 'user_name': info[2],
            'password': info[3], 'role_id': info[4], 'account_isdelete': info[5]}
    try:
        cursor.execute(user['get_customer_info'], (account_id, ))
        conn.commit()
    except:
        conn.rollback()
    khachhang = cursor.fetchone()
    if khachhang:
        khachhang = {'customer_id': khachhang[0], 'first_name': khachhang[1], 'last_name': khachhang[2], 'account_id': khachhang[3], 'customer_identity': khachhang[4], 'customer_gender': khachhang[5],
                    'customer_phone': khachhang[6], 'customer_address': khachhang[7], 'customer_date': khachhang[8], 'customer_note': khachhang[10], 'customer_nation': khachhang[9]}
    conn.close()

    if request.method == 'POST' and 'identify' in request.form and 'address' in request.form and 'birthday' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        gender = request.form['gender']
        phone_number = request.form['phonenumber']
        identity = request.form['identify']
        address = request.form['address']
        birthday = request.form['birthday']
        note = request.form['note']
        conn = connect_db()
        cursor = get_cursor(conn)
        try:
            cursor.execute(user['get_customer_info'], (account_id, ))
            conn.commit()
        except:
            conn.rollback()
        data = cursor.fetchone()

        if data:
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                cursor.execute(user['update_customer_info'],
                               (firstname, lastname, identity, gender, phone_number, address, birthday, note, account_id,))
                cursor.execute(user['update_username'], (username, account_id))
                conn.commit()
            except:
                conn.rollback()
            flash('Update seccuessfully')
        else:
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                cursor.execute(user['insert_customer_info'], (firstname, lastname, account_id, identity, gender, phone_number, address, birthday, note,))
                cursor.execute(user['update_username'], (username, account_id))
                conn.commit()
            except:
                conn.rollback()
            flash('Update seccuessfully')

        conn.commit()
        return redirect(url_for('view.profile'))
    else:
        flash('Update seccuessfully')
    return render_template('user/profile-edit.html', khachhang=khachhang, info=info, msg=msg)


@auth_blp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('view.home'))
