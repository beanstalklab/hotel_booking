import datetime
import math
from datetime import datetime
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify,
    flash,
)
from app.db_utils import connect_db, get_cursor
from datetime import timedelta
from app.sql import *

adview_blp = Blueprint(
    "adview", __name__, template_folder="templates/admin", static_folder="static"
)


@adview_blp.route("/home")
def admin_home():
    return render_template("admin_home.html")


@adview_blp.route("/index")
def index():
    return render_template("index.html")


@adview_blp.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    session.pop("email", None)
    return redirect(url_for("auth.login"))


@adview_blp.route("/dashboard")
def dashboard():
    search_text = request.args.get("search_text")
    print(search_text)
    try:
        temp = search_text.lower()
        conn = connect_db()
        cursor = get_cursor(conn)
        
        cursor.execute(
            """select hoadon.id_bill, concat(khachhang.first_name," ", khachhang.last_name), phong.room_id, hoadon.total_money, hoadon.tinhtrang
                        from hoadon 
                        inner join datphong on datphong.bookroom_id = hoadon.bookroom_id
                        inner join khachhang on khachhang.customer_id = datphong.customer_id
                        inner join phong on datphong.room_id = phong.room_id
                        where hoadon.id_bill like "%{}%" or LOWER(phong.room_name) like "%{}%" or LOWER(khachhang.first_name) like "%{}%" or LOWER(khachhang.last_name) like "%{}%";
        """.format(
                temp, temp, temp, temp
            )
        )
        data = cursor.fetchall()
        final_data = []
        for row in data:
            temp = {}
            temp["bill_id"] = row[0]
            temp["customer_name"] = row[1]
            temp["room_id"] = row[2]
            temp["total_money"] = row[3]
            temp["tinhtrang"] = row[4]
            final_data.append(temp)
        return render_template(
            "admin/dashboard.html",
            title="Dashboard",
            data=final_data,
            search_text=search_text,
        )
    except:
        conn = connect_db()
        cursor = get_cursor(conn)
        cursor.execute(
            """select hoadon.id_bill, concat(khachhang.first_name," ", khachhang.last_name), phong.room_id, hoadon.total_money, hoadon.tinhtrang
                        from hoadon 
                        inner join datphong on datphong.bookroom_id = hoadon.bookroom_id
                        inner join khachhang on khachhang.customer_id = datphong.customer_id
                        inner join phong on datphong.room_id = phong.room_id
                        order by hoadon.time_commit desc;
        """
        )
        data = cursor.fetchall()
        final_data = []
        for row in data:
            temp = {}
            temp["bill_id"] = row[0]
            temp["customer_name"] = row[1]
            temp["room_id"] = row[2]
            temp["total_money"] = row[3]
            temp["tinhtrang"] = row[4]
            final_data.append(temp)
        cursor.execute(''' select sum(hoadon.total_money) from hoadon where hoadon.tinhtrang = "Đã thanh toán";
        ''')
        total_money = cursor.fetchone()
        conn.close()
        return render_template(
            "admin/dashboard.html",
            title="Dashboard",
            data=final_data,
            search_text=search_text,
            total_money = total_money[0]

        )


def get_date(dates):
    temp = dates.split("-")
    return datetime.date(int(temp[2]), int(temp[0]), int(temp[1]))


