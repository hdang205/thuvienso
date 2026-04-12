import pytest
from library.models import User, Book, Loan
from django.utils import timezone
from datetime import timedelta


@pytest.mark.django_db
class TestUserModel:
    def test_user_creation(self, user_factory):
        user = user_factory.create(
            username='testuser',
            email='test@example.com',
            role='student'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == 'student'
        assert str(user) == 'testuser (Sinh viên)'

    def test_librarian_role(self, user_factory):
        user = user_factory.create(role='librarian')
        assert user.role == 'librarian'
        assert str(user) == 'testuser (Thủ thư)'

    def test_user_roles(self):
        """Test that user roles are properly defined"""
        assert User.ROLE_CHOICES == [
            ('student', 'Sinh viên'),
            ('librarian', 'Thủ thư'),
        ]


@pytest.mark.django_db
class TestBookModel:
    def test_book_creation(self, book_factory):
        book = book_factory.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890123',
            category='Fiction',
            total_quantity=5
        )
        assert book.title == 'Test Book'
        assert book.author == 'Test Author'
        assert book.isbn == '1234567890123'
        assert book.category == 'Fiction'
        assert book.total_quantity == 5
        assert book.available_quantity == 5
        assert str(book) == 'Test Book by Test Author'

    def test_book_with_description(self, book_factory):
        book = book_factory.create(
            description='A great book about testing'
        )
        assert book.description == 'A great book about testing'

    def test_book_ordering(self, book_factory):
        book1 = book_factory.create(title='Book A')
        book2 = book_factory.create(title='Book B')

        books = list(Book.objects.all())
        assert books[0].title == 'Book A'
        assert books[1].title == 'Book B'


@pytest.mark.django_db
class TestLoanModel:
    def test_loan_creation(self, user_factory, book_factory):
        user = user_factory.create()
        book = book_factory.create()
        due_date = timezone.now() + timedelta(days=14)

        loan = Loan.objects.create(
            user=user,
            book=book,
            due_date=due_date
        )

        assert loan.user == user
        assert loan.book == book
        assert loan.status == 'borrowed'
        assert loan.return_date is None
        assert str(loan) == f'{user.username} - {book.title} (Đang mượn)'

    def test_loan_return(self, user_factory, book_factory):
        user = user_factory.create()
        book = book_factory.create()
        loan = Loan.objects.create(
            user=user,
            book=book,
            due_date=timezone.now() + timedelta(days=14)
        )

        # Return the book
        loan.status = 'returned'
        loan.return_date = timezone.now()
        loan.save()

        assert loan.status == 'returned'
        assert loan.return_date is not None
        assert str(loan) == f'{user.username} - {book.title} (Đã trả)'

    def test_overdue_loan(self, user_factory, book_factory):
        user = user_factory.create()
        book = book_factory.create()
        # Create loan with due date in the past
        past_date = timezone.now() - timedelta(days=1)

        loan = Loan.objects.create(
            user=user,
            book=book,
            due_date=past_date
        )

        assert loan.status == 'borrowed'
        # Note: We would need to implement a method to check if loan is overdue
        # This could be a model method or property

    def test_loan_status_choices(self):
        """Test that loan status choices are properly defined"""
        assert Loan.STATUS_CHOICES == [
            ('borrowed', 'Đang mượn'),
            ('returned', 'Đã trả'),
            ('overdue', 'Quá hạn'),
        ]