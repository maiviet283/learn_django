import os
import sys
import django
from django.db import connection, reset_queries

CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from books.models import Author, Book

def main():
    reset_queries() 
    # ----------- LÝ THUYẾT -----------
    # exists(): Kiểm tra xem QuerySet có phần tử nào hay không.
    # -> Trả về True nếu có ít nhất một bản ghi khớp với điều kiện, ngược lại trả về False.
    # -> Tối ưu hiệu suất vì chỉ sinh ra câu truy vấn SQL dùng LIMIT 1, không load toàn bộ dữ liệu.

    # count(): Đếm số lượng bản ghi trong QuerySet.
    # -> Sinh ra câu truy vấn SQL với COUNT(*) để đếm trực tiếp trên database.
    # -> Không load toàn bộ dữ liệu vào Python, hiệu suất tốt hơn `len(QuerySet)`.

    # ----------- CODE CỤ THỂ -----------

    # Kiểm tra xem có tác giả nào có tên chứa từ "nga" (không phân biệt hoa thường) hay không
    has_book = Author.objects.filter(name__icontains="nga").exists()
    print(has_book)  # True nếu tồn tại ít nhất 1 tác giả có tên chứa "nga"

    # Đếm số lượng sách của các tác giả có tên chứa "Nguyễn NhậT ÁNH" (không phân biệt hoa thường)
    anh_count_book = Book.objects.filter(author__name__icontains="Nguyễn NhậT ÁNH").count()
    print(anh_count_book)  # Ví dụ: 4

    print("so luong truy van = ", len(connection.queries))

if __name__ == '__main__':
    main()