@adview_blp.route("/detail_bill/<bill_id>")
def detail_bill(bill_id):
    conn = connect_db()
    cursor = get_cursor(conn)
    cursor.execute(
        """select khachhang.customer_id, concat(khachhang.first_name," ", khachhang.last_name),khachhang.customer_identity, hoadon.total_money, hoadon.tinhtrang
                    from khachhang 
                    inner join datphong on datphong.customer_id = khachhang.customer_id
                    inner join hoadon on hoadon.bookroom_id = datphong.bookroom_id
                    where hoadon.id_bill = %s""",
        (bill_id,),
    )
    khachhang = cursor.fetchone()
    cursor.execute(
        """select phong.room_id, phong.room_name, phong.room_address, tinhthanh.province_name, datphong.time_start, datphong.time_end, loaiphong.room_name, phong.room_price
                    from phong 
                    inner join datphong on datphong.room_id = phong.room_id
                    inner join hoadon on hoadon.bookroom_id = datphong.bookroom_id
                    inner join tinhthanh on tinhthanh.province_id = phong.id_province
                    inner join loaiphong on loaiphong.room_id = phong.id_roomtype
                    where hoadon.id_bill = %s
                    """,
        (bill_id,),
    )
    phong = cursor.fetchone()
    # checkin = phong[4]
    # checkout = phong[5]
    # print(checkout - checkin)
    cursor.execute(
        """ select dichvu.service_name, dichvu.service_price, ql_dichvu.soluong from ql_dichvu 
                    inner join datphong on datphong.bookroom_id = ql_dichvu.id_dangky
                    inner join dichvu on dichvu.service_id = ql_dichvu.id_dichvu
                    inner join hoadon on hoadon.bookroom_id = datphong.bookroom_id
                    where hoadon.id_bill = %s;""",
        (bill_id,),
    )
    dichvu = cursor.fetchall()
    print(khachhang)
    print(phong)
    print(dichvu)
    return render_template(
        "bill_detail.html",
        hoadon=bill_id,
        dichvu=dichvu,
        khachhang=khachhang,
        phong=phong,
    )


@adview_blp.route("/profile")
def profile():
    msg = {}
    id_account = session["id"]
    conn = connect_db()
    cursor = get_cursor(conn)
    try:
        cursor.execute(user["get_account_info"] % (id_account,))
        conn.commit()
    except:
        conn.rollback()
    info = cursor.fetchone()
    info = {
        "account_id": info[0],
        "email": info[1],
        "user_name": info[2],
        "password": info[3],
        "role_id": info[4],
        "account_isdelete": info[5],
    }
    try:
        cursor.execute(user["get_customer_info"] % (id_account,))
        conn.commit()
    except:
        conn.rollback()
    khachhang = cursor.fetchone()

    if khachhang:
        session["customer_id"] = khachhang[0]
        khachhang = {
            "customer_id": khachhang[0],
            "first_name": khachhang[1],
            "last_name": khachhang[2],
            "account_id": khachhang[3],
            "customer_identity": khachhang[4],
            "customer_gender": khachhang[5],
            "customer_phone": khachhang[6],
            "customer_address": khachhang[7],
            "customer_date": khachhang[8],
            "customer_note": khachhang[10],
            "customer_nation": khachhang[9],
        }
    try:
        cursor.execute(user["info_action"] % (session["customer_id"],))
        conn.commit()
    except:
        conn.rollback()

    # print(session['customer_id'])
    hoatdong = cursor.fetchall()
    lichsu = []
    if hoatdong:
        trangthai = {
            "0": "Đã thanh toán",
            "1": "Đã đặt",
            "2": "Chờ duyêt",
            "3": "Đã hủy",
        }
        for row in hoatdong:
            temp = {}
            temp["room_name"] = row[0]
            temp["time_start"] = row[1]
            temp["time_end"] = row[2]
            temp["status"] = trangthai[str(row[3])]
            lichsu.append(temp)
    try:
        cursor.execute("select * from user_image where user_id = %s", (id_account,))
        conn.commit()
    except:
        conn.rollback()
    img = cursor.fetchone()
    # print(img[2])
    if img:
        index = img[2].index("/")
        img = {"folder": img[2][0:index], "name": img[2][index + 1 :]}
    print(img)
    conn.close()
    return render_template(
        "admin/profile.html",
        info=info,
        khachhang=khachhang,
        msg=msg,
        lichsu=lichsu,
        img=img,
    )


