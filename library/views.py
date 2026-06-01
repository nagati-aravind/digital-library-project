from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from .models import Book, BorrowRecord, Author, Category
from rest_framework.generics import ListAPIView
from .serializers import BookSerializer
from rest_framework.generics import ListAPIView
from .serializers import (
    AuthorSerializer,
    CategorySerializer,
    BookSerializer,
    BorrowRecordSerializer
)
from django.contrib import messages

def home(request):

    query = request.GET.get('q')
    category_id = request.GET.get('category')

    books = Book.objects.all()

    if query:
        books = books.filter(
            title__icontains=query
        )

    if category_id:
        books = books.filter(
            category_id=category_id
        )

    categories = Category.objects.all()

    context = {
        'books': books,
        'categories': categories,
        'selected_category': category_id,
    }

    return render(request, 'home.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    return render(
        request,
        'book_detail.html',
        {'book': book}
    )


@login_required
def borrow_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    if book.available_copies > 0:

        BorrowRecord.objects.create(
            member=request.user,
            book=book,
            due_date=date.today() + timedelta(days=14)
        )

        book.available_copies -= 1
        book.save()
        messages.success(request, 'Book borrowed successfully!')

    return redirect('book_detail', book_id=book.id)


@login_required
def return_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    borrow_record = BorrowRecord.objects.filter(
        member=request.user,
        book=book,
        returned=False
    ).first()

    if borrow_record:

        borrow_record.returned = True
        borrow_record.return_date = date.today()

        late_days = (
            borrow_record.return_date -
            borrow_record.due_date
        ).days

        if late_days > 0:
            borrow_record.fine = late_days * 5

        borrow_record.save()

        book.available_copies += 1
        book.save()
        messages.success(request,'Book returned successfully!')

    return redirect('book_detail', book_id=book.id)
@login_required
def borrowing_history(request):

    records = BorrowRecord.objects.filter(
        member=request.user
    )

    return render(
        request,
        'history.html',
        {'records': records}
    )
@login_required
def dashboard(request):

    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    total_categories = Category.objects.count()
    total_borrow_records = BorrowRecord.objects.count()
    active_borrows = BorrowRecord.objects.filter(returned=False).count()

    context = {
        'total_books': total_books,
        'total_authors': total_authors,
        'total_categories': total_categories,
        'total_borrow_records': total_borrow_records,
        'active_borrows': active_borrows,
    }

    return render(request, 'dashboard.html', context)
class AuthorListAPIView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookListAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BorrowRecordListAPIView(ListAPIView):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer