from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Book, Loan

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'student_id', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Thông tin thư viện', {'fields': ('role', 'student_id', 'phone')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Thông tin thư viện', {'fields': ('role', 'student_id', 'phone')}),
    )
    search_fields = ['username', 'first_name', 'last_name', 'email', 'student_id']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'category', 'available_quantity', 'total_quantity', 'published_date']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'author', 'isbn', 'category', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'loan_date', 'due_date', 'return_date', 'status']
    list_filter = ['status', 'loan_date', 'due_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'book__title', 'book__isbn']
    readonly_fields = ['loan_date']
