import os
import sys
import django
from django.db.models import Count
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
    """
        có thể tận dụng hiển thị name rồi tính số lượng sách luôn cũng được vì chỉ trong 1 truy vấn
        total_books = BookTwo.objects.aggregate(total = Count('id')) : sẽ thêm 1 truy vấn nữa
        nếu ko hiển hị mà chỉ đếm thôi thì dùng total_books
    """
    i = 0
    books = Book.objects.select_related('author')
    for book in books:
        print(f'{book.author.name}')
        i+=1
    print(f'Co {i} cuon sach')
    print('so luong queries = ', len(connection.queries))
    print("-"*40)

    reset_queries()
    authors = Author.objects.annotate(book_count = Count('books')).prefetch_related('books').order_by('-book_count')
    for author in authors:
        print(f'{author} co {author.book_count} cuon sach')
        for book in author.books.all():
            print(" ----", book.title) 
    print('so luong queries = ', len(connection.queries))

    print("-"*40)
    reset_queries()
    total_books = Book.objects.aggregate(total = Count('id'))['total']
    book111 = Book.objects.get(id=15) # +1 truy van
    print(f'Co {total_books} cuon sach')
    print('so luong queries = ', len(connection.queries))

if __name__ == '__main__':
    main()