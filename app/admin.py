from flask import Blueprint, redirect, render_template, request, session, url_for, jsonify, flash
from app.db_utils import connect_db, get_cursor
from datetime import timedelta
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
    room_image = request.args.get('image')
    room_image = os.path.join('Ảnh test', room_image)
    print(room_type, room_province, room_image)
    
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
        cursor.execute('''INSERT INTO `phong` VALUES (NULL,%s, %s, %s, %s,%s,%s,1) ;''', 
        (room_name, room_address, room_performance, room_price, id_type[0],id_province[0]))
        conn.commit()
        print("Add successful")
        cursor.execute('select room_id from phong where room_name like "%{}%"'.format(room_name))
        conn.commit()
        room_id = cursor.fetchone()
        cursor.execute('insert into hinhanh values (NULL, %s, %s, 1,1)', (room_id, room_image))
        conn.commit()
        conn.close()
        return redirect ('/manage_rooms')
    except:
        print("Update unsuccessful")
        conn.rollback()
    return redirect('/add_room')


@admin_blp.route('/customer')
def customer():
    pass


@admin_blp.route('/convenient')
def convenient():
    pass


@admin_blp.route('/service')
def service():
    pass
