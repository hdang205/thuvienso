from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import User, Book, Loan
from .serializers import UserSerializer, BookSerializer, LoanSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username']

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'author', 'isbn', 'category']
    ordering_fields = ['title', 'author', 'created_at']

    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):
        book = self.get_object()
        user_id = request.data.get('user_id')
        due_date = request.data.get('due_date')

        if not user_id or not due_date:
            return Response(
                {'error': 'user_id and due_date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if book.available_quantity <= 0:
            return Response(
                {'error': 'Book is not available'},
                status=status.HTTP_400_BAD_REQUEST
            )

        loan = Loan.objects.create(
            user=user,
            book=book,
            due_date=due_date
        )

        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.select_related('user', 'book')
    serializer_class = LoanSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'user', 'book']
    search_fields = ['user__username', 'book__title']
    ordering_fields = ['loan_date', 'due_date', 'return_date']

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        loan = self.get_object()

        if loan.status == 'returned':
            return Response(
                {'error': 'Book already returned'},
                status=status.HTTP_400_BAD_REQUEST
            )

        loan.status = 'returned'
        loan.return_date = request.data.get('return_date')
        loan.save()

        serializer = LoanSerializer(loan)
        return Response(serializer.data)
