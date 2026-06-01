from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    biography = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )
    cover_image = models.ImageField(upload_to='books/',blank=True,null=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    isbn = models.CharField(max_length=20)

    publication_year = models.IntegerField()

    total_copies = models.IntegerField()

    available_copies = models.IntegerField()

    description = models.TextField()

    def __str__(self):
        return self.title
class BorrowRecord(models.Model):
    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    borrow_date = models.DateField(auto_now_add=True)

    due_date = models.DateField()

    return_date = models.DateField(
        null=True,
        blank=True
    )

    fine = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    returned = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.member.username} - {self.book.title}"