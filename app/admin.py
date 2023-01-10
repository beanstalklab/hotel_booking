from flask import Blueprint, redirect, render_template, request, session, url_for, jsonify, flash
from app.db_utils import connect_db, get_cursor
from app.sql import *
import os
admin_blp = Blueprint(
    "admin", __name__, template_folder='templates/admin', static_folder='static')


@admin_blp.route('/edit_room/<id>', methods=['GET','POST'])
def edit_room(id):
    conn = connect_db()
    cursor = get_cursor(conn)
    phong = ''
    try:
        cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_id = %s;', (id,))
        conn.commit()
    except:
        conn.rollback()

    phong = cursor.fetchone()
    # print(phong)

    temp = {}
    temp['room_id'] = phong[0]
    temp['room_name'] = phong[1]
    temp['room_address'] = phong[2]
    temp['room_performance'] = phong[3]
    temp['room_price'] = phong[4]
    temp['room_type'] = phong[5]
    temp['room_province'] = phong[6]
    conn.close()
    return render_template('edit_room.html', row=temp)

@admin_blp.route('/edit_room_submit', methods=['GET','POST'])
def edit_room_submit():

    conn = connect_db()
    cursor = get_cursor(conn)
    room_id = request.args.get('room_id')
    room_name = request.args.get('room_name')
    room_address = request.args.get('room_address')
    room_performance = request.args.get('room_performance')
    room_type = request.args.get('room_type')
    room_price = request.args.get('room_price')
    room_province = request.args.get('room_province')
    print(room_type, room_province, room_id)
    
    # print(id_type, id_province)
    try:
        
        sql1 = '''select room_id from loaiphong where room_name like "%{}%" '''
        cursor.execute(sql1.format(room_type))
        conn.commit()
        id_type = cursor.fetchone()
        print('catch id_type', id_type[0])
        sql2 = '''select province_id from tinhthanh where province_name like "%{}%"'''
        cursor.execute(sql2.format(room_province))
        conn.commit()
        id_province = cursor.fetchone()
        print('catch id_province', str(id_province))
        cursor.execute('''UPDATE `phong` SET `room_name` = %s, `room_address` = %s, `room_performence` = %s, `room_price` = %s, `id_roomtype` = %s, `id_province` = %s WHERE `room_id` = %s;''', 
        (room_name, room_address, room_performance, room_price, id_type[0],id_province[0], room_id ))
        conn.commit()
        print("Update successful")
        conn.close()
        return redirect ('/manage_rooms')
    except:
        print("Update unsuccessful")
        conn.rollback()
    return redirect(url_for('admin.edit_room', id=room_id))


@admin_blp.route('/delete_room/<id>', methods=['POST', 'GET'])
def delete_room(id):
    conn = connect_db()
    cursor = get_cursor(conn)
    sql = 'update phong set room_isdelete = 0 where room_id = %s'
    cursor.execute(sql, (id,))
    conn.commit()
    return redirect('/manage_rooms')
@admin_blp.route('/enable_room', methods=['POST', 'GET'])
def enable_room():
    id = request.args.getlist('restore')
    print(id)

    conn = connect_db()
    cursor = get_cursor(conn)
    sql = 'update phong set room_isdelete = 1 where room_id in %s'
    cursor.execute(sql, (id,))
    conn.commit()
    return redirect('/manage_rooms')
@admin_blp.route('/add_room')
def add_room():
    return render_template('admin/add_room.html')
@admin_blp.route('/submit_add_room')
def submit_add_room():
    conn = connect_db()
    cursor = get_cursor(conn)
    room_name = request.args.get('room_name')
    room_address = request.args.get('room_address')
    room_performance = request.args.get('room_performance')
    room_type = request.args.get('room_type')
    room_price = request.args.get('room_price')
    room_province = request.args.get('room_province')
    room_image = request.args.getlist('image')
    print(room_type, room_province, room_image)
    
    try:
        sql2 = '''select province_id from tinhthanh where province_name like "%{}%"'''
        cursor.execute(sql2.format(room_province))
        id_province = cursor.fetchone()
        print('catch id_province', str(id_province))
        cursor.execute('''INSERT INTO `phong` VALUES (NULL,%s, %s, %s, %s,%s,%s, "Trống",1) ;''', 
        (room_name, room_address, room_performance, room_price, room_type,id_province[0]))
        conn.commit()
        print("Add successful")
        cursor.execute('select room_id from phong where room_name like "%{}%"'.format(room_name))
        conn.commit()
        room_id = cursor.fetchone()
        for img in room_image:
            item_image = 'Ảnh test' + "/" + img
            cursor.execute('insert into hinhanh values (NULL, %s, %s, 1,1)', (room_id, item_image))
            conn.commit()
            
        conn.close()
        return redirect ('/manage_rooms')
    except:
        print("Update unsuccessful")
        conn.rollback()
    return redirect('/add_room')


@admin_blp.route('/edit_customer/<id>')
def edit_customer(id):
    conn = connect_db()
    cursor = get_cursor(conn)
    try:
        cursor.execute('select * from khachhang where customer_isdelete = 1 and customer_id = %s', (id, ))
        conn.commit()
    except:
        conn.commit()
    row = cursor.fetchone()
    # print(khachhang)
    temp = {}
    if row:
        temp['customer_id'] = row[0]
        temp['first_name'] = row[1]
        temp['last_name'] = row[2]
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

    print(temp)
    return render_template('admin/edit_customer.html', row = temp)

