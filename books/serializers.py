from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','title','description','author']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.author:
            rep['author'] = instance.author.name
        return rep