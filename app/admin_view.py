import math
from flask import Blueprint, redirect, render_template, request, session, url_for, jsonify, flash
from app.db_utils import connect_db, get_cursor
from datetime import timedelta
from app.sql import *
adview_blp = Blueprint(
    "adview", __name__, template_folder='templates/admin', static_folder='static')


@adview_blp.route('/home')
def admin_home():
    return render_template('admin_home.html')

@adview_blp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('auth.login'))
@adview_blp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html', title='Dashboard')
@adview_blp.route('/profile')
def profile():
    msg = {}
    id_account = session['id']
    conn = connect_db()
    cursor = get_cursor(conn) 
    try:
        cursor.execute(user['get_account_info']% (id_account,))
        conn.commit()
    except:
        conn.rollback()
    info = cursor.fetchone()
    info = {'account_id': info[0], 'email': info[1], 'user_name': info[2],
            'password': info[3], 'role_id': info[4], 'account_isdelete': info[5]}
    try:
        cursor.execute(user['get_customer_info']% (id_account, ))
        conn.commit()
    except:
        conn.rollback()
    khachhang = cursor.fetchone()

    if khachhang:
        session['customer_id'] = khachhang[0]
        khachhang = {'customer_id': khachhang[0], 'first_name': khachhang[1], 'last_name': khachhang[2], 'account_id': khachhang[3], 'customer_identity': khachhang[4], 'customer_gender': khachhang[5],
                 'customer_phone': khachhang[6], 'customer_address': khachhang[7], 'customer_date': khachhang[8], 'customer_note': khachhang[10], 'customer_nation': khachhang[9]}
    try:
        cursor.execute(user['info_action'] % (session['customer_id'],))
        conn.commit()
    except:
        conn.rollback()
    
    # print(session['customer_id'])
    hoatdong = cursor.fetchall()
    lichsu = []
    if hoatdong:
        trangthai = {'0': 'Đã thanh toán', '1': 'Đã đặt', '2': 'Chờ duyêt', '3': 'Đã hủy'}
        for row in hoatdong:
            temp = {}
            temp['room_name'] = row[0]
            temp['time_start'] = row[1]
            temp['time_end'] = row[2]
            temp['status'] = trangthai[str(row[3])]
            lichsu.append(temp)
    try:
        cursor.execute('select * from user_image where user_id = %s', (id_account,))
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
    return render_template('admin/profile.html', info=info,khachhang=khachhang,msg=msg, lichsu=lichsu,img=img)
@adview_blp.route('/manage_rooms', defaults={'page': 1})
@adview_blp.route('/manage_rooms/<int:page>', methods=['GET', 'POST'])
def room(page):
    limit = 5

    offset = page * limit - limit
    conn = connect_db()
    cursor = get_cursor(conn)
    try:
        cursor.execute('SELECT * FROM phong where room_isdelete = 1')
        conn.commit()
    except:
        conn.rollback()
    total_row = cursor.rowcount
    total_page = math.ceil(total_row/limit)

    next = page + 1
    prev = page - 1
    try:
        cursor.execute('SELECT * FROM phong')
        conn.commit()
    except:
        conn.rollback()
    conn.close()
    total_row = cursor.rowcount
    total_page = math.ceil(total_row/limit)
    
    conn = connect_db()
    cursor = get_cursor(conn)
    phong=''
    try:
        cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 1 order by phong.room_id LIMIT %s OFFSET %s;', (limit, offset,))
        conn.commit()
        phong = cursor.fetchall()
    except:
        conn.rollback()
    final_data = []
    for row in phong:
        temp = {}
        temp['room_id'] = row[0]
        temp['room_name'] = row[1]
        temp['room_address'] = row[2]
        temp['room_performance'] = row[3]
        temp['room_price'] = row[4]
        temp['room_type'] = row[5]
        temp['room_province'] = row[6]
        temp['room_isdelete'] = 'Active'

        final_data.append(temp)
    conn.close()
    # print(final_data)
    return render_template('admin/room.html', data = final_data, page=total_page, next=next, prev=prev)
