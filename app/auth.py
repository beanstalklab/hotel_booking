import datetime
import os
import re
from flask import Blueprint, redirect, render_template, request, session, url_for, flash, make_response
from pymysql import Date
from app.db_utils import connect_db, get_cursor
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from app.sql import *
auth_blp = Blueprint(
    "auth", __name__, template_folder='templates', static_folder='static')
global COOKIE_TIME_OUT 
COOKIE_TIME_OUT = 60*5
@auth_blp.route('/login')
def login():
    return render_template('auth/login.html')
@auth_blp.route('/login_submit', methods=['POST'])
def login_submit():
    email = request.form['email']
    password = request.form['password']
    remember = request.form.getlist('inputRemember')
    if 'email' in request.cookies:
        username = request.cookies.get('email')
        password = request.cookies.get('password')
        conn = connect_db()
        cursor = get_cursor(conn)
        sql = 'SELECT * from taikhoan where email=%s;'
        cursor.execute(sql, (username, ))
        row = cursor.fetchone()
        if row and check_password_hash(row[3], password):
            session['email'] = row[2]
            session['loggedin'] = True
            session['id'] = row[0]
            session['username'] = row[2]
            session['role_id'] = row[4]
            cursor.close()
            conn.close()
            if row[4] == 0:
                return redirect('/manage_rooms')
            return redirect('/home')
        else:
            return redirect('/login')
    elif email and password:        
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
        if account:
            if check_password_hash(account[3], password):
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[2]
                session['role_id'] = account[4]
                if account[4] == 0:
                    return redirect('/manage_rooms')
                if remember:
                    resp = make_response(redirect('/home'))
                    resp.set_cookie('email', account[1], max_age=COOKIE_TIME_OUT)
                    resp.set_cookie('password', password, max_age=COOKIE_TIME_OUT)
                    resp.set_cookie('rem', 'checked', max_age=COOKIE_TIME_OUT)
                    return resp
                flash("Login successfully")
                print(session['role_id'])
                return redirect('/home')
            else:
                flash('Invalid Password')
                return redirect('/login')
        else:
            flash("Account does not exist")
            return redirect('/login')
    else:
        flash('Invalid Email or Password')
        return redirect('/login')
@auth_blp.route('/resetpass', methods=['GET', 'POST'])
def resetpass():
    msg = ''
    if request.method == 'POST' and 'password' in request.form:
        new_password = request.form['password']
        email = request.form['email']
        repeat_password = request.form['repassword']
        conn = connect_db()
        cursor = get_cursor(conn)
        cursor.execute('select * from taikhoan where email = %s', (email, ))
        check_account = cursor.fetchone()
        if check_account:
            if (repeat_password ==  new_password):
                conn = connect_db()
                cursor = get_cursor(conn)
                cursor.execute(account['reset_password'],
                            (generate_password_hash(new_password), email, ))
                msg = 'Thay đổi mật khẩu thành công'
                conn.commit()
                return redirect(url_for('auth.login'))

            else:
                flash('Mật khẩu chưa khớp')
        else:
            flash('Tài khoản không tồn tại')
            return redirect(url_for('auth.resetpass'))
    return render_template('auth/reset_password.html', msg=msg, title='Reset Password Page')

@auth_blp.route('/register')
def register():
    return render_template('auth/register.html')
@auth_blp.route('/register_submit', methods=['GET', 'POST'])
def register_submit():
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
            flash('Email đã tồn tại!')
        elif not username or not password or not email:
            flash('Please fill out the form !')
        elif not (repassword == password):
            flash('Invalid password, please try again')
        else:
            password_hash = generate_password_hash(password)
            cursor.execute('INSERT INTO taikhoan VALUES (NULL, %s, %s, %s, 2, 0)',
                           (email, username, password_hash, ))
            conn.commit()
            msg = 'Đăng ký tài khoản thành công'
            return redirect('/login')
    return redirect('/register')
