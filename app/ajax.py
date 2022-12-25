from flask import Blueprint, redirect, render_template, request, session, url_for, jsonify, flash
from app.db_utils import connect_db, get_cursor
from datetime import timedelta
from app.sql import *
ajax_blp = Blueprint(
    "ajax", __name__, template_folder='templates/admin', static_folder='static')


@ajax_blp.route("/type_room_ajax",methods=["POST","GET"])
def type_room_ajax():
    conn = connect_db()
    cursor = get_cursor(conn)
    if request.method == 'POST':
        queryString = request.form['queryString']
        print(queryString)
        query = "SELECT * from loaiphong WHERE room_name LIKE '%{}%' LIMIT 10".format(queryString)
        cursor.execute(query)
        loaiphong = cursor.fetchall()
    return jsonify({'htmlresponse': render_template('admin/response/response_roomtype.html', loaiphong=loaiphong)})
@ajax_blp.route("/nation_ajax",methods=["POST","GET"])
def nation_ajax():
    conn = connect_db()
    cursor = get_cursor(conn)
    if request.method == 'POST':
        queryString = request.form['queryString']
        print(queryString)
        query = "SELECT * from quoctich WHERE name LIKE '%{}%' LIMIT 10".format(queryString)
        cursor.execute(query)
        nation =cursor.fetchall()
    return jsonify({'htmlresponse': render_template('admin/response/respone_nation.html', nation=nation)})
@ajax_blp.route("/room_ajax",methods=["POST","GET"])
def room_ajax():
    conn = connect_db()
    cursor = get_cursor(conn)
    if request.method == 'POST':
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        province = request.form['province']
        print(checkin, checkout, province)
        query = """SELECT phong.room_id, phong.room_name, datphong.time_start from phong inner join datphong on datphong.room_id = phong.room_id 
    where date(datphong.time_start) > '%s' or date(datphong.time_end) < '%s'""".format(checkout, checkin)
        cursor.execute(query)
        room =cursor.fetchall()
        print(room)
    return jsonify({'htmlresponse': render_template('admin/response/respone_room.html', room=room)})
@ajax_blp.route("/ajaxlivesearch",methods=["POST","GET"])
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

@ajax_blp.route("/ajaxpost",methods=["POST","GET"])
def ajaxpost():
    conn = connect_db()
    cursor = get_cursor(conn)
    if request.method == 'POST':
        queryString = request.form['queryString']
        print(queryString)
        query = "SELECT * from tinhthanh WHERE province_name LIKE '%{}%' LIMIT 10".format(queryString)
        cursor.execute(query)
        tinhthanh = cursor.fetchall()
    return jsonify({'htmlresponse': render_template('admin/response/response_province.html', tinhthanh=tinhthanh)})
