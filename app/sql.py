user = {}
user['update_customer_info'] = '''UPDATE khachhang SET `first_name` = %s, `last_name` = %s, `customer_identity`= %s,`customer_date`=%s, `customer_phone` = %s, `customer_address`=%s,`customer_gender`=%s,   `customer_note` = %s 
                                WHERE `account_id` = %s;'''
user['insert_customer_info'] = '''INSERT INTO khachhang values(NULL, %s,%s, %s, %s, %s,%s, %s, %s, NULL, %s, 0)'''      
user['update_username'] = '''UPDATE taikhoan  SET `user_name` = %s where `account_id` = %s;'''
user['get_customer_info'] = '''SELECT * FROM khachhang where account_id = %s'''
user['get_account_info'] = '''SELECT * FROM taikhoan where taikhoan.account_id = % s;'''

account = {}
account['reset_password'] = '''UPDATE taikhoan SET `password` = % s where `email` = % s;'''

room = {}
room['edit_room'] = '''UPDATE `phong` SET room_name = %s, room_address = %s, room_performence = %s, room_price = %s, id_roomtype = %s, id_province = %s WHERE `phong`.`room_id` = %s;'''
room['room_info'] ='''select phong.room_id, phong.room_name,room_address, room_performence, room_price,loaiphong.room_name as "room_type" ,province_name from phong inner join loaiphong on loaiphong.room_id = phong.id_roomtype inner join tinhthanh on tinhthanh.province_id = phong.id_province;'''
user['info_action'] = '''select phong.room_name, datphong.time_start, datphong.time_end, qldp.tinhtrang from datphong
                        inner join phong on phong.room_id = datphong.room_id
                        inner join ql_datphong as qldp on qldp.id_datphong = datphong.bookroom_id where datphong.customer_id = %s'''