@adview_blp.route("/manage_rooms", defaults={"page": 1})
@adview_blp.route("/manage_rooms/<int:page>", methods=["GET", "POST"])
def room(page):
    search_text = request.args.get("search_text")
    print(search_text)
    if search_text:
        temp = search_text.lower()

        limit = 5
        offset = page * limit - limit
        conn = connect_db()
        cursor = get_cursor(conn)
        try:
            cursor.execute(
                """select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province 
            where phong.room_isdelete = 1 and LOWER(phong.room_name) like "%{}%" or LOWER(tinhthanh.province_name) like "%{}%" or LOWER(phong.room_address) like "%{}%" order by phong.room_id LIMIT {} OFFSET {};""".format(
                    temp, temp, temp, limit, offset
                )
            )
            conn.commit()
            phong = cursor.fetchall()
        except:
            conn.rollback()
        total_row = cursor.rowcount
        total_page = math.ceil(total_row / limit)

        next = page + 1
        prev = page - 1

        conn = connect_db()
        cursor = get_cursor(conn)
        phong = ""
        try:
            cursor.execute(
                """select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name,  phong.status  from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province 
            where phong.room_isdelete = 1 and LOWER(phong.room_name) like "%{}%" or LOWER(tinhthanh.province_name) like "%{}%" or LOWER(phong.room_address) like "%{}%" order by phong.room_id LIMIT {} OFFSET {};""".format(
                    temp, temp, temp, limit, offset
                )
            )
            conn.commit()
            phong = cursor.fetchall()
        except:
            conn.rollback()
        print(phong, temp)
        final_data = []
        for row in phong:
            temp = {}
            temp["room_id"] = row[0]
            temp["room_name"] = row[1]
            temp["room_address"] = row[2]
            temp["room_performance"] = row[3]
            temp["room_price"] = row[4]
            temp["room_type"] = row[5]
            temp["room_province"] = row[6]
            temp["room_isdelete"] = "Active"
            temp["status"] = row[7]
            final_data.append(temp)
        conn.close()
        print(final_data)
        return render_template(
            "admin/room.html",
            data=final_data,
            page=total_page,
            next=next,
            prev=prev,
            search_text=search_text,
            amount=total_row,
        )
    else:
        limit = 5
        offset = page * limit - limit
        conn = connect_db()
        cursor = get_cursor(conn)
        try:
            cursor.execute("SELECT * FROM phong where room_isdelete = 1")
            conn.commit()
        except:
            conn.rollback()
        total_row = cursor.rowcount
        total_page = math.ceil(total_row / limit)

        next = page + 1
        prev = page - 1
        try:
            cursor.execute("SELECT * FROM phong")
            conn.commit()
        except:
            conn.rollback()
        conn.close()
        total_row = cursor.rowcount
        total_page = math.ceil(total_row / limit)

        conn = connect_db()
        cursor = get_cursor(conn)
        phong = ""
        try:
            cursor.execute(
                'select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name,  phong.status from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 1 order by phong.room_id LIMIT %s OFFSET %s;',
                (
                    limit,
                    offset,
                ),
            )
            conn.commit()
            phong = cursor.fetchall()
        except:
            conn.rollback()
        final_data = []
        for row in phong:
            temp = {}
            temp["room_id"] = row[0]
            temp["room_name"] = row[1]
            temp["room_address"] = row[2]
            temp["room_performance"] = row[3]
            temp["room_price"] = row[4]
            temp["room_type"] = row[5]
            temp["room_province"] = row[6]
            temp["status"] = row[7]

            final_data.append(temp)
        conn.close()
        # print(final_data)
        return render_template(
            "admin/room.html", data=final_data, page=total_page, next=next, prev=prev
        )