@adview_blp.route('/room_filter', defaults={'page': 1})
@adview_blp.route('/room_filter/<int:page>')
def filter(page):
    limit = 5
    offset = page * limit - limit
    conn = connect_db()
    cursor = get_cursor(conn)
    try:
        cursor.execute('SELECT * FROM phong where room_isdelete = 1')
    except:
        conn.rollback()
    total_row = cursor.rowcount
    total_page = math.ceil(total_row/limit)

    next = page + 1
    prev = page - 1
    try:
        cursor.execute('SELECT * FROM phong')
    except:
        conn.rollback()
    conn.close()
    total_row = cursor.rowcount
    total_page = math.ceil(total_row/limit)
    conn = connect_db()
    cursor = get_cursor(conn)
    phong=''
    id_filter = request.args.get('id_filter')
    show_option = request.args.get('show_option')
    if show_option == 'hoatdong':
        if id_filter == 'room_id':
            try:
                cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 1  order by phong.room_id LIMIT %s OFFSET %s;', (limit, offset,))
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
        elif id_filter == 'room_price_up':
            try:
                cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 1  order by phong.room_price ASC LIMIT %s OFFSET %s;', (limit, offset,))
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
        else:
            try:
                cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province  where phong.room_isdelete = 1 order by phong.room_price DESC LIMIT %s OFFSET %s;', (limit, offset,))
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
        conn.close()
    else:
        cursor.execute('SELECT * FROM phong where room_isdelete = 0')        
        total_row = cursor.rowcount
        total_page = math.ceil(total_row/limit)
        if id_filter == 'room_id':
            try:
                cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 0  order by phong.room_id LIMIT %s OFFSET %s;', (limit, offset,))
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
        elif id_filter == 'room_price_up':
            try:
                cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 0  order by phong.room_price ASC LIMIT %s OFFSET %s;', (limit, offset,))
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
        else:
            try:
                cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province  where phong.room_isdelete = 0 order by phong.room_price DESC LIMIT %s OFFSET %s;', (limit, offset,))
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
    final_data = []
    for row in phong:
        temp = {}
        temp['room_id'] = row[0]
        temp['room_name'] = row[1]
        temp['room_address'] = row[2]
        temp['room_performance'] = row[3]
        temp['room_price'] = row[4]
        temp['room_type'] = row[5]
        temp['room_province'] = row[6]
        if row[7] == b'\x00':
            temp['room_isdelete'] = 'UNACTIVE'
        else:
            temp['room_isdelete'] = 'ACTIVE'
        final_data.append(temp)
    print(id_filter, show_option)
    return render_template('admin/room.html', data = final_data, show_option=show_option, id_filter=id_filter, page=total_page, next=next, prev=prev)

@adview_blp.route('/customer')
def customer():
    conn = connect_db()
    cursor = get_cursor(conn)
    try:
        cursor.execute('select * from khachhang where customer_isdelete = 1')
        conn.commit()
    except:
        conn.commit()
    khachhang = cursor.fetchall()
    print(khachhang)
    data = []
    for row in khachhang:
        temp = {}
        temp['customer_id'] = row[0]
        temp['customer_name'] = row[1] + ' ' + row[2]
        temp['customer_identity'] = row [4]
        temp['customer_gender'] = row[5]
        temp['customer_phone'] = row[6]
        temp['customer_date'] = row[8]
        temp['customer_address'] =row[7]
        temp['customer_nation'] = row[9]
        temp['customer_note'] = row[10]
        if row[11] == b'\x01':
            temp['customer_isdelete'] = 'ACTIVE'
        else:
            temp['customer_isdelete'] = 'UNACTIVE'

        data.append(temp)
    print(data)
    return render_template('admin/customer.html', data=data)
@adview_blp.route('/filter_customer')
def filter_customer():
    show_option = request.args.get('show_option')
    id_file = request.args.get('id_filter')
    if show_option == 'daxoa':
        if id_file == 'name_up':
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                cursor.execute('select * from khachhang where customer_isdelete = 0 order by last_name asc;')
            except:
                conn.rollback()
            khachhang = cursor.fetchall()    
            conn.close()
        elif id_file == 'name_down':
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                cursor.execute('select * from khachhang where customer_isdelete = 0 order by last_name desc;')
            except:
                conn.rollback()
            khachhang = cursor.fetchall()    
            conn.close()
        else:
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                cursor.execute('select * from khachhang where customer_isdelete = 0 order by customer_id asc;')
            except:
                conn.rollback()
            khachhang = cursor.fetchall()    
            conn.close()
    else:
        if id_file == 'name_up':
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                cursor.execute('select * from khachhang where customer_isdelete = 1 order by last_name asc;')
            except:
                conn.rollback()
            khachhang = cursor.fetchall()    
            conn.close()
        elif id_file == 'name_down':
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                cursor.execute('select * from khachhang where customer_isdelete = 1 order by last_name desc;')
            except:
                conn.rollback()
            khachhang = cursor.fetchall()    
            conn.close()
        else:
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                cursor.execute('select * from khachhang where customer_isdelete = 1 order by customer_id asc;')
            except:
                conn.rollback()
            khachhang = cursor.fetchall()    
            conn.close()
    data = []
    for row in khachhang:
        temp = {}
        temp['customer_id'] = row[0]
        temp['customer_name'] = row[1] + ' ' + row[2]
        temp['customer_identity'] = row [4]
        temp['customer_gender'] = row[5]
        temp['customer_phone'] = row[6]
        temp['customer_date'] = row[8]
        temp['customer_address'] =row[7]
        temp['customer_nation'] = row[9]
        temp['customer_note'] = row[10]
        if row[11] == b'\x01':
            temp['customer_isdelete'] = 'ACTIVE'
        else:
            temp['customer_isdelete'] = 'UNACTIVE'

        data.append(temp)
    print(data)
    return render_template('admin/customer.html', data=data, id_filter = id_file, show_option=show_option)
    

@adview_blp.route('/room_booking')
def booking_room():
    return render_template('admin/booking.html')

