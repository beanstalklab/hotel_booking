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


@adview_blp.route('/manage_rooms')
def room():
    conn = connect_db()
    cursor = get_cursor(conn)
    phong=''
    try:
        cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 1 order by phong.room_id;')
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
    return render_template('admin/room.html', data = final_data)

@adview_blp.route('/room_filter')
def filter():
    conn = connect_db()
    cursor = get_cursor(conn)
    phong=''
    id_filter = request.args.get('id_filter')
    show_option = request.args.get('show_option')
    if show_option == 'hoatdong':
        if id_filter == 'room_id':
            try:
                cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 1  order by phong.room_id')
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
        elif id_filter == 'room_price_up':
            try:
                cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 1  order by phong.room_price ASC')
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
        else:
            try:
                cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province  where phong.room_isdelete = 1 order by phong.room_price DESC')
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
    else:
        if id_filter == 'room_id':
            try:
                cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 0  order by phong.room_id')
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
        elif id_filter == 'room_price_up':
            try:
                cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 0  order by phong.room_price ASC')
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
        else:
            try:
                cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province  where phong.room_isdelete = 0 order by phong.room_price DESC')
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
    conn.close()
    print(id_filter, show_option)
    return render_template('admin/room.html', data = final_data, show_option=show_option, id_filter=id_filter)
