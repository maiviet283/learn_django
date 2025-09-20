import os
import django
from django.db import connection, reset_queries
from books.custom_author_manager_queryset import AuthorManager


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from books.models import Author


def main():
    reset_queries()

    print("-"*50)

    authors = Author.objects.has_books().adults(54)
    for author in authors:
        print(f"{author.name} - {author.age} years old")

    print("-"*50)

    authors = Author.objects.age_between(20, 30)
    for author in authors:
        print(f"{author.name} - {author.age} years old")

    print("-"*50)

    authors = Author.objects.age_between(20, 30).name_contains("bo")
    for author in authors:
        print(f"{author.name} - {author.age} years old")

    print("-"*50)

    authors = Author.active_authors.filter(age__gte=40)
    for author in authors:
        print(f"{author.name} - {author.age} years old")
    
    print("-"*50)

    print("so luong truy van = ", len(connection.queries))

    print("-"*50)

if __name__ == '__main__':
    main()