@adview_blp.route("/room_filter", defaults={"page": 1})
@adview_blp.route("/room_filter/<int:page>")
def filter(page):
    limit = 5
    offset = page * limit - limit
    conn = connect_db()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT * FROM phong where room_isdelete = 1")
    except:
        conn.rollback()
    total_row = cursor.rowcount
    total_page = math.ceil(total_row / limit)

    next = page + 1
    prev = page - 1
    try:
        cursor.execute("SELECT * FROM phong")
    except:
        conn.rollback()
    conn.close()
    total_row = cursor.rowcount
    total_page = math.ceil(total_row / limit)
    conn = connect_db()
    cursor = get_cursor(conn)
    phong = ""
    id_filter = request.args.get("id_filter")
    show_option = request.args.get("show_option")
    if show_option == "hoatdong":
        if id_filter == "room_id":
            try:
                cursor.execute(
                    'select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 1  order by phong.room_id LIMIT %s OFFSET %s;',
                    (
                        limit,
                        offset,
                    ),
                )
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
        elif id_filter == "room_price_up":
            try:
                cursor.execute(
                    'select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 1  order by phong.room_price ASC LIMIT %s OFFSET %s;',
                    (
                        limit,
                        offset,
                    ),
                )
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
        else:
            try:
                cursor.execute(
                    'select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province  where phong.room_isdelete = 1 order by phong.room_price DESC LIMIT %s OFFSET %s;',
                    (
                        limit,
                        offset,
                    ),
                )
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
        conn.close()
    else:
        cursor.execute("SELECT * FROM phong where room_isdelete = 0")
        total_row = cursor.rowcount
        total_page = math.ceil(total_row / limit)
        if id_filter == "room_id":
            try:
                cursor.execute(
                    'select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 0  order by phong.room_id LIMIT %s OFFSET %s;',
                    (
                        limit,
                        offset,
                    ),
                )
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
        elif id_filter == "room_price_up":
            try:
                cursor.execute(
                    'select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_isdelete = 0  order by phong.room_price ASC LIMIT %s OFFSET %s;',
                    (
                        limit,
                        offset,
                    ),
                )
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
        else:
            try:
                cursor.execute(
                    'select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name, room_isdelete from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province  where phong.room_isdelete = 0 order by phong.room_price DESC LIMIT %s OFFSET %s;',
                    (
                        limit,
                        offset,
                    ),
                )
                conn.commit()
                phong = cursor.fetchall()
            except:
                conn.rollback()
    final_data = []
    for row in phong:
        temp = {}
        temp["room_id"] = row[0]
        temp["room_name"] = row[1]
        temp["room_address"] = row[2]
        temp["room_performance"] = row[3]
        temp["room_price"] = row[4]
        temp["room_type"] = row[5]
        temp["room_province"] = row[6]
        if row[7] == b"\x00":
            temp["room_isdelete"] = "UNACTIVE"
        else:
            temp["room_isdelete"] = "ACTIVE"
        final_data.append(temp)
    print(id_filter, show_option)
    return render_template(
        "admin/room.html",
        data=final_data,
        show_option=show_option,
        id_filter=id_filter,
        page=total_page,
        next=next,
        prev=prev,
    )


@adview_blp.route("/customer")
def customer():
    conn = connect_db()
    cursor = get_cursor(conn)
    try:
        cursor.execute("select * from khachhang where customer_isdelete = 1")
        conn.commit()
    except:
        conn.commit()
    khachhang = cursor.fetchall()
    print(khachhang)
    data = []
    for row in khachhang:
        temp = {}
        temp["customer_id"] = row[0]
        temp["customer_name"] = row[1] + " " + row[2]
        temp["customer_identity"] = row[4]
        temp["customer_gender"] = row[5]
        temp["customer_phone"] = row[6]
        temp["customer_date"] = row[8]
        temp["customer_address"] = row[7]
        temp["customer_nation"] = row[9]
        temp["customer_note"] = row[10]
        if row[11] == b"\x01":
            temp["customer_isdelete"] = "ACTIVE"
        else:
            temp["customer_isdelete"] = "UNACTIVE"

        data.append(temp)
    print(data)
    return render_template("admin/customer.html", data=data)


