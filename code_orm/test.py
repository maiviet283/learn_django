import os
import sys
import django
from django.db.models import Count, Prefetch
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

    authors = (
        Author.objects
        .only('name')
        .annotate(count_book = Count('books'))
        .filter(count_book__gt = 0)
        .prefetch_related(
            Prefetch('books', queryset=Book.objects.only('title','author'), to_attr='pub_books')
        )
        .order_by('-count_book')
    )
    
    for author in authors:
        print(f'author : {author.name}')
        for book in author.pub_books:
            print(f"-----{book.title}")

    print(f"\nTotal queries SQL = {len(connection.queries)}")

if __name__ == '__main__':
    main()
