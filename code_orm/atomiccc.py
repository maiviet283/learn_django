import os
import sys
import django
from django.db import connection, reset_queries, transaction

CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from books.models import Author, Book

def create_author_book(ten, tuoi, tieu_de):
    author = Author.objects.create(name=ten, age=tuoi)
    Book.objects.create(title=tieu_de, author=author)

def main():
    reset_queries()

    try:
        with transaction.atomic():
            create_author_book("Neymar", 33, "Samba")
            create_author_book("Manadona", 61, "Goden Boy")
            create_author_book("Pele", 80, "King Football")
    except Exception as e:
        print("Đã xảy ra lỗi, toàn bộ transaction sẽ bị rollback:", e)

    print("Tổng số truy vấn SQL = ", len(connection.queries))

if __name__ == '__main__':
    main()