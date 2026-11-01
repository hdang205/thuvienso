from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Sinh viên'),
        ('librarian', 'Thủ thư'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    total_quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    published_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        ordering = ['title']

class Loan(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Đang mượn'),
        ('returned', 'Đã trả'),
        ('overdue', 'Quá hạn'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.get_status_display()})"

    class Meta:
        ordering = ['-loan_date']

    def save(self, *args, **kwargs):
        # Update book availability when loan status changes
        if self.pk:  # Existing loan
            try:
                old_loan = Loan.objects.get(pk=self.pk)
                if old_loan.status != self.status:
                    if self.status == 'returned' and old_loan.status in ['borrowed', 'overdue']:
                        self.book.available_quantity += 1
                        self.book.save()
                    elif self.status in ['borrowed', 'overdue'] and old_loan.status == 'returned':
                        if self.book.available_quantity > 0:
                            self.book.available_quantity -= 1
                            self.book.save()
            except Loan.DoesNotExist:
                pass
        else:  # New loan
            if self.status == 'borrowed':
                if self.book.available_quantity > 0:
                    self.book.available_quantity -= 1
                    self.book.save()

        super().save(*args, **kwargs)