@adview_blp.route("/filter_customer")
def filter_customer():
    show_option = request.args.get("show_option")
    id_file = request.args.get("id_filter")
    if show_option == "daxoa":
        if id_file == "name_up":
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                cursor.execute(
                    "select * from khachhang where customer_isdelete = 0 order by last_name asc;"
                )
            except:
                conn.rollback()
            khachhang = cursor.fetchall()
            conn.close()
        elif id_file == "name_down":
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                cursor.execute(
                    "select * from khachhang where customer_isdelete = 0 order by last_name desc;"
                )
            except:
                conn.rollback()
            khachhang = cursor.fetchall()
            conn.close()
        else:
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                cursor.execute(
                    "select * from khachhang where customer_isdelete = 0 order by customer_id asc;"
                )
            except:
                conn.rollback()
            khachhang = cursor.fetchall()
            conn.close()
    else:
        if id_file == "name_up":
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                cursor.execute(
                    "select * from khachhang where customer_isdelete = 1 order by last_name asc;"
                )
            except:
                conn.rollback()
            khachhang = cursor.fetchall()
            conn.close()
        elif id_file == "name_down":
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                cursor.execute(
                    "select * from khachhang where customer_isdelete = 1 order by last_name desc;"
                )
            except:
                conn.rollback()
            khachhang = cursor.fetchall()
            conn.close()
        else:
            conn = connect_db()
            cursor = get_cursor(conn)
            try:
                cursor.execute(
                    "select * from khachhang where customer_isdelete = 1 order by customer_id asc;"
                )
            except:
                conn.rollback()
            khachhang = cursor.fetchall()
            conn.close()
    data = []
    for row in khachhang:
        temp = {}
        temp["customer_id"] = row[0]
        temp["customer_name"] = row[1] + " " + row[2]
        temp["customer_identity"] = row[4]
        temp["customer_gender"] = row[5]
        temp["customer_phone"] = row[6]
        temp["customer_date"] = row[8]
        temp["customer_address"] = row[7]
        temp["customer_nation"] = row[9]
        temp["customer_note"] = row[10]
        if row[11] == b"\x01":
            temp["customer_isdelete"] = "ACTIVE"
        else:
            temp["customer_isdelete"] = "UNACTIVE"

        data.append(temp)
    print(data)
    return render_template(
        "admin/customer.html", data=data, id_filter=id_file, show_option=show_option
    )


@adview_blp.route("/room_booking")
def booking_room():
    return render_template("admin/booking.html")


@adview_blp.route("/booking_detail", defaults={"page": 1})
@adview_blp.route("/booking_detail/<int:page>", methods=["GET", "POST"])
def booking_detail(page):
    search_text = request.args.get("search_text")

    limit = 10
    offset = page * limit - limit
    conn = connect_db()
    cursor = get_cursor(conn)
    try:
        cursor.execute("SELECT * FROM datphong")
        conn.commit()
    except:
        conn.rollback()
    total_row = cursor.rowcount
    total_page = math.ceil(total_row / limit)

    next = page + 1
    prev = page - 1
    try:
        cursor.execute("SELECT * FROM datphong where datphong.isdelete = 0")
        conn.commit()
    except:
        conn.rollback()
    conn.close()
    total_row = cursor.rowcount
    total_page = math.ceil(total_row / limit)
    conn = connect_db()
    cursor = get_cursor(conn)

    cursor.execute(
        """select khachhang.customer_id, datphong.bookroom_id, concat(khachhang.first_name," ", khachhang.last_name),
                        khachhang.customer_phone, khachhang.customer_nation, phong.room_name, phong.room_id, datphong.time_start, datphong.status from datphong 
            inner join khachhang on khachhang.customer_id = datphong.customer_id
            inner JOIN phong on phong.room_id = datphong.room_id
            where datphong.isdelete = 0 order by datphong.bookroom_id LIMIT {} OFFSET {}""".format(
            limit, offset
        )
    )
    khachhang = cursor.fetchall()
    data = []
    status = ['Đã nhận phòng', 'Đã đặt trước', 'Đã đăng ký']
    for row in khachhang:
        temp = {}
        temp["customer_id"] = row[0]
        temp["bookroom_id"] = row[1]
        temp["customer_name"] = row[2]
        temp["customer_phone"] = row[3]
        temp["customer_nation"] = row[4]
        temp["room_name"] = row[5]
        temp["room_id"] = row[6]
        temp['check_in'] = row[7]
        temp['status'] = status[int(row[8])]
        data.append(temp)
    return render_template(
        "admin/booking_detail.html",
        data=data,
        page=total_page,
        next=next,
        prev=prev,
        search_text=search_text,
        amount=total_row,
    )
