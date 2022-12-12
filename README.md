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
- Xem video hướng dẫn dưới đây để tải git: https://www.youtube.com/watch?v=z-BDl0SBtgo&t=944s
- Sau khi tải git, bắt đầu tiến hành kết nối
B1: Tạo 1 folder mới để kết nối, đặt tên tùy ý
B2: Di chuyển vào folder, mở terminal gõ lệnh: git init 
B3: Gõ lệnh sau vào terminal: git remote add origin https://github.com/VanhhNe/hootel_booking.git
B4: sau khi gõ ko thấy lỗi gì, gõ tiếp lệnh để tải hết các file trên github về để làm việc: git pull origin master 
Vậy là bên trên đã hướng dẫn kết nối với github, sau đây là hướng dẫn cách làm việc chung:
# Hướng dẫn sử dụng github
Nếu đã xem video hẳn mọi người đã biết workflow của github, mình sẽ k trình bày lại mà muốn thống nhất cách làm việc của nhóm
- Mỗi khi sửa file xong, mọi người cần add lên repository với lệnh: git add .
- Lệnh trên sẽ đưa mọi người đổi của mọi người vào "staging area", sau đó fox lênh: git commit -m "Ghi chú cho thay đổi của mình"
- Sau khi đã commit, bạn gõ lệnh: git push origin master
- Vậy là hoàn thành việc cập nhật file từ local lên github. 
* Lưu ý: Mọi người cần phải cập nhật ghi chú đầy đủ, để thành viên nắm rõ.

