from rest_framework.viewsets import ModelViewSet

from books.models import Book
from books.serializers import BookSerializer
from easy_tags.filters import GetObjectsByAllTagsFilter


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [GetObjectsByAllTagsFilter]
