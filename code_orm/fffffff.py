import os
import django
from django.db import connection, reset_queries
from django.db.models import F, Count
import sys

CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from books.models import Author, Book


def main():
    reset_queries()

    """
        Không cần load từng Author vào RAM → rất nhanh và tối ưu.
        Dùng update(...) chứ không phải .save() lặp từng object.

        Chạy hoàn toàn trong SQL
        Không load dữ liệu lên Python
        Không gọi .save() hoặc signal
        Rất phù hợp để cập nhật hàng loạt

        Giảm số lượng sản phẩm sau khi đặt hàng
        tăng số tuổi của toàn bộ người dùng
        tăng lượt xem bài viết
        Thêm điểm thưởng cho người dùng sau khi mua hàng
        Tính tổng tiền đơn hàng (sau khi giảm giá)
        Tìm học sinh có điểm giữa kỳ thấp hơn điểm cuối kỳ: Student.objects.filter(midterm_score__lt=F('final_score'))
        Tăng số lượng người theo dõi khi có người nhấn "Follow"
        Tự động trừ số lần sử dụng mã giảm giá sau mỗi đơn hàng
    """

    # Tăng tuổi của tất cả tác giả lên 5
    # Author.objects.filter(age__gt=50).update(age=F('age')+1)

    # Chỉ tăng tuổi cho tác giả có hơn 3 cuốn sách (sử dụng annotate + filter)
    Author.objects.annotate(book_count=Count('books')).filter(book_count__gt=3).update(age=F('age') + 1)


    print("so luong truy van = ", len(connection.queries))

if __name__ == '__main__':
    main()