from django.urls import path
from .views import home, book_detail,borrow_book,return_book,borrowing_history,dashboard,BookListAPIView
from .views import (
    AuthorListAPIView,
    CategoryListAPIView,
    BookListAPIView,
    BorrowRecordListAPIView
)
urlpatterns = [
    path('', home, name='home'),
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('return/<int:book_id>/', return_book, name='return_book'),
    path('history/',borrowing_history,name='history'),
    path('dashboard/', dashboard, name='dashboard'),
    path('api/books/',BookListAPIView.as_view(),name='api-books'),
    path('api/authors/', AuthorListAPIView.as_view()),
    path('api/categories/', CategoryListAPIView.as_view()),
    path('api/books/', BookListAPIView.as_view()),
    path('api/borrow-records/', BorrowRecordListAPIView.as_view()),

]