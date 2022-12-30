import math
import os
from flask import Blueprint, redirect, render_template, request, session, url_for, send_from_directory, jsonify
from app.db_utils import connect_db, get_cursor
from app.config import HOTEL_IMAGE, USER_IMAGE
from app.config import HOTEL_IMAGE, USER_IMAGE
from app.sql import *
main_blp = Blueprint(
    "view", __name__, template_folder='templates', static_folder='static')


@main_blp.route('/')
@main_blp.route('/home', methods=['GET'])
def home():
    conn = connect_db()
    cursor = get_cursor(conn)
    final_data = []
    try:
        cursor.execute('SELECT * FROM phong where phong.room_isdelete = 1 ORDER BY room_price ASC LIMIT 9 ')
        conn.commit()
    except:
        print('cannot get data')

    datas = cursor.fetchall()
    print(datas)
    conn.close()
    for data in datas:
        temp_data = {'room_id': data[0], 'room_name': data[1], 'room_address': data[2],
                     'room_performance': data[3], 'room_price': data[4], 'id_typeroom': data[5], 'room_isdelete': data[6]}
        room_id = data[0]
        conn = connect_db()
        cursor = get_cursor(conn)
        try:
            cursor.execute(
                'SELECT image_link, image_rank from hinhanh where room_id = %s', (room_id,))
            conn.commit()
        except:
            print('error image')
            # conn.rollback()
        img = cursor.fetchone()
        print(img)
        idx = img[0].index('/')
        img = {'folder': img[0][0:idx],
            'name': img[0][idx+1:], 'rank': img[1]}
        final_data.append((temp_data, img))
    conn.close()
    return render_template('home.html', data=final_data)

@main_blp.route('/profile', methods=['GET'])
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
    return render_template('user/profile.html', info=info,khachhang=khachhang,msg=msg, lichsu=lichsu,img=img)

@main_blp.route('/page', defaults={'page': 1})
@main_blp.route('/page/<int:page>', methods=['GET', 'POST'])
def room(page):
    limit = 9
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
    
    total_row = cursor.rowcount
    total_page = math.ceil(total_row/limit)

    try:
        cursor.execute(
        'SELECT * FROM phong where room_isdelete = 1 ORDER BY room_id ASC LIMIT %s OFFSET %s', (limit, offset,))
        conn.commit()
    except:
        conn.rollback()
    datas = cursor.fetchall()
    final_data = []
    
    for data in datas:
        temp_data = {'room_id': data[0], 'room_name': data[1], 'room_address': data[2],
                     'room_performance': data[3], 'room_price': data[4], 'id_typeroom': data[5], 'room_isdelete': data[6]}
        room_id = int(data[0])
        try:
            cursor.execute(
                'SELECT image_link, image_rank from hinhanh where room_id = % s;', (room_id,))
            conn.commit()
        except:
            conn.rollback()
        img = cursor.fetchone()
        
        if img:
            index = img[0].index('/')
            img = {'folder': img[0][0:index],
                'name': img[0][index+1:], 'rank': img[1]}
            final_data.append((temp_data, img))
        else:
            continue
    conn.close()
    return render_template('room.html', data=final_data, page=total_page, next=next, prev=prev)
    


@main_blp.route('/detail/<room_id>', methods=['GET', 'POST'])
def detail(room_id):
    msg = ''
    conn = connect_db()
    cursor = get_cursor(conn)
    try:
        cursor.execute(
            'SELECT * FROM phong where room_id = %s', (room_id,))
        conn.commit()
    except:
        conn.rollback()
    data = cursor.fetchone()

    data = {'room_id': data[0], 'room_name': data[1], 'room_address': data[2],
                    'room_performance': data[3], 'room_price': data[4], 'id_typeroom': data[5], 'room_province': data[6]}
    try:
        cursor.execute(
            'SELECT image_link, image_rank from hinhanh where room_id = % s;', (room_id,))
        conn.commit()
    except:
        conn.rollback()
    number_img = cursor.rowcount
    imgs = cursor.fetchall()
    try:
        cursor.execute(
            'SELECT province_name from tinhthanh where province_id = % s;', (data['room_province'],))
        conn.commit()
    except:
        conn.rollback()
    province = cursor.fetchone()
    list_img = []
    for img in imgs:

        index = img[0].index('/')
        img = {'folder': img[0][0:index],
            'name': img[0][index+1:], 'rank': img[1]}
        list_img.append(img)
    try: 
        cursor.execute('''select tiennghi.ten_dich_vu, ql_tiennghi.soluong from ql_tiennghi 
                        inner join tiennghi on tiennghi.id = ql_tiennghi.id_tiennghi where ql_tiennghi.id_phong = %s''', (room_id, ))
        mota = cursor.fetchall()
        cursor.execute('''select room_note from loaiphong where room_id = %s''', (room_id, ))
        loaiphong = cursor.fetchone()
        print(mota, loaiphong, province)
    except:
        print('errro')
    
    cursor.execute('select * from binhluan where room_id  = %s')
    conn.close()
    
    return render_template('detail.html', data=data, msg=msg, img=list_img,num=number_img, mota=mota, loaiphong=loaiphong, province=province)


