from rest_framework.serializers import ModelSerializer

from books.models import Book, Author
from easy_tags.serializers import TagSerializer


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        exclude = ('id',)


class BookSerializer(ModelSerializer):
    author = AuthorSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        exclude = ('id',)
