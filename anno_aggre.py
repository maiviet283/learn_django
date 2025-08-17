import os
import django
from django.db import connection, reset_queries
from django.db.models import Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from books.models import Author, Book

def main():
    reset_queries()

    authors = Author.objects.annotate(book_count = Count('books')).prefetch_related('books')

    for author in authors:
        print(f'{author} has {author.book_count} books')
        for book in author.books.all():
            print(f" -{book.title}")

    total_book = Book.objects.aggregate(total = Count('id'))
    print(f'There are {total_book['total']} books')

    print(f'Total queries SQL = {len(connection.queries)}')

if __name__ == '__main__':
    main()
