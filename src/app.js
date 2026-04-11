// Thư viện số FBU - Frontend JavaScript

const API_BASE = 'http://localhost:8000/api';

// Global state
let books = [];
let users = [];
let loans = [];

// Load data on page load
document.addEventListener('DOMContentLoaded', function () {
  loadBooks();
  loadUsers();
  loadLoans();

  // Add event listeners
  document
    .getElementById('add-book-btn')
    .addEventListener('click', showAddBookForm);
  document
    .getElementById('search-books')
    .addEventListener('input', filterBooks);
});

// API helper functions
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    alert('Có lỗi xảy ra khi kết nối với server. Vui lòng thử lại.');
    return null;
  }
}

// Load books from API
async function loadBooks() {
  const data = await apiRequest('/books/');
  if (data) {
    books = data;
    displayBooks(books);
  }
}

// Display books in the UI
function displayBooks(booksToShow) {
  const booksList = document.getElementById('books-list');
  booksList.innerHTML = '<h3>Danh sách sách</h3>';

  if (booksToShow.length === 0) {
    booksList.innerHTML += '<p>Không có sách nào.</p>';
    return;
  }

  // Add search input
  booksList.innerHTML += `
        <div class="search-container">
            <input type="text" id="search-books" placeholder="Tìm kiếm sách...">
        </div>
    `;

  const booksContainer = document.createElement('div');
  booksContainer.className = 'books-container';

  booksToShow.forEach((book) => {
    const bookCard = document.createElement('div');
    bookCard.className = 'book-card';
    bookCard.innerHTML = `
            <h4>${book.title}</h4>
            <p><strong>Tác giả:</strong> ${book.author}</p>
            <p><strong>Thể loại:</strong> ${book.category}</p>
            <p><strong>ISBN:</strong> ${book.isbn}</p>
            <p><strong>Số lượng:</strong> ${book.available_quantity}/${book.total_quantity}</p>
            <div class="book-actions">
                <button onclick="editBook(${book.id})">Sửa</button>
                <button onclick="deleteBook(${book.id})" class="delete-btn">Xóa</button>
            </div>
        `;
    booksContainer.appendChild(bookCard);
  });

  booksList.appendChild(booksContainer);
}

// Filter books based on search
function filterBooks() {
  const searchTerm = document
    .getElementById('search-books')
    .value.toLowerCase();
  const filteredBooks = books.filter(
    (book) =>
      book.title.toLowerCase().includes(searchTerm) ||
      book.author.toLowerCase().includes(searchTerm) ||
      book.category.toLowerCase().includes(searchTerm)
  );
  displayBooks(filteredBooks);
}

// Show add book form
function showAddBookForm() {
  const formHtml = `
        <div id="book-form-modal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal()">&times;</span>
                <h3>Thêm sách mới</h3>
                <form id="add-book-form">
                    <label for="title">Tên sách:</label>
                    <input type="text" id="title" required>

                    <label for="author">Tác giả:</label>
                    <input type="text" id="author" required>

                    <label for="isbn">ISBN:</label>
                    <input type="text" id="isbn" required>

                    <label for="category">Thể loại:</label>
                    <input type="text" id="category" required>

                    <label for="description">Mô tả:</label>
                    <textarea id="description"></textarea>

                    <label for="total_quantity">Số lượng:</label>
                    <input type="number" id="total_quantity" min="1" value="1" required>

                    <button type="submit">Thêm sách</button>
                </form>
            </div>
        </div>
    `;

  document.body.insertAdjacentHTML('beforeend', formHtml);
  document
    .getElementById('add-book-form')
    .addEventListener('submit', handleAddBook);
}

// Handle add book form submission
async function handleAddBook(event) {
  event.preventDefault();

  const bookData = {
    title: document.getElementById('title').value,
    author: document.getElementById('author').value,
    isbn: document.getElementById('isbn').value,
    category: document.getElementById('category').value,
    description: document.getElementById('description').value,
    total_quantity: parseInt(document.getElementById('total_quantity').value),
  };

  const result = await apiRequest('/books/', {
    method: 'POST',
    body: JSON.stringify(bookData),
  });

  if (result) {
    alert('Thêm sách thành công!');
    closeModal();
    loadBooks(); // Reload books list
  }
}

