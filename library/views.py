from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, Book, Loan
from .serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer, BookSerializer, LoanSerializer

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

    def get_queryset(self):
        """Filter loans based on user role"""
        user = self.request.user
        if user.role == 'student':
            # Students can only see their own loans
            return Loan.objects.filter(user=user).select_related('user', 'book')
        # Librarians can see all loans
        return Loan.objects.select_related('user', 'book')

    @action(detail=False, methods=['post'])
    def borrow(self, request):
        """Borrow a book"""
        book_id = request.data.get('book_id')
        due_date = request.data.get('due_date')

        if not book_id:
            return Response(
                {'error': 'book_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            book = Book.objects.select_for_update().get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if book is available
        if book.available_quantity <= 0:
            return Response(
                {'error': 'Book is not available for loan'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user already has this book borrowed
        existing_loan = Loan.objects.filter(
            user=request.user,
            book=book,
            status='borrowed'
        ).exists()

        if existing_loan:
            return Response(
                {'error': 'You already have this book borrowed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Set default due date if not provided (14 days from now)
        from datetime import timedelta
        if not due_date:
            due_date = (request.data.get('loan_date') or timezone.now()) + timedelta(days=14)

        loan = Loan.objects.create(
            user=request.user,
            book=book,
            due_date=due_date
        )

        # Update book availability
        book.available_quantity -= 1
        book.save()

        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """Return a borrowed book"""
        loan = self.get_object()

        # Check permissions - only borrower or librarian can return
        if request.user.role != 'librarian' and loan.user != request.user:
            return Response(
                {'error': 'You can only return your own loans'},
                status=status.HTTP_403_FORBIDDEN
            )

        if loan.status == 'returned':
            return Response(
                {'error': 'Book already returned'},
                status=status.HTTP_400_BAD_REQUEST
            )

        loan.status = 'returned'
        loan.return_date = timezone.now()
        loan.save()

        # Update book availability
        loan.book.available_quantity += 1
        loan.book.save()

        serializer = LoanSerializer(loan)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_loans(self, request):
        """Get current user's loans"""
        loans = Loan.objects.filter(user=request.user).select_related('user', 'book')
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue loans (librarian only)"""
        if request.user.role != 'librarian':
            return Response(
                {'error': 'Only librarians can view overdue loans'},
                status=status.HTTP_403_FORBIDDEN
            )

        from django.utils import timezone
        overdue_loans = Loan.objects.filter(
            status='borrowed',
            due_date__lt=timezone.now()
        ).select_related('user', 'book')

        serializer = LoanSerializer(overdue_loans, many=True)
        return Response(serializer.data)


# Authentication views
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login user and return JWT tokens"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Register new user"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout user by blacklisting refresh token"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Successfully logged out'})
    except Exception as e:
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """Get current user information"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# Chat/Recommendation views
def get_book_recommendations(query, limit=5):
    """
    Simple rule-based book recommendation engine.
    Matches books by category, title, or author based on the query.
    """
    query_lower = query.lower()
    
    # Search by category
    books = Book.objects.filter(
        category__icontains=query_lower
    ) | Book.objects.filter(
        title__icontains=query_lower
    ) | Book.objects.filter(
        author__icontains=query_lower
    ) | Book.objects.filter(
        description__icontains=query_lower
    )
    
    # Order by availability and relevance
    books = books.filter(available_quantity__gt=0).order_by('-available_quantity')[:limit]
    
    return books


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_recommend_view(request):
    """
    AI Chatbot recommendation endpoint.
    Takes a user query and returns book recommendations.
    
    Request: { "query": "machine learning books" }
    Response: { "suggestions": [...], "message": "..." }
    """
    query = request.data.get('query', '').strip()
    
    if not query:
        return Response(
            {
                'suggestions': [],
                'message': 'Please ask me about book recommendations! Try: "books about machine learning" or "fiction novels"'
            }
        )
    
    # Get recommendations
    books = get_book_recommendations(query, limit=5)
    
    if not books:
        return Response(
            {
                'suggestions': [],
                'message': f'I couldn\'t find books matching "{query}". Try searching for different topics like: Fiction, Science, History, Technology, etc.'
            }
        )
    
    # Format response
    suggestions = []
    for book in books:
        suggestions.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'category': book.category,
            'description': book.description[:100] + '...' if book.description and len(book.description) > 100 else book.description,
            'available_quantity': book.available_quantity,
        })
    
    message = f"Great! I found {len(suggestions)} book(s) matching your interest in '{query}'. Would you like to borrow any of these?"
    
    return Response({
        'suggestions': suggestions,
        'message': message
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """Update user profile"""
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
