## PHẦN HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH

# Chuẩn bị dữ liệu
Cấu trúc thư mục dữ được chia trên ổ của hệ điều hành Windown,nên thầy cô dùng Windown và làm theo hướng dẫn:
• B1: Đưa thư mục có tên "hotel_image" vào trong ổ D: 
(D:/hotel_image)
• B2: Mở folder chứa source code, và cài một số thư viện python liên quan
• B3: Mở Terminal cài các thư viện sau: pymysql, flask,
• B4: Cài đặt venv cho thư mục lưu trữ source code
Bên trên là các bước cài thư viện và chuẩn bị dữ liệu

# Hướng dẫn đặt đường dẫn
Chúng ta thay đổi các đường dẫn sau nhằm phù hợp với đường dẫn máy tính hiện tại
Trong file set_env.ps1: (dòng 9-11)
$Env:HOTEL_IMAGE="D:\\hotel_image" 
$Env:USER_IMAGE="D:\\...\\app\\static\\user_img"
$Env:BLOG_IMAGE="D:\\hotel_image\\blog_image"

Trong file view.py: (dòng 22-24)
sys.path.append(
    "D:\\...\\app"
)

Trong file config.py: (dòng 11-13)
HOTEL_IMAGE = os.environ.get("HOTEL_IMAGE", "D:\\hotel_image")
USER_IMAGE = os.environ.get("USER_IMAGE","D:\\...\\app\\static\\user_img")
BLOG_IMAGE = os.environ.get("BLOG_IMAGE","D:\\hotel_image\\blog_image")


# Cách chạy các file trên thư mục
- Chúng ta chỉ chạy một file duy nhất là "application.py" và "set_env.ps1" trong folder
- Các bước chạy như sau:
B1: Mở terminal trong VScode, di chuyển đến thư mục chưa file set_env.ps1 và application.py
B2: Gõ lệnh sau trong terminal: '.\set_env.ps1' (hoặc gõ 'set' rồi ấn tab) và enter
Lệnh trên thực hiện việc kết nối vs database
B3: Gõ lệnh: 'python application.py'. Được hiện thị bên dưới
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://localhost:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 389-649-
 
- Bạn giữ ctrl và nhấn vô đường dẫn 'http://localhost:5000' sẽ khởi tạo trình duyệt web của ta.
Vậy là ta vừa có thể sử dụng các file, phần sau sẽ hướng dẫn về database


## PHẦN MÔ TẢ CÁC FILE

# hootel_booking
Cách sử phân chia cấu trúc thư mục:
- thư mục 'venv' là để khởi chạy môi trường ảo
- Thư mục 'app' để chứa các thay đổi, các api, các templates. Trong đó
+ 'templates' chứa các file giao diện .html, được phân ra 2 loại là cho người dùng (user) và quản lý (admin), ngoài ra cũng chia theo chức năng của giao diện đó. Ví dụ 'auth' là templates chứa các giao diện cần xác minh (login, register, reset,...)
+ Các file .html còn lại trong 'templates' là giao diện chung
+ "statics" để chứa các file ảnh, file .css là các file tĩnh, ít phải chỉnh sửa nhiều
+ Các file .py là các API dành cho người dùng, và admin.

# Mục đích của file .py
Giải thích sơ lược về các sử dụng file
- '__init__.py' là file để tạo package chưa các module
- 'config.py' là file xây dựng cấu hình và liên kết với database
- 'db_utils.py' là file để tạo các module dùng tương tác với database
- 'view.py' và 'auth.py' là file API dùng để tương tác giữa web và database

# Hướng dẫn kết nối github
- Xem video hướng dẫn dưới đây để tải git tại [đây](https://www.youtube.com/watch?v=z-BDl0SBtgo&t=944s)
- Sau khi tải git, bắt đầu tiến hành kết nối
B1: Tạo 1 folder mới để kết nối, đặt tên tùy ý <br>
B2: Di chuyển vào folder, mở terminal gõ lệnh: git init <br>
B3: Gõ lệnh sau vào terminal: git remote add origin https://github.com/supehungay/hootel_booking.git <br>
B4: sau khi gõ ko thấy lỗi gì, gõ tiếp lệnh để tải hết các file trên github về để làm việc: git pull origin master <br>
Vậy là bên trên đã hướng dẫn kết nối với github, sau đây là hướng dẫn cách làm việc chung:
# Hướng dẫn sử dụng github
Nếu đã xem video hẳn mọi người đã biết workflow của github, mình sẽ k trình bày lại mà muốn thống nhất cách làm việc của nhóm
- Mỗi khi sửa file xong, mọi người cần add lên repository với lệnh: git add .
- Lệnh trên sẽ đưa mọi người đổi của mọi người vào "staging area", sau đó fox lênh: git commit -m "Ghi chú cho thay đổi của mình"
- Sau khi đã commit, bạn gõ lệnh: git push origin master
- Vậy là hoàn thành việc cập nhật file từ local lên github. 
* Lưu ý: Mọi người cần phải cập nhật ghi chú đầy đủ, để thành viên nắm rõ.

