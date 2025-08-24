import os
import django
from django.db import connection, reset_queries
from django.db.models import Count, Prefetch

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from books.models import Author, Book

def main():
    reset_queries()

    authors = (
        Author.objects
        .only('name')
        .annotate(count_book=Count('books'))
        .filter(count_book__gt=0)
        .prefetch_related(
            Prefetch('books', queryset=Book.objects.only('title', 'author'))
        )
        .order_by('-count_book')
    )

    for author in authors:
        print(f"{author.name} co {author.count_book} cuon sach")
        for book in author.books.all():
            print(f" ----{book.title}")

    total_book = Book.objects.aggregate(total=Count('id'))['total']
    print(f'Total book = {total_book}')

    print("\n=== SQL Queries ===")
    for q in connection.queries:
        print(q["sql"])

    print(f"\nTotal queries SQL = {len(connection.queries)}")

if __name__ == '__main__':
    main()
