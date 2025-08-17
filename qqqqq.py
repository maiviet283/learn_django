import os
import django
from django.db import connection, reset_queries
from django.db.models import Q, Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from books.models import Author

def main():
    reset_queries()

    authors = Author.objects.annotate(book_count = Count('books')).filter(
        Q(name__icontains = 'Ng') & Q(age__gte = 50) | Q(pk__exact = 9) # iexact
    ).order_by('book_count').prefetch_related('books')

    for author in authors:
        print(f"{author.name} co {author.book_count} cuon sach")
        for book in author.books.all():
            print(f" ---- {book.title}")

    print("so luong truy van = ", len(connection.queries))

if __name__ == '__main__':
    main()