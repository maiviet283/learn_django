# ================================
# MỤC ĐÍCH: Tạo Author và Book liên kết với nhau trong một transaction duy nhất.
# GIẢI THÍCH: Mỗi Author có một Book, và tất cả sẽ được ghi vào DB trong 1 transaction duy nhất.
# KẾT QUẢ: Nếu bất kỳ lỗi nào xảy ra, toàn bộ dữ liệu sẽ rollback để đảm bảo tính toàn vẹn.
# ================================

import os
import django
from django.db import connection, reset_queries, transaction

# Cấu hình Django khi chạy script ngoài
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

# Import model
from books.models import Author, Book

# ================================
# HÀM: create_author_book
# CHỨC NĂNG: Tạo một Author mới và một Book mới liên kết với tác giả đó.
# Lưu ý: Không dùng @transaction.atomic ở đây để tránh tạo nhiều transaction nhỏ không cần thiết.
# ================================
def create_author_book(ten, tuoi, tieu_de):
    # Tạo tác giả mới
    author = Author.objects.create(name=ten, age=tuoi)
    # Tạo sách mới, liên kết với tác giả vừa tạo
    Book.objects.create(title=tieu_de, author=author)

# ================================
# HÀM: main
# CHỨC NĂNG: Chạy các thao tác chính trong một transaction duy nhất để tối ưu truy vấn.
# GIẢI THÍCH:
# - reset_queries(): Xóa bộ đếm truy vấn SQL của Django (chỉ dùng để đo performance).
# - with transaction.atomic(): Bọc toàn bộ logic trong một transaction duy nhất.
# - Điều này giúp tránh việc tạo 3 transaction riêng biệt (nếu @transaction.atomic được đặt trong mỗi hàm).
# - Tổng số truy vấn mong đợi: 1 BEGIN + 3 INSERT Author + 3 INSERT Book + 1 COMMIT = 8 truy vấn.
# ================================
def main():
    reset_queries()  # Xóa bộ đếm truy vấn (phục vụ việc thống kê)

    # Tối ưu bằng cách gộp nhiều thao tác vào một transaction duy nhất
    try:
        with transaction.atomic():
            create_author_book("Neymar", 33, "Samba")
            create_author_book("Manadona", 61, "Goden Boy")
            create_author_book("Pele", 80, "King Football")
    except Exception as e:
        print("Đã xảy ra lỗi, toàn bộ transaction sẽ bị rollback:", e)

    # In ra số lượng truy vấn SQL đã thực hiện
    print("Tổng số truy vấn SQL = ", len(connection.queries))

# ================================
# CHẠY CHƯƠNG TRÌNH
# ================================
if __name__ == '__main__':
    main()