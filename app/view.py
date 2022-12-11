from flask import Blueprint, redirect, render_template, request, session, url_for
from app.db_utils import connect_db, get_cursor

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
    cursor.execute(
        'select * from khachhang where khachhang.account_id = %s', (id_account, ))
    khachhang = cursor.fetchone()
    conn.commit()
    return render_template('profile.html', info=info, msg=msg, khachhang=khachhang)


@main_blp.route('/room', methods=['GET', 'POST'])
def room():
    msg = ''
    conn = connect_db()
    cursor = get_cursor(conn)
    cursor.execute('SELECT * FROM khachsan')
    data = cursor.fetchone()
    data = {'hotel_id': data[0], 'hotel_province': data[1], 'hotel_image': data[2], 'hotel_code': data[3],
            'hotel_name': data[4], 'hotel_address': data[5], 'hotel_intro': data[6], 'hotel_isdelete': data[7]}
    conn.commit()
    return render_template('room.html', data=data, msg=msg)