@adview_blp.route('/update_booking', methods=['GET', 'POST'])
def update_booking():
    select = request.args.get('status')
    bookroom_id = request.args.getlist('booking')
    customer = ''
    if bookroom_id and select:
        conn = connect_db()
        cursor = get_cursor(conn)
        print(select, bookroom_id[0])
        cursor.execute('UPDATE datphong set datphong.status = %s where datphong.bookroom_id in %s', (select, bookroom_id,))
        conn.commit()
        print(int(select))
        if (int(select) == 0):
            if len(bookroom_id) == 1:
                try:
                    cursor.execute('select datphong.customer_id, datphong.time_start, datphong.time_end, phong.room_price from datphong inner join phong on phong.room_id = datphong.room_id where bookroom_id = %s', (bookroom_id[0],))
                    customer = cursor.fetchone()
                    bill_id = str(bookroom_id[0]) + "_" + str(customer[0])
                    days = int((customer[2] - customer[1]).days)
                    total_money = days * customer[3]
                    print(bill_id, total_money)
                    cursor.execute("insert into hoadon VALUES (%s,%s,%s, 'Chưa thanh toán', %s)",(bill_id,bookroom_id[0], total_money,datetime.now(),))
                    conn.commit()
                    print('bill ok')
                    cursor.execute('update datphong set datphong.isdelete = 1 where datphong.bookroom_id = %s', (bookroom_id[0]))
                    conn.commit()
                    print('isdelete')
                    cursor.execute('UPDATE phong set phong.status = "Đang phục vụ" where phong.room_id in (select datphong.room_id from datphong where datphong.bookroom_id = %s)', (bookroom_id[0]))
                    conn.commit()
                    print('Thanh cong')
                    flash("Created a bill for this booking", "alert alert-success")
                except:
                    conn.rollback()
                    flash("Fail to create a bill for this booking", "alert alert-danger")
            else:
                for item in bookroom_id:
                    try:
                        cursor.execute('select datphong.customer_id, datphong.time_start, datphong.time_end, phong.room_price from datphong inner join phong on phong.room_id = datphong.room_id where bookroom_id = %s', (int(item),))
                        customer = cursor.fetchone()
                        bill_id = str(item[0]) + "_" + str(customer[0])
                        days = int((customer[2] - customer[1]).days)
                        total_money = days * int(customer[3])
                        cursor.execute("insert into hoadon VALUES (%s,%s,%s, 'Chưa thanh toán', %s)",(bill_id,int(item), total_money,datetime.now(),))
                        conn.commit()
                        cursor.execute('update datphong set datphong.isdelete = 1 where datphong.bookroom_id = %s', (item))
                        conn.commit()
                        cursor.execute('UPDATE phong set phong.status = "Đang phục vụ" where phong.room_id in (select datphong.room_id from datphong where datphong.bookroom_id = %s', (item,))
                        conn.commit()
                    except:
                        conn.rollback()
                        flash("Fail to create bills for this booking", "alert alert-danger")
                print('Thanh cong')
                flash("Created bills for these booking", "alert alert-success")
        flash("Update successfully", "alert alert-success")
    else:
        flash('Empty selection or actions! Please try again', "alert alert-warning")
    # try:
    #     cursor.execute('UPDATE datphong set datphong.status = %s where datphong.bookroom_id in %s', (select, bookroom_id,))
    #     conn.commit()
    #     if (select == 0):
    #         cursor.execute('select datphong.customer_id from datphong where bookroom_id = %s', (bookroom_id,))
    #         customer = customer.fetchone()
    #         bill_id = str(bookroom_id) + "_" + str(customer[0])
    #         cursor.execute("insert into hoadon VALUES (%s,%s,%s, 'Chưa thanh toán')",(bill_id,id_datphong[0], total_money,))
    #         conn.commit()
    #         print('Thanh cong')
    # except:
    #     conn.rollback()
    return redirect('/booking_detail')