import os
import django
from django.db import connection, reset_queries

# Thiết lập Django environment (dành cho script chạy ngoài manage.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from books.models import Book

def main():
    print("-" * 40)

    # Reset lại danh sách các truy vấn để đo chính xác số lượng SQL
    reset_queries()

    """
    Sử dụng defer('description') để trì hoãn việc load trường 'description'.
    Nghĩa là Django sẽ không lấy giá trị trường 'description' ngay từ truy vấn ban đầu.
    Trường này chỉ được load nếu bạn truy cập nó sau này (lazy load).
    """
    books = Book.objects.defer('description')  # Đây là một QuerySet, chưa bị evaluate

    # In ra QuerySet (vẫn chưa thực hiện truy vấn SQL)
    print(books)

    # Khi bắt đầu lặp qua QuerySet, Django mới thực hiện truy vấn SQL đầu tiên
    # Truy vấn sẽ lấy tất cả các field trừ 'description'
    for book in books:
        print(f"{book.title}")  # Truy cập title (đã có sẵn từ truy vấn ban đầu)

        # Nếu thêm dòng này:
        # print(book.description)
        # → Django sẽ thực hiện thêm một truy vấn SQL nữa cho mỗi book

    # In ra số lượng truy vấn đã thực hiện
    # Trong trường hợp chỉ truy cập 'title', sẽ chỉ có 1 truy vấn duy nhất (load danh sách sách)
    print("Số lượng truy vấn SQL đã thực hiện =", len(connection.queries))
    print("-" * 40)

if __name__ == '__main__':
    main()
