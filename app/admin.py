import re
from flask import Blueprint, redirect, render_template, request, session, url_for, jsonify
from app.db_utils import connect_db, get_cursor
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from app.sql import *
admin_blp = Blueprint(
    "admin", __name__, template_folder='templates/admin', static_folder='static')


@admin_blp.route('/home')
def admin_home():
    return render_template('admin_home.html')

@admin_blp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('auth.login'))
@admin_blp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html', title='Dashboard')


@admin_blp.route('/manage_rooms')
def room():
    # conn = connect_db()
    # cursor = get_cursor(conn)
    # phong=''
    # try:
    #     cursor.execute('select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 1 order by phong.room_id;')
    #     conn.commit()
    #     phong = cursor.fetchall()
    # except:
    #     conn.rollback()
    # final_data = []
    # for row in phong:
    #     temp = {}
    #     temp['room_id'] = row[0]
    #     temp['room_name'] = row[1]
    #     temp['room_address'] = row[2]
    #     temp['room_performance'] = row[3]
    #     temp['room_price'] = row[4]
    #     temp['room_type'] = row[5]
    #     temp['room_province'] = row[6]
    #     final_data.append(temp)
    # conn.close()
    # print(final_data)
    # return render_template('filter.html', data = final_data)
    return render_template('filter.html')
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
    conn = connect_db()
    cursor = get_cursor(conn)
    if request.method  == 'POST':
        room_name = request.form['room_name']
        room_address = request.form['room_address']
        room_performance = request.form['room_performance']
        room_type = request.form['room_type']
        room_price = request.form['room_price']
        room_province = request.form['room_province']
        try:
            cursor.execute('''UPDATE `phong` SET room_name = %s, room_address = %s, room_performence = %s, room_price = %s, id_roomtype = %s, id_province = %s WHERE `phong`.`room_id` = %s;''', (room_name, room_address, room_performance, room_price, room_type,room_province, id, ))
            conn.commit()
            print("Update successful")
        except:
            print("Update unsuccessful", room_province, room_type)
            conn.rollback()
        conn.close()
        return redirect(url_for('admin.room'))
    else:
        print('error')
    return render_template('admin/edit_room.html', row=temp)

@admin_blp.route("/ajaxlivesearch",methods=["POST","GET"])
def ajaxlivesearch():
    conn = connect_db()
    cur = get_cursor(conn)
    if request.method == 'POST':
        search_word = request.form['query']
        print(search_word)
        if search_word == '':
            cur.execute('select phong.room_id, room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 1 order by phong.room_id;')
            room = cur.fetchall()
        else:    
            query = '''select phong.room_id, room_address, room_performence, room_price, loaiphong.room_name as room_type ,province_name from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province 
WHERE room_address LIKE %s OR room_performence LIKE %s OR loaiphong.room_name LIKE %s  OR  province_name like %s ORDER BY phong.room_id DESC LIMIT 20''', (search_word,search_word, search_word, search_word, )
            cur.execute(query)
            numrows = int(cur.rowcount)
            room = cur.fetchall()
            print(numrows)
    final_data = []
    for row in room:
        temp = {}
        temp['room_id'] = row[0]
        temp['room_name'] = row[1]
        temp['room_address'] = row[2]
        temp['room_performance'] = row[3]
        temp['room_price'] = row[4]
        temp['room_type'] = row[5]
        # temp['room_province'] = row[6]
        final_data.append(temp)
    return jsonify({'htmlresponse': render_template('admin/room.html', room=room)})

@admin_blp.route('/customer')
def customer():
    pass


@admin_blp.route('/convenient')
def convenient():
    pass


@admin_blp.route('/service')
def service():
    pass
