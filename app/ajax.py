from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
)
from app.db_utils import connect_db, get_cursor
from app.sql import *

ajax_blp = Blueprint(
    "ajax", __name__, template_folder="templates/admin", static_folder="static"
)


@ajax_blp.route("/type_room_ajax", methods=["POST", "GET"])
def type_room_ajax():
    conn = connect_db()
    cursor = get_cursor(conn)
    if request.method == "POST":
        queryString = request.form["queryString"]
        print(queryString)
        query = "SELECT * from loaiphong WHERE room_name LIKE '%{}%' LIMIT 10".format(
            queryString
        )
        cursor.execute(query)
        loaiphong = cursor.fetchall()
    return jsonify(
        {
            "htmlresponse": render_template(
                "admin/response/response_roomtype.html", loaiphong=loaiphong
            )
        }
    )


@ajax_blp.route("/nation_ajax", methods=["POST", "GET"])
def nation_ajax():
    conn = connect_db()
    cursor = get_cursor(conn)
    if request.method == "POST":
        queryString = request.form["queryString"]
        print(queryString)
        query = "SELECT * from quoctich WHERE name LIKE '%{}%' LIMIT 10".format(
            queryString
        )
        cursor.execute(query)
        nation = cursor.fetchall()
    return jsonify(
        {
            "htmlresponse": render_template(
                "admin/response/respone_nation.html", nation=nation
            )
        }
    )


@ajax_blp.route("/room_ajax", methods=["POST", "GET"])
def room_ajax():
    conn = connect_db()
    cursor = get_cursor(conn)
    if request.method == "POST":
        checkin = request.form["checkin"]
        checkout = request.form["checkout"]
        province = request.form["province"]
        print(checkin, checkout, province)
        query = """select room_id, room_name from phong INNER JOIN tinhthanh on tinhthanh.province_id = phong.id_province where phong.room_id not in (
SELECT distinct phong.room_id from phong inner join datphong on datphong.room_id = phong.room_id where (datphong.time_start BETWEEN '{}' and  '{}') or (datphong.time_end BETWEEN '{}' and  '{}')) and tinhthanh.province_name like "%{}" and datphong.isdelete = 0;""".format(
            checkin, checkout, checkin, checkout, province
        )
        print(query)
        cursor.execute(query)
        room = cursor.fetchall()
        print(room)
    return jsonify(
        {"htmlresponse": render_template("admin/response/respone_room.html", room=room)}
    )


@ajax_blp.route("/caculate_ajax", methods=["get", "post"])
def caculate():
    conn = connect_db()
    cur = get_cursor(conn)
    data = request.form["karaoke"]
    print("connect")
    return


@ajax_blp.route("/ajax_bill_search", methods=["POST", "GET"])
def ajax_bill_search():
    conn = connect_db()
    cursor = get_cursor(conn)
    if request.method == "POST":
        queryString = request.form["query"]
        cursor.execute("""select * from hoadon""")
        result = cursor.fetchall()
        print(queryString, result)
    return jsonify("success")


@ajax_blp.route("/ajaxpost", methods=["POST", "GET"])
def ajaxpost():
    conn = connect_db()
    cursor = get_cursor(conn)
    if request.method == "POST":
        queryString = request.form["queryString"]
        print(queryString)
        query = (
            "SELECT * from tinhthanh WHERE province_name LIKE '%{}%' LIMIT 10".format(
                queryString
            )
        )
        cursor.execute(query)
        tinhthanh = cursor.fetchall()
    return jsonify(
        {
            "htmlresponse": render_template(
                "admin/response/response_province.html", tinhthanh=tinhthanh
            )
        }
    )
