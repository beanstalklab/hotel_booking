from flask import render_template, session
from app import app

from app.db_utils import connect_db, get_cursor


@app.route('/profile', methods=['GET'])
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