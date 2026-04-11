from rest_framework import serializers
from .models import User, Book, Loan

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                 'role', 'student_id', 'phone', 'date_joined']
        read_only_fields = ['date_joined']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'category', 'description',
                 'total_quantity', 'available_quantity', 'published_date',
                 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'user', 'book', 'user_id', 'book_id', 'loan_date',
                 'due_date', 'return_date', 'status', 'notes']
        read_only_fields = ['loan_date']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        book_id = validated_data.pop('book_id')
        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)

        # Check if book is available
        if book.available_quantity <= 0:
            raise serializers.ValidationError("Book is not available for loan")

        loan = Loan.objects.create(user=user, book=book, **validated_data)
        return loan