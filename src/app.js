// Thư viện số FBU - Frontend JavaScript

const API_BASE = "http://localhost:8000/api";

// Load books on page load
document.addEventListener("DOMContentLoaded", function () {
  loadBooks();
  loadUsers();
  loadLoans();

  // Add event listeners
  document.getElementById("add-book-btn").addEventListener("click", addBook);
});

// Load books from API
async function loadBooks() {
  try {
    const response = await fetch(`${API_BASE}/books/`);
    const books = await response.json();
    displayBooks(books);
  } catch (error) {
    console.error("Error loading books:", error);
    // Fallback to sample data
    displayBooks([
      { id: 1, title: "Sample Book 1", author: "Author 1" },
      { id: 2, title: "Sample Book 2", author: "Author 2" },
    ]);
  }
}

// Display books in the UI
function displayBooks(books) {
  const booksList = document.getElementById("books-list");
  booksList.innerHTML = "<h3>Danh sách sách</h3>";
  books.forEach((book) => {
    const bookDiv = document.createElement("div");
    bookDiv.innerHTML = `<p><strong>${book.title}</strong> by ${book.author}</p>`;
    booksList.appendChild(bookDiv);
  });
}

// Add new book
function addBook() {
  const title = prompt("Tên sách:");
  const author = prompt("Tác giả:");
  if (title && author) {
    // TODO: Implement API call to add book
    alert("Chức năng thêm sách sẽ được triển khai sau");
  }
}

// Load users
async function loadUsers() {
  // TODO: Implement users API
  const usersList = document.getElementById("users-list");
  usersList.innerHTML = "<h3>Danh sách người dùng</h3><p>Chưa triển khai</p>";
}

// Load loans
async function loadLoans() {
  // TODO: Implement loans API
  const loansList = document.getElementById("loans-list");
  loansList.innerHTML = "<h3>Danh sách mượn trả</h3><p>Chưa triển khai</p>";
}
