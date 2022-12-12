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