@admin_blp.route('/submit_edit_customer', methods=['GET', 'POST'])
def edit_customer_submit():
    customer_id = request.args.get('customer_id')
    firstname = request.args.get('first_name')
    lastname = request.args.get('last_name')
    gender = request.args.get('optionsRadios')
    phone_number = request.args.get('customer_phone')
    identity = request.args.get('customer_identify')
    address = request.args.get('customer_address')
    birthday = request.args.get('customer_date')
    note = request.args.get('customer_note')
    nation = request.args.get('customer_nation')
    print(birthday)
    conn = connect_db()
    cursor = get_cursor(conn)
    try:
        sql1 =  '''UPDATE khachhang SET `first_name` = %s, `last_name` = %s, `customer_identity`= %s,`customer_date`=%s, `customer_phone` = %s, `customer_address`=%s,`customer_gender`=%s,   `customer_note` = %s, 
                        customer_nation = %s WHERE `customer_id` = %s;'''
        cursor.execute(sql1, (firstname, lastname, identity,birthday, phone_number, address, gender,note, nation, customer_id,))
        conn.commit()
        print('Update khachhang seccuessfully')
        return redirect('/customer')
    except:
        conn.rollback()
    return redirect(url_for('admin.edit_customer', id=customer_id))

@admin_blp.route('/delete_customer/<id>', methods=['POST', 'GET'])
def delete_customer(id):
    conn = connect_db()
    cursor = get_cursor(conn)
    try:
        cursor.execute('update khachhang set customer_isdelete = 0 where customer_id = %s', (id, ))
        conn.commit()
        conn.close()
        print('deleted customer')
    except:
        conn.rollback()
        print('Cant delete customer')
    return redirect('/customer')
@admin_blp.route('/enable_customer', methods=['POST', 'GET'])
def enable_customer():
    conn = connect_db()
    cursor = get_cursor(conn)
    list_id = request.args.getlist('restore')
    print(list_id)
    try:
        cursor.execute('update khachhang set customer_isdelete = 1 where customer_id in %s', (list_id, ))
        conn.commit()
        conn.close()
        print('restored customer')
    except:
        conn.rollback()
        print('Cant restore customer')
    return redirect('/customer')

@admin_blp.route('/submit_booking')
def submit_booking():
    firstname = request.args.get('first_name')
    lastname = request.args.get('last_name')
    identity = request.args.get('customer_identify')
    phone = request.args.get('customer_phone')
    gender = request.args.get('optionsRadios')
    start_time = request.args.get('checkin')
    end_time = request.args.get('checkout')
    province = request.args.get('room_province')
    room = request.args.get('room')
    conn = connect_db()
    cursor = get_cursor(conn)
    id_customer = get_customer_id(cursor, identity)
    
    temp = {}
    temp['first'] = firstname
    temp['last'] = lastname
    temp['identity'] = identity
    temp['phone'] = phone
    temp['gender'] = gender
    temp['start_time'] = start_time
    temp['end_time'] = end_time
    temp['province'] = province
    temp['room'] = room
    print(end_time)
    if id_customer:
        try:
            cursor.execute('select room_id from phong where room_name like "%{}%";'.format(room))
            id_room = cursor.fetchone()
            cursor.execute('INSERT INTO datphong values (NULL, %s, %s, %s, %s, 2,0)', (id_customer, id_room[0], start_time, end_time,))
            conn.commit()
            conn.close()
        except: 
            conn.rollback()
    else:
        try:
            cursor.execute('insert into khachhang values (NULL, %s, %s, NULL, %s, %s, %s, NULL, NULL, NULL, NULL,1)', (firstname, lastname, identity, gender, phone))
            conn.commit()
            cursor.execute('SELECT * FROM khachhang where customer_identity = %s', (identity, ))
            id_customer = cursor.fetchone()[0]
            cursor.execute('select room_id from phong where room_name like "%{}%";'.format(room))
            id_room = cursor.fetchone()[0]
            cursor.execute('INSERT INTO datphong values (NULL, %s, %s, %s, %s, 2,0)', (id_customer, id_room, start_time, end_time,))
            conn.commit()
            conn.close()
        except:
            conn.rollback()
    return redirect(url_for('adview.booking_detail'))
def get_customer_id(cursor, identity):
    sql = '''SELECT * FROM khachhang where customer_identity = %s'''
    cursor.execute(sql, (identity,))
    data = cursor.fetchone()
    if data:
        return data[0]
    else:
        return ''
@admin_blp.route('/submit_bill_purchase/<bill_id>')
def submit_bill_purchase(bill_id):
    conn = connect_db()
    cursor = get_cursor(conn)
    try:
        cursor.execute('UPDATE hoadon set tinhtrang = "Đã thanh toán" where id_bill = %s', (bill_id,))
        conn.commit()
        cursor.execute('''UPDATE phong set phong.status = "Trống" where phong.room_id in (select datphong.room_id 
                        from datphong 
                        inner join hoadon on hoadon.bookroom_id = datphong.bookroom_id and hoadon.id_bill = %s) ''', (bill_id, ))
        conn.commit()
        conn.close()
        flash('Thanh toán thành công!', 'alert alert-success')
        return redirect('/dashboard')
    except:
        conn.rollback()
        conn.close()
        flash('Thanh toán thất bại', 'alert alert-warning')
        return redirect(url_for('adview.detail_bill', bill_id=bill_id))

@admin_blp.route('/convenient')
def convenient():
    pass


@admin_blp.route('/service')
def service():
    pass
