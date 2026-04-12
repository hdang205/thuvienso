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

    def create(self, validated_data):
        # Set available_quantity to total_quantity if not provided
        if 'available_quantity' not in validated_data:
            validated_data['available_quantity'] = validated_data.get('total_quantity', 1)
        return super().create(validated_data)

class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    book_id = serializers.IntegerField(write_only=True, required=False)
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['id', 'user', 'book', 'user_id', 'book_id', 'loan_date',
                 'due_date', 'return_date', 'status', 'notes', 'is_overdue']
        read_only_fields = ['loan_date', 'return_date']

    def get_is_overdue(self, obj):
        """Check if loan is overdue"""
        from django.utils import timezone
        return obj.status == 'borrowed' and obj.due_date < timezone.now()

    def validate(self, attrs):
        # For creation, require book_id
        if self.instance is None and 'book_id' not in attrs:
            raise serializers.ValidationError({'book_id': 'This field is required for new loans'})

        # Check book availability for new loans
        if self.instance is None:
            try:
                book = Book.objects.get(id=attrs['book_id'])
                if book.available_quantity <= 0:
                    raise serializers.ValidationError({'book_id': 'Book is not available for loan'})
            except Book.DoesNotExist:
                raise serializers.ValidationError({'book_id': 'Book not found'})

        return attrs

    def create(self, validated_data):
        user_id = validated_data.pop('user_id', None)
        book_id = validated_data.pop('book_id')

        # Use current user if not specified (for student self-borrowing)
        if not user_id:
            user_id = self.context['request'].user.id

        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)

        # Check if user already has this book
        existing_loan = Loan.objects.filter(
            user=user,
            book=book,
            status='borrowed'
        ).exists()

        if existing_loan:
            raise serializers.ValidationError('You already have this book borrowed')

        loan = Loan.objects.create(user=user, book=book, **validated_data)

        # Update book availability - REMOVED FOR DEBUG
        # book.available_quantity -= 1
        # book.save()

        return loan