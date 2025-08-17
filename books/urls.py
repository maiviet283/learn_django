from django.urls import path
from . import views
from . import controller

app_name = 'books'
urlpatterns = [
    path('', views.book_list, name='home'),
    path('list/', controller.BookList.as_view(), name='api-book-list'),
    path('<int:pk>/', controller.BookDetail.as_view(), name='book-detail'),

    path('details-author/<int:id>', views.details_author, name='details-author'),
    path('update-author/<int:id>', views.update_author, name='update-author'),
]