import os
import django
from django.db import connection, reset_queries
from django.db.models import F, Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from books.models import Author, Book


def main():
    reset_queries()

    Author.objects.filter(id=5).update(age=10)


    print("so luong truy van = ", len(connection.queries))

if __name__ == '__main__':
    main()