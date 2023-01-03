import math
import os
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, send_from_directory, jsonify
from app.db_utils import connect_db, get_cursor
from app.config import HOTEL_IMAGE, USER_IMAGE, BLOG_IMAGE
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
        for row in hoatdong:
            temp = {}
            temp['room_name'] = row[0]
            temp['time_start'] = row[1]
            temp['time_end'] = row[2]
            temp['status'] = row[3]
            temp['id_bill'] = row[4]
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

@main_blp.route('/blog_customer/<account_id>')
def blog_customer(account_id):
    conn = connect_db()
    cursor = get_cursor(conn)
    posts=''
    cursor.execute('select * from baiviet where account_id = %s and status = 0', (account_id,))
    data = cursor.fetchall()
    posts = []
    for row in data:
        temp = {}
        temp['post_id'] = row[0]
        temp['title'] = row[2]
        temp['body'] = row[3]
        temp['time'] = row[4]
        cursor.execute('select * from blog_image where post_id = %s', (row[0],))
        img_list = cursor.fetchall()
        final_img = []
        for img in img_list:
            if img:
                final_img.append(img[2])
        posts.append((temp, final_img))
    # try:

    #     cursor.execute('select * from baiviet where account_id = %s where status = 0', (account_id,))
    #     data = cursor.fetchall()
    #     posts = []
    #     for row in data:
    #         temp = {}
    #         temp['post_id'] = row[0]
    #         temp['title'] = row[2]
    #         temp['body'] = row[3]
    #         temp['time'] = row[4]
    #         cursor.execute('select * from blog_image where post_id = %s', (row[0],))
    #         img_list = cursor.fetchall()
    #         final_img = []
    #         for img in img_list:
    #             if img:
    #                 index = img[2].index('/')
    #                 img = {'folder': img[2][0:index],
    #                         'name': img[2][index+1:]}
    #                 final_img.append(img)
    #         posts.append((temp, final_img))
    # except:
    #     conn.rollback()
    return render_template('user/blog_user.html', blogs = posts)

@main_blp.route('/write_blog/<account_id>')
def write_blog(account_id):

    title = request.args.get('title')
    body = request.args.get('body')
    image_file = request.args.getlist('file')
    conn = connect_db()
    cursor = get_cursor(conn)
    print(body, title, image_file, account_id)
    msg = ''
    try:
        cursor.execute('insert into baiviet (`account_id`,`title`, `body`) values(%s,%s, %s)', (account_id, title, body))
        conn.commit()
        print('add thanh cong')
        cursor.execute('select * from baiviet where account_id = {} and title = "{}"'.format(account_id, title))
        post_id = cursor.fetchone()
        print('post_id:', post_id)
        for image in image_file:
            blog_image = str(image)
            cursor.execute('insert into blog_image (`post_id`,`img_link`) values(%s,%s)', (post_id[0], blog_image))
            conn.commit()
        conn.close()
        print('Thanh cong')
        flash('tạo bài viết thành công')

        return redirect(url_for('view.blog_customer', account_id = account_id))

    except:
        print('error')
        conn.rollback()
        conn.close()
        flash('Tạo bài viết không thành công')
    return redirect(url_for('view.blog_customer', account_id = account_id))

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
        cursor.execute('''select avg(danhgia.rating) from danhgia
                            where danhgia.room_id = %s
                            GROUP BY danhgia.room_id; ''', (room_id,))
        rating = cursor.fetchone()
        if rating:
            temp_data['rating'] = math.ceil(rating[0])
        else:
            temp_data['rating'] = 3
        print(rating)
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
    
    cursor.execute('''select binhluan.id, binhluan.room_id, taikhoan.user_name, binhluan.post, binhluan.date_post, taikhoan.account_id 
                from binhluan
                inner join taikhoan on taikhoan.account_id = binhluan.user_id 
                where binhluan.room_id  = %s order by binhluan.date_post desc limit 5''', (room_id))
    posts = cursor.fetchall()
    post_list = []
    if posts:
        for row in posts:
            temp = {}
            temp['post_id'] = row[0]
            temp['room_id'] = row[1]
            temp['user_name'] = row[2]
            temp['post'] = row[3]
            temp['date_post'] = row[4]
            temp['user_id'] = row[5]
            post_list.append(temp)
    conn.close()
    
    return render_template('detail.html', data=data, msg=msg, img=list_img,num=number_img, mota=mota, loaiphong=loaiphong, province=province, post_list=post_list)
