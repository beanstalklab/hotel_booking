import os
from flask import Blueprint, redirect, render_template, request, session, url_for, send_from_directory
from app.db_utils import connect_db, get_cursor
from app.config import HOTEL_IMAGE
main_blp = Blueprint(
    "view", __name__, template_folder='templates', static_folder='static')


@main_blp.route('/')
@main_blp.route('/home', methods=['GET'])
def home():

    return render_template('home.html')


@main_blp.route('/profile', methods=['GET'])
def profile():
    msg = {}
    id_account = session['id']
    conn = connect_db()
    cursor = get_cursor(conn)
    cursor.execute(
        'select * from taikhoan where taikhoan.account_id = % s;', (id_account,))
    info = cursor.fetchone()
    info = {'account_id': info[0], 'email': info[1], 'user_name': info[2],
            'password': info[3], 'role_id': info[4], 'account_isdelete': info[5]}
    cursor.execute(
        'select * from khachhang where khachhang.account_id = %s', (id_account, ))
    khachhang = cursor.fetchone()
    conn.commit()
    khachhang = {'customer_id': khachhang[0], 'customer_name': khachhang[1], 'account_id': khachhang[2], 'customer_identity': khachhang[3], 'customer_gender': khachhang[4],
                 'customer_phone': khachhang[5], 'customer_address': khachhang[6], 'customer_date': khachhang[7], 'customer_note': khachhang[8], 'customer_isdelete': khachhang[9]}
    return render_template('user/profile.html', info=info, msg=msg, khachhang=khachhang)


@main_blp.route('/room', methods=['GET', 'POST'])
def room():
    msg = ''
    conn = connect_db()
    cursor = get_cursor(conn)
    cursor.execute('SELECT * FROM khachsan')
    data = cursor.fetchone()
    index = data[2].index('/')
    data = {'hotel_id': data[0], 'hotel_province': data[1], 'hotel_folder': data[2][0:index], 'hotel_image': data[2][index+1:], 'hotel_code': data[3],
            'hotel_name': data[4], 'hotel_address': data[5], 'hotel_intro': data[6], 'hotel_isdelete': data[7]}
    conn.commit()
    return render_template('rooms.html', data=data, msg=msg)
@main_blp.route('/detail', methods=['GET', 'POST'])
def detail():
    msg = ''
    conn = connect_db()
    cursor = get_cursor(conn)
    cursor.execute('SELECT * FROM khachsan')
    data = cursor.fetchone()
    index = data[2].index('/')
    data = {'hotel_id': data[0], 'hotel_province': data[1], 'hotel_folder': data[2][0:index], 'hotel_image': data[2][index+1:], 'hotel_code': data[3],
            'hotel_name': data[4], 'hotel_address': data[5], 'hotel_intro': data[6], 'hotel_isdelete': data[7]}
    conn.commit()
    return render_template('detail.html', data=data, msg=msg)
@main_blp.route('/folder_image/<folder>/<name>')
def image_file(folder, name):
    return send_from_directory(os.path.join(HOTEL_IMAGE, folder), name)
