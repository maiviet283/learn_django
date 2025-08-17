from django.db import models
from .custom_author_manager_queryset import AuthorManager

class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    created_at = models.DateTimeField(auto_now_add=True)

    # .objects
    objects = AuthorManager()

    # Bạn có thể đặt tên khác nếu muốn, như:
    active_authors = AuthorManager()

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='This is a well-written novel exploring deep human emotions and relationships.')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
