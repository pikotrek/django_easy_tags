from rest_framework.routers import DefaultRouter

from books.views import BookViewSet

router = DefaultRouter()

router.register(r'book', BookViewSet, base_name='book')

urlpatterns = [

] + router.urls
