import os
import django
from django.db import connection, reset_queries
from django.db.models import OuterRef, Subquery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from books.models import Author, Book


def main():
    reset_queries()

    """
        SELECT author.id, author.name, (
            SELECT title FROM book 
            WHERE book.author_id = author.id 
            ORDER BY created_at DESC LIMIT 1
        ) AS latest_book_title FROM author
    """

    authors = Author.objects.annotate(
        latest_book_title = Subquery(
            Book.objects.filter(author=OuterRef('pk')).order_by('-created_at').values('title')[:1]
        )
    )

    for author in authors:
        print(f"{author} - {author.latest_book_title}")

    print("so luong truy van = ", len(connection.queries))

if __name__ == '__main__':
    main()