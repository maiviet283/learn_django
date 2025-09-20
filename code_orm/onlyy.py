import os
import django
from django.db import connection, reset_queries

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from books.models import Book

def main():
    print("-"*40)
    reset_queries()

    books = Book.objects.only('title','author__name').select_related('author')
    for book in books:
        print(f"{book.author.name} - {book.title} - {book.author.age}")
        if book.author.age == 31:
            book.author.age = 30
            book.author.save()
        # truy cap them tuoi se them 1 truy van

    print("so luong truy van = ", len(connection.queries))
    print("-"*40)

if __name__ == '__main__':
    main()