@main_blp.route('/full_detail_comment/<room_id>', methods=['GET', 'POST'])
def full_detail_comment(room_id):
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
    
    cursor.execute('''select binhluan.id, binhluan.room_id, taikhoan.user_name, binhluan.post, binhluan.date_post, taikhoan.account_id 
                from binhluan
                inner join taikhoan on taikhoan.account_id = binhluan.user_id where room_id  = %s order by binhluan.date_post desc''', (room_id))
    posts = cursor.fetchall()
    post_list = []
    if posts:
        for row in posts:
            temp = {}
            temp['post_id'] = row[0]
            temp['room_id'] = row[1]
            temp['user_name'] = row[2]
            temp['post'] = row[3]
            temp['date_post'] = row[4]
            temp['user_id'] = row[5]
            post_list.append(temp)
    conn.close()
    
    return render_template('detail.html', data=data, msg=msg, img=list_img,num=number_img, mota=mota, loaiphong=loaiphong, province=province, post_list=post_list, full='full')
@main_blp.route('/delete_comment/<room_id>/<post_id>')
def delete_comment(post_id, room_id):
    conn = connect_db()
    cursor = get_cursor(conn)
    try:
        cursor.execute('delete from binhluan where id = %s and room_id = %s', (post_id, room_id, ))
        conn.commit()
    except:
        conn.rollback()
    conn.close()
    return redirect(url_for('view.detail', room_id=room_id))
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
        cursor.execute('''select avg(danhgia.rating) from danhgia
                            where danhgia.room_id = %s
                            GROUP BY danhgia.room_id; ''', (room_id,))
        rating = cursor.fetchone()
        if rating:
            temp_data['rating'] = math.ceil(rating[0])
        else:
            temp_data['rating'] = 3
        print(rating)
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
                    print(img)
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
def write_post(id_room):
    conn = connect_db()
    cursor = get_cursor(conn)
    post = request.args.get('body')
    star = request.args.get('star')
    user_id = session['id']
    if post:
        try:
            cursor.execute('insert into binhluan(`room_id`, `user_id`, `post`) values ({}, {},"{}")'.format(id_room,user_id,post))
            conn.commit()
        except:
            conn.rollback()
    conn.close()
    if star:
        conn = connect_db()
        cursor = get_cursor(conn)
        cursor.execute('''select * from danhgia where account_id = %s and room_id = %s;''', (user_id, id_room,))
        rating = cursor.fetchone()
        print(rating)
        if rating:
            try:
                cursor.execute('''delete from danhgia where `account_id` = {} and `room_id` = {};'''.format(user_id, id_room))
                cursor.execute('insert into danhgia values (%s, %s, %s)', (id_room, user_id, star,))
                conn.commit()
                print('update thanh cong')
            except:
                print('khong the update')
                conn.rollback()
        else:
            try:
                cursor.execute('insert into danhgia values (%s, %s, %s)', (id_room, user_id, star,))
                conn.commit()
            except:
                conn.rollback()
        conn.close()
    
    print(id_room,user_id,post, star)
    return redirect(url_for('view.detail', room_id=id_room))

@main_blp.route('/folder_image/<folder>/<name>')
def image_file(folder, name):
    return send_from_directory(os.path.join(HOTEL_IMAGE, folder), name)
@main_blp.route('/user_image/<name>')
def user_image(name):
    return send_from_directory(USER_IMAGE, name)

@main_blp.route('/blog_image/<name>')
def blog_image(name):
    return send_from_directory(BLOG_IMAGE, name)