@main_blp.route('/page/filter', defaults={'page': 1})
@main_blp.route('/page/filter/<int:page>', methods=['GET', 'POST'])
def room_filter(page):
    id_filter = request.args.get('filter')
    
    if id_filter:
        # list_filter = {'price_down': ['room_price', 'DESC'], 'price_up': ['room_price', 'ASC'], 'most_popular':'room_id'}
        limit = 9
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
            cursor.execute('SELECT * FROM phong where room_isdelete = 1')
            conn.commit()
        except:
            conn.rollback()
        
        total_row = cursor.rowcount
        total_page = math.ceil(total_row/limit)
        if id_filter == 'price_up':

            try:
                cursor.execute('SELECT * FROM phong where room_isdelete = 1 ORDER BY room_price ASC LIMIT {} OFFSET {}'.format(limit, offset,))
                conn.commit()
            except:
                conn.rollback()
        elif id_filter == 'price_down':
            try:
                cursor.execute('SELECT * FROM phong where room_isdelete = 1 ORDER BY room_price DESC LIMIT {} OFFSET {}'.format(limit, offset,))
                conn.commit()
            except:
                conn.rollback()
        else:
            try:
                cursor.execute(
                    'SELECT * FROM phong where room_isdelete = 1 ORDER BY room_id ASC LIMIT {} OFFSET {}'.format(limit, offset))
                conn.commit()
            except:
                conn.rollback()
        
    datas = cursor.fetchall()
    final_data = []
    
    for data in datas:
        temp_data = {'room_id': data[0], 'room_name': data[1], 'room_address': data[2],
                     'room_performance': data[3], 'room_price': data[4], 'id_typeroom': data[5], 'room_isdelete': data[6]}
        room_id = int(data[0])
        try:
            cursor.execute(
                'SELECT image_link, image_rank from hinhanh where room_id = % s;', (room_id,))
            conn.commit()
        except:
            conn.rollback()
        img = cursor.fetchone()
        
        if img:
            index = img[0].index('/')
            img = {'folder': img[0][0:index],
                'name': img[0][index+1:], 'rank': img[1]}
            final_data.append((temp_data, img))
        else:
            continue
    conn.close()
    return render_template('room.html', data=final_data, page=total_page, next=next, prev=prev,id_filter=id_filter)
@main_blp.route('/filter_local')
def filter_local():
    conn = connect_db()
    cursor = get_cursor(conn)
    room_province = request.args.get('input-search')
    sql2 = '''select province_id from tinhthanh where province_name like "%{}%"'''
    cursor.execute(sql2.format(room_province))
    conn.commit()
    id_province = cursor.fetchone()
    if id_province:
        print(id_province[0])
        try:
            cursor.execute(
                'SELECT * FROM phong where room_isdelete = 1 and id_province = {} ORDER BY room_id ASC '.format(id_province[0]))
            conn.commit()
            print('select succeed')
            row_count = cursor.rowcount
            datas = cursor.fetchall()
            final_data = []
            conn.close()
            for data in datas:
                conn = connect_db()
                cursor = get_cursor(conn)
                temp_data = {'room_id': data[0], 'room_name': data[1], 'room_address': data[2],
                            'room_performance': data[3], 'room_price': data[4], 'id_typeroom': data[5], 'room_isdelete': data[6]}
                room_id = int(data[0])
                try:
                    cursor.execute(
                        'SELECT image_link, image_rank from hinhanh where room_id = % s;', (room_id,))
                    
                except:
                    conn.rollback()
                img = cursor.fetchone()
                if img:
                    index = img[0].index('/')
                    img = {'folder': img[0][0:index],
                        'name': img[0][index+1:], 'rank': img[1]}
                    final_data.append((temp_data, img))
                else:
                    continue
                conn.close()
            return render_template('room.html', data=final_data,  id_filter='most_popular', row_count=row_count)
        except:
            conn.rollback()
            msg = 'We dont have that data'
            return render_template('room.html', data='final_data',  id_filter='most_popular', msg=msg, row_count=0)
    msg = 'We dont have that data'
    return render_template('room.html', data='',  id_filter='most_popular', msg=0)
@main_blp.route('/write_post/<id_room>')
def write_post(id):
    conn = connect_db()
    cursor = get_cursor(conn)
    post = request.args.get('body')
    cursor.execute('insert into binhluan(NULL, {}, {},NULL)'.format(id, post))
    return redirect(url_for('view.detail', room_id=id))
@main_blp.route('/folder_image/<folder>/<name>')
def image_file(folder, name):
    return send_from_directory(os.path.join(HOTEL_IMAGE, folder), name)
@main_blp.route('/user_image/<name>')
def user_image(name):
    return send_from_directory(USER_IMAGE, name)