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

from books.models import Book

def main():
    reset_queries()

    books = Book.objects.all()
    for book in books:
        print(book.title)

    print("so luong truy van = ", len(connection.queries))

if __name__ == '__main__':
    main()
