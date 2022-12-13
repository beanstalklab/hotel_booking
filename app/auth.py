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

@auth_blp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    account_id = session['id']
    msg = 'Wating'
    # Query data from dabases to show on web
    conn = connect_db()
    cursor = get_cursor(conn)
    cursor.execute(
        'select * from taikhoan where taikhoan.account_id = % s;', (account_id,))
    info = cursor.fetchone()
    info = {'account_id': info[0], 'email': info[1], 'user_name': info[2],
            'password': info[3], 'role_id': info[4], 'account_isdelete': info[5]}
    cursor.execute(
        'select * from khachhang where khachhang.account_id = % s', (account_id, ))
    khachhang = cursor.fetchone()
    khachhang = {'customer_id': khachhang[0], 'customer_name': khachhang[1], 'account_id': khachhang[2], 'customer_identity': khachhang[3], 'customer_gender': khachhang[4],
                 'customer_phone': khachhang[5], 'customer_address': khachhang[6], 'customer_date': khachhang[7], 'customer_note': khachhang[8], 'customer_isdelete': khachhang[9]}
    conn.commit()

    if request.method == 'POST' and 'identify' in request.form and 'address' in request.form and 'birthday' in request.form:
        fullname = request.form['fullname']
        username = request.form['username']
        gender = request.form['gender']
        phone_number = request.form['phonenumber']
        identity = request.form['identify']
        address = request.form['address']
        birthday = request.form['birthday']
        note = request.form['note']
        conn = connect_db()
        cursor = get_cursor(conn)        
        cursor.execute(
            'SELECT * FROM khachhang where account_id = %s', (account_id, ))
        data = cursor.fetchone()
        conn.commit()

        if data:
            conn = connect_db()
            cursor = get_cursor(conn)
            cursor.execute('UPDATE khachhang SET `customer_name` = %s, `customer_identity`= %s, `customer_gender`=%s, `customer_phone` = %s, `customer_address`=%s,  `customer_note` = %s where `account_id` = %s',
                           (fullname, identity, gender, phone_number, address, account_id, birthday, note, account_id,))
            cursor.execute(
                'UPDATE taikhoan  SET `user_name` = %s where `account_id` = %s', (username, account_id))
        else:
            conn = connect_db()
            cursor = get_cursor(conn)            
            cursor.execute('INSERT INTO khachhang values(NULL, %s, %s, %s, %s,%s, %s, %s, %s, 0)', (
                fullname, account_id, identity, gender, phone_number, address, birthday, note,))
            cursor.execute(
                'UPDATE taikhoan  SET user_name = %s where account_id = %s', (username, account_id))

        conn.commit()
        return redirect(url_for('profile'))
    else:
        msg = 'Edit profile not successful'
    return render_template('user/profile-edit.html', khachhang=khachhang, info=info, msg=msg)
@auth_blp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('password', None)
    return redirect(url_for('view.home'))