@auth_blp.route('/customer_booking/<room_id>', methods=['get'])
def customer_booking(room_id):
    # create connect to database
    conn = connect_db()
    cursor = get_cursor(conn)
    # Get data from form 
    checkin = request.args.get('start')
    checkout = request.args.get('end')
    service  = request.args.getlist('service')

    #Convert date format to insert to database
    checkout = get_date(checkout)
    checkin = get_date(checkin)
    print(checkout, checkin,service, len(service))
    days = int((checkout - checkin).days)

    # Start query data to caculate
    cursor.execute('select customer_id from khachhang where account_id = %s', (session['id'],))
    customer = cursor.fetchone()
    if (customer):
        cursor.execute('select room_price from phong where room_id = %s', (room_id, ))
        room_price = cursor.fetchone()
        if len(service) > 0:
            cursor.execute('select service_price from dichvu where service_id in %s', (service, ))
            service_price = cursor.fetchall()
            
            # Caculate money
            sum_service = 0
            for i in service_price: 
                sum_service += int(i[0])
        else:
             sum_service = 0
        total_money = sum_service + int(room_price[0]) * days
        cursor.execute('insert into datphong values (NULL, {}, {}, date("{}"), date("{}"))'.format(customer[0], room_id, checkin, checkout))
        conn.commit()
        print('insert datphong ok')
        cursor.execute('select bookroom_id from datphong where customer_id = {}  and room_id = {} and time_start like "%{}%" and time_end like "%{}%"'.format(customer[0], room_id, checkin, checkout, ))
        id_datphong = cursor.fetchone()
        print(id_datphong)
        # # Generate bill_id
        bill_id = str(id_datphong[0]) + "_" + str(customer[0])
        print(bill_id, total_money, id_datphong[0])
        cursor.execute("insert into hoadon VALUES (%s,%s,%s, 'Chưa thanh toán')",(bill_id,id_datphong[0], total_money,))
        conn.commit()
        print('Thanh cong')
        if len(service) > 0:
            for item in service:
                cursor.execute('insert into ql_dichvu values (NULL, %s, %s, 1)', (item,id_datphong[0]))
                conn.commit()
        conn.close()
            
        flash('Bạn đã đặt phòng thành công')
        return redirect(url_for('view.profile'))
    #     try:
    #         cursor.execute('insert into datphong values (NULL, {}, {}, date("{}"), date("{}"))'.format(customer[0], room_id, checkin, checkout))
    #         conn.commit()
    #         print('insert datphong ok')
    #         cursor.execute('select bookroom_id from datphong where customer_id = {}  and room_id = {} and time_start like "%{}%" and time_end like "%{}%"'.format(customer[0], room_id, checkin, checkout, ))
    #         id_datphong = cursor.fetchone()
    #         print(id_datphong)
    #         # # Generate bill_id
    #         bill_id = str(id_datphong[0]) + "_" + str(customer[0])
    #         print(bill_id, total_money, id_datphong[0])
    #         cursor.execute("insert into hoadon (`id_bill`,`bookroom_id`, `tongtien`, `tinhtrang`) VALUES ({},{},{}, 'Chưa thanh toán')".format(bill_id,id_datphong[0], total_money))
    #         conn.commit()
    #         print('Thanh cong')
    #         conn.close()
    #         flash('Bạn đã đặt phòng thành công')
    #         return redirect(url_for('view.profie'))
    #     except:
    #         conn.rollback()
    #         return (redirect('/home'))

    # else:
    #     flash('Bạn cần hoàn thiện thông tin cá nhân để đặt phòng')
    #     return render_template('view.profile')
def get_date(dates):
    temp = dates.split('/')
    return  datetime.date(int(temp[2]),int(temp[0]),int(temp[1]))

@auth_blp.route('/edit_profile')
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
    try:
        cursor.execute('select * from user_image where user_id = %s', (account_id,))
        conn.commit()
    except:
        conn.rollback()
    img = cursor.fetchone()
    # print(img[2])
    if img:
        index = img[2].index('/')
        img = {'folder': img[2][0:index],
                'name': img[2][index+1:]}
    print(img)  
    conn.close()
    return render_template('user/profile-edit.html', khachhang=khachhang, info=info, msg=msg, img=img)

@auth_blp.route('/edit_profile_submit', methods=['GET', 'POST'])
def edit_profile_submit():
    account_id = session['id']
    print(account_id)
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
        image = request.form['user_img']
        user_image = 'user_image' +'/' + str(image)
        conn = connect_db()
        cursor = get_cursor(conn)
        print(user_image)
        try:
            sql='''SELECT * FROM khachhang where account_id = %s'''
            cursor.execute(sql % (account_id))
            print("true")
            conn.commit()
        except:
            conn.rollback()
        data = cursor.fetchone()

        if data:
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                sql1 =  '''UPDATE khachhang SET `first_name` = %s, `last_name` = %s, `customer_identity`= %s,`customer_date`=%s, `customer_phone` = %s, `customer_address`=%s,`customer_gender`=%s,   `customer_note` = %s 
                                WHERE `account_id` = %s;'''
                cursor.execute(sql1, (firstname, lastname, identity,birthday, phone_number, address, gender,   note, account_id,))
                print('Update khachhang seccuessfully')
                sql2 = '''UPDATE taikhoan  SET `user_name` = %s where `account_id` = %s;'''
                cursor.execute(sql2, (username, account_id,))
                conn.commit()
                print('Update taikhoan seccuessfully')
                cursor.execute('select * from user_image where user_image.user_id = %s', (account_id,))
                conn.commit()
                img = cursor.fetchone()
                print(user_image)
                if image and img:
                    print('----------')
                    cursor.execute('update `user_image` set `img_link` = "{}" where `user_id` = {}'.format(user_image, account_id,))
                    conn.commit()
                    print('update anh')
                else:
                    cursor.execute('insert into user_image value (NULL, %s, %s)', (account_id, user_image,))
                    conn.commit()
                    print('insert')

            except:
                print('Update unseccuessfully')
                conn.rollback()
        else:
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                cursor.execute(user['insert_customer_info'], (firstname, lastname, account_id, identity, gender, phone_number, address, birthday, note,))
                conn.commit()
                cursor.execute(user['update_username'], (username, account_id))
                conn.commit()
                cursor.execute('insert into user_image value (NULL, %s, %s)', (account_id, user_image,))
                conn.commit()
                print('Insert khachhang seccuessfully')
                msg='Cập nhật thông tin thành công'

            except:
                print('Insert khachhang unseccuessfully')

                conn.rollback()

        conn.commit()
        return redirect(url_for('view.profile'))
    else:
        # flash('Update seccuessfully')
        print('Update unseccuessfully')
        return redirect('auth.edit_profile')

@auth_blp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('view.home'))
