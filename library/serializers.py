from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Book, Loan

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                 'role', 'student_id', 'phone', 'date_joined']
        read_only_fields = ['date_joined']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm',
                 'first_name', 'last_name', 'role', 'student_id', 'phone']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include username and password')

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