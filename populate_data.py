import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thuvienso_backend.settings')
django.setup()

from library.models import User, Book, Loan

def create_sample_data():
    # Create sample users
    if not User.objects.filter(username='student1').exists():
        User.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='password123',
            first_name='Nguyen',
            last_name='Van A',
            role='student',
            student_id='2024001'
        )

    if not User.objects.filter(username='librarian1').exists():
        User.objects.create_user(
            username='librarian1',
            email='librarian1@example.com',
            password='password123',
            first_name='Tran',
            last_name='Thi B',
            role='librarian'
        )

    # Create sample books
    books_data = [
        {
            'title': 'Python Programming',
            'author': 'John Smith',
            'isbn': '9780123456789',
            'category': 'Programming',
            'description': 'Learn Python programming',
            'total_quantity': 5,
            'available_quantity': 5
        },
        {
            'title': 'Django Web Development',
            'author': 'Jane Doe',
            'isbn': '9780987654321',
            'category': 'Web Development',
            'description': 'Build web apps with Django',
            'total_quantity': 3,
            'available_quantity': 3
        },
        {
            'title': 'Data Structures and Algorithms',
            'author': 'Bob Johnson',
            'isbn': '9781122334455',
            'category': 'Computer Science',
            'description': 'Fundamental data structures',
            'total_quantity': 2,
            'available_quantity': 2
        }
    ]

    for book_data in books_data:
        if not Book.objects.filter(isbn=book_data['isbn']).exists():
            Book.objects.create(**book_data)

    print("Sample data created successfully!")

if __name__ == '__main__':
    create_sample_data()