// Edit book
function editBook(bookId) {
  const book = books.find((b) => b.id === bookId);
  if (!book) return;

  // Similar to add form but pre-filled
  const formHtml = `
        <div id="book-form-modal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal()">&times;</span>
                <h3>Sửa thông tin sách</h3>
                <form id="edit-book-form">
                    <input type="hidden" id="book-id" value="${book.id}">

                    <label for="title">Tên sách:</label>
                    <input type="text" id="title" value="${book.title}" required>

                    <label for="author">Tác giả:</label>
                    <input type="text" id="author" value="${book.author}" required>

                    <label for="isbn">ISBN:</label>
                    <input type="text" id="isbn" value="${book.isbn}" required>

                    <label for="category">Thể loại:</label>
                    <input type="text" id="category" value="${book.category}" required>

                    <label for="description">Mô tả:</label>
                    <textarea id="description">${book.description || ''}</textarea>

                    <label for="total_quantity">Số lượng:</label>
                    <input type="number" id="total_quantity" min="1" value="${book.total_quantity}" required>

                    <button type="submit">Cập nhật</button>
                </form>
            </div>
        </div>
    `;

  document.body.insertAdjacentHTML('beforeend', formHtml);
  document
    .getElementById('edit-book-form')
    .addEventListener('submit', handleEditBook);
}

// Handle edit book form submission
async function handleEditBook(event) {
  event.preventDefault();

  const bookId = document.getElementById('book-id').value;
  const bookData = {
    title: document.getElementById('title').value,
    author: document.getElementById('author').value,
    isbn: document.getElementById('isbn').value,
    category: document.getElementById('category').value,
    description: document.getElementById('description').value,
    total_quantity: parseInt(document.getElementById('total_quantity').value),
  };

  const result = await apiRequest(`/books/${bookId}/`, {
    method: 'PUT',
    body: JSON.stringify(bookData),
  });

  if (result) {
    alert('Cập nhật sách thành công!');
    closeModal();
    loadBooks();
  }
}

// Delete book
async function deleteBook(bookId) {
  if (!confirm('Bạn có chắc muốn xóa sách này?')) return;

  const result = await apiRequest(`/books/${bookId}/`, {
    method: 'DELETE',
  });

  if (result !== null) {
    // DELETE returns no content
    alert('Xóa sách thành công!');
    loadBooks();
  }
}

// Close modal
function closeModal() {
  const modal = document.getElementById('book-form-modal');
  if (modal) {
    modal.remove();
  }
}

// Load users
async function loadUsers() {
  const data = await apiRequest('/users/');
  if (data) {
    users = data;
    displayUsers(users);
  }
}

// Display users
function displayUsers(usersToShow) {
  const usersList = document.getElementById('users-list');
  usersList.innerHTML = '<h3>Danh sách người dùng</h3>';

  if (usersToShow.length === 0) {
    usersList.innerHTML += '<p>Không có người dùng nào.</p>';
    return;
  }

  usersToShow.forEach((user) => {
    const userDiv = document.createElement('div');
    userDiv.innerHTML = `<p><strong>${user.username}</strong> (${user.role}) - ${user.email}</p>`;
    usersList.appendChild(userDiv);
  });
}

// Load loans
async function loadLoans() {
  const data = await apiRequest('/loans/');
  if (data) {
    loans = data;
    displayLoans(loans);
  }
}

// Display loans
function displayLoans(loansToShow) {
  const loansList = document.getElementById('loans-list');
  loansList.innerHTML = '<h3>Danh sách mượn trả</h3>';

  if (loansToShow.length === 0) {
    loansList.innerHTML += '<p>Không có giao dịch mượn trả nào.</p>';
    return;
  }

  loansToShow.forEach((loan) => {
    const loanDiv = document.createElement('div');
    loanDiv.innerHTML = `
            <p><strong>${loan.book.title}</strong> - ${loan.user.username}</p>
            <p>Trạng thái: ${loan.status} | Hạn trả: ${new Date(
              loan.due_date
            ).toLocaleDateString('vi-VN')}</p>
        `;
    loansList.appendChild(loanDiv);
  });
}

// Load users
async function loadUsers() {
  // TODO: Implement users API
  const usersList = document.getElementById('users-list');
  usersList.innerHTML = '<h3>Danh sách người dùng</h3><p>Chưa triển khai</p>';
}

// Load loans
async function loadLoans() {
  // TODO: Implement loans API
  const loansList = document.getElementById('loans-list');
  loansList.innerHTML = '<h3>Danh sách mượn trả</h3><p>Chưa triển khai</p>';
}
