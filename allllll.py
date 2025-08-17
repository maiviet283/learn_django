import os
import django
from django.db import connection, reset_queries

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from books.models import Author, Book

"""
.all() trả về toàn bộ dữ liệu → nếu bảng có nhiều bản ghi sẽ rất nặng.

Bạn có thể kết hợp thêm:
.filter(...) → lọc kết quả
.exclude(...) → loại bỏ
.order_by(...) → sắp xếp
.only(...) hoặc .values(...) → lấy cột cụ thể để tối ưu
"""


def main():
    reset_queries()

    books = Book.objects.all()
    for book in books:
        print(book.title)


    print("so luong truy van = ", len(connection.queries))

if __name__ == '__main__':
    main()