// Thư viện số FBU - Frontend JavaScript

// Import configuration from config.js
let API_BASE = 'http://localhost:8000/api';
if (typeof window !== 'undefined' && typeof window.API_BASE !== 'undefined') {
  API_BASE = window.API_BASE;
}

// Global state
let books = [];
let users = [];
let loans = [];
let currentUser = null;
let accessToken = null;
let refreshToken = null;
let activeTab = 'books';

// Load data on page load
document.addEventListener('DOMContentLoaded', function () {
  initializeApp();
});

// Toast notification helper
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Initialize app
function initializeApp() {
  loadTokensFromStorage();
  setupAuthEventListeners();
  setupDataEventListeners();
  setupTabNavigation();
  updateAuthUI();

  if (accessToken) {
    loadData();
  }
}

// Setup Tab Navigation
function setupTabNavigation() {
  const tabLinks = document.querySelectorAll('.nav-link');
  tabLinks.forEach((link) => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const tab = link.getAttribute('data-tab');
      switchTab(tab);
    });
  });
}

function switchTab(tabName) {
  activeTab = tabName;
  const sections = ['books', 'loans', 'users'];
  sections.forEach((sec) => {
    const el = document.getElementById(sec);
    if (el) el.style.display = sec === tabName ? 'block' : 'none';
  });

  const links = document.querySelectorAll('.nav-link');
  links.forEach((link) => {
    if (link.getAttribute('data-tab') === tabName) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

// Authentication Event Listeners
function setupAuthEventListeners() {
  const loginBtn = document.getElementById('login-btn');
  const regBtn = document.getElementById('register-btn');
  const logoutBtn = document.getElementById('logout-btn');
  const tabLoginBtn = document.getElementById('tab-login-btn');
  const tabRegBtn = document.getElementById('tab-reg-btn');

  if (loginBtn) loginBtn.addEventListener('click', showLoginForm);
  if (regBtn) regBtn.addEventListener('click', showRegisterForm);
  if (logoutBtn) logoutBtn.addEventListener('click', logout);
  if (tabLoginBtn) tabLoginBtn.addEventListener('click', showLoginForm);
  if (tabRegBtn) tabRegBtn.addEventListener('click', showRegisterForm);

  const loginForm = document.getElementById('login-form');
  const regForm = document.getElementById('register-form');
  if (loginForm) loginForm.addEventListener('submit', handleLogin);
  if (regForm) regForm.addEventListener('submit', handleRegister);
}

// Data Event Listeners
function setupDataEventListeners() {
  const addBookBtn = document.getElementById('add-book-btn');
  const searchInput = document.getElementById('search-books');
  const borrowBtn = document.getElementById('borrow-book-btn');

  if (addBookBtn) addBookBtn.addEventListener('click', showAddBookForm);
  if (searchInput) searchInput.addEventListener('input', filterBooks);
  if (borrowBtn) borrowBtn.addEventListener('click', showBorrowBookForm);
}

function loadTokensFromStorage() {
  accessToken = localStorage.getItem('accessToken');
  refreshToken = localStorage.getItem('refreshToken');
  const userData = localStorage.getItem('currentUser');
  if (userData) {
    try {
      currentUser = JSON.parse(userData);
    } catch {
      currentUser = null;
    }
  }
}

function saveTokensToStorage(access, refresh, user) {
  accessToken = access;
  refreshToken = refresh;
  currentUser = user;
  localStorage.setItem('accessToken', access);
  localStorage.setItem('refreshToken', refresh);
  localStorage.setItem('currentUser', JSON.stringify(user));

  if (window.chatbox) {
    window.chatbox.accessToken = access;
  }
}

function clearTokensFromStorage() {
  accessToken = null;
  refreshToken = null;
  currentUser = null;
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  localStorage.removeItem('currentUser');

  if (window.chatbox) {
    window.chatbox.accessToken = null;
  }
}

function updateAuthUI() {
  const navLinks = document.getElementById('nav-links');
  const authForms = document.getElementById('auth-forms');
  const userInfo = document.getElementById('user-info');
  const loginBtn = document.getElementById('login-btn');
  const registerBtn = document.getElementById('register-btn');
  const logoutBtn = document.getElementById('logout-btn');
  const addBookBtn = document.getElementById('add-book-btn');
  const usersNavLink = document.getElementById('users-nav-link');
  const loansTitle = document.getElementById('loans-title');

  if (currentUser && accessToken) {
    const isLibrarian = currentUser.role === 'librarian';
    userInfo.textContent = `Xin chào, ${currentUser.first_name || ''} ${currentUser.last_name || currentUser.username} (${isLibrarian ? 'Thủ thư' : 'Sinh viên'})`;
    loginBtn.style.display = 'none';
    registerBtn.style.display = 'none';
    logoutBtn.style.display = 'inline-flex';
    navLinks.style.display = 'flex';
    authForms.style.display = 'none';

    if (addBookBtn) addBookBtn.style.display = isLibrarian ? 'inline-flex' : 'none';
    if (usersNavLink) usersNavLink.style.display = isLibrarian ? 'inline-block' : 'none';
    if (loansTitle) {
      loansTitle.textContent = isLibrarian ? 'Quản lý mượn trả sách' : 'Lịch sử mượn trả sách của tôi';
    }

    switchTab(activeTab || 'books');
  } else {
    userInfo.textContent = '';
    loginBtn.style.display = 'inline-flex';
    registerBtn.style.display = 'inline-flex';
    logoutBtn.style.display = 'none';
    navLinks.style.display = 'none';
    authForms.style.display = 'block';

    document.getElementById('books').style.display = 'none';
    document.getElementById('users').style.display = 'none';
    document.getElementById('loans').style.display = 'none';
  }
}

function showLoginForm() {
  document.getElementById('login-form-container').style.display = 'block';
  document.getElementById('register-form-container').style.display = 'none';
  const tabLogin = document.getElementById('tab-login-btn');
  const tabReg = document.getElementById('tab-reg-btn');
  if (tabLogin) tabLogin.classList.add('active');
  if (tabReg) tabReg.classList.remove('active');
}

function showRegisterForm() {
  document.getElementById('login-form-container').style.display = 'none';
  document.getElementById('register-form-container').style.display = 'block';
  const tabLogin = document.getElementById('tab-login-btn');
  const tabReg = document.getElementById('tab-reg-btn');
  if (tabLogin) tabLogin.classList.remove('active');
  if (tabReg) tabReg.classList.add('active');
}

async function handleLogin(event) {
  event.preventDefault();

  const username = document.getElementById('login-username').value.trim();
  const password = document.getElementById('login-password').value;

  const result = await apiRequest('/auth/login/', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });

  if (result && result.access) {
    saveTokensToStorage(result.access, result.refresh, result.user);
    updateAuthUI();
    loadData();
    showToast('Đăng nhập thành công!', 'success');
  }
}

async function handleRegister(event) {
  event.preventDefault();

  const password = document.getElementById('reg-password').value;
  const passwordConfirm = document.getElementById('reg-password-confirm').value;

  if (password !== passwordConfirm) {
    showToast('Mật khẩu xác nhận không khớp!', 'error');
    return;
  }

  const data = {
    username: document.getElementById('reg-username').value.trim(),
    email: document.getElementById('reg-email').value.trim(),
    password: password,
    password_confirm: passwordConfirm,
    first_name: document.getElementById('reg-first-name').value.trim(),
    last_name: document.getElementById('reg-last-name').value.trim(),
    role: document.getElementById('reg-role').value,
  };

  const result = await apiRequest('/auth/register/', {
    method: 'POST',
    body: JSON.stringify(data),
  });

  if (result && result.access) {
    saveTokensToStorage(result.access, result.refresh, result.user);
    updateAuthUI();
    loadData();
    showToast('Đăng ký tài khoản thành công!', 'success');
  }
}

async function logout() {
  if (refreshToken) {
    await apiRequest('/auth/logout/', {
      method: 'POST',
      body: JSON.stringify({ refresh: refreshToken }),
    });
  }

  clearTokensFromStorage();
  updateAuthUI();
  showToast('Đã đăng xuất an toàn.', 'info');
}

// Load data after authentication
function loadData() {
  loadBooks();
  if (currentUser && currentUser.role === 'librarian') {
    loadUsers();
  }
  loadLoans();
}

// API helper functions
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  };

  if (accessToken) {
    config.headers['Authorization'] = `Bearer ${accessToken}`;
  }

  try {
    const response = await fetch(url, config);
    if (!response.ok) {
      if (response.status === 401) {
        clearTokensFromStorage();
        updateAuthUI();
        showToast('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.', 'error');
        return null;
      }
      const errData = await response.json().catch(() => null);
      const errMsg = (errData && (errData.error || errData.detail)) || `Lỗi HTTP ${response.status}`;
      showToast(errMsg, 'error');
      return null;
    }
    if (response.status === 204) {
      return {};
    }
    return await response.json();
  } catch {
    showToast('Không thể kết nối đến máy chủ. Vui lòng kiểm tra lại mạng!', 'error');
    return null;
  }
}

// Load books from API
async function loadBooks() {
  const booksList = document.getElementById('books-list');
  if (booksList) {
    booksList.innerHTML = '<div class="empty-state"><p>Đang tải danh sách sách...</p></div>';
  }

  const data = await apiRequest('/books/');
  if (data) {
    books = Array.isArray(data) ? data : data.results || [];
    displayBooks(books);
  }
}

// Display books in UI
function displayBooks(booksToShow) {
  const booksList = document.getElementById('books-list');
  if (!booksList) return;

  if (booksToShow.length === 0) {
    booksList.innerHTML = '<div class="empty-state"><p>Không tìm thấy sách nào phù hợp.</p></div>';
    return;
  }

  const isLibrarian = currentUser && currentUser.role === 'librarian';
  let html = '<div class="books-container">';

  booksToShow.forEach((book) => {
    const isAvailable = book.available_quantity > 0;
    const stockClass = isAvailable ? 'available' : 'empty';
    const stockText = isAvailable
      ? `Còn ${book.available_quantity}/${book.total_quantity} cuốn`
      : 'Đã hết sách';

    let actionButtons = '';
    if (isLibrarian) {
      actionButtons = `
        <button class="btn btn-secondary" onclick="window.editBook(${book.id})">Sửa</button>
        <button class="btn btn-danger" onclick="window.deleteBook(${book.id})">Xóa</button>
      `;
    } else {
      actionButtons = isAvailable
        ? `<button class="btn btn-success" onclick="window.borrowDirect(${book.id})">Mượn sách</button>`
        : `<button class="btn btn-secondary" disabled style="opacity: 0.6; cursor: not-allowed;">Hết sách</button>`;
    }

    html += `
      <div class="book-card">
        <span class="book-badge">${escapeHtml(book.category || 'Khác')}</span>
        <h4>${escapeHtml(book.title)}</h4>
        <p><strong>Tác giả:</strong> ${escapeHtml(book.author || 'N/A')}</p>
        <p><strong>ISBN:</strong> ${escapeHtml(book.isbn || 'N/A')}</p>
        ${book.description ? `<p style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">${escapeHtml(book.description)}</p>` : ''}
        <p class="book-stock ${stockClass}">${stockText}</p>
        <div class="book-actions">
          ${actionButtons}
        </div>
      </div>
    `;
  });

  html += '</div>';
  booksList.innerHTML = html;
}

// Filter books
function filterBooks() {
  const input = document.getElementById('search-books');
  if (!input) return;
  const term = input.value.trim().toLowerCase();
  if (!term) {
    displayBooks(books);
    return;
  }

  const filtered = books.filter(
    (b) =>
      (b.title && b.title.toLowerCase().includes(term)) ||
      (b.author && b.author.toLowerCase().includes(term)) ||
      (b.category && b.category.toLowerCase().includes(term)) ||
      (b.isbn && b.isbn.toLowerCase().includes(term))
  );
  displayBooks(filtered);
}

// Show Add Book Modal
function showAddBookForm() {
  closeModal();
  const formHtml = `
    <div id="book-form-modal" class="modal">
      <div class="modal-content">
        <span class="close" onclick="window.closeModal()">&times;</span>
        <h3 style="margin-top:0;">Thêm sách mới vào thư viện</h3>
        <form id="add-book-form">
          <label for="title">Tên sách:</label>
          <input type="text" id="title" required placeholder="Nhập tên sách..." />

          <label for="author">Tác giả:</label>
          <input type="text" id="author" required placeholder="Nhập tên tác giả..." />

          <label for="isbn">ISBN (10-13 chữ số):</label>
          <input type="text" id="isbn" required placeholder="Ví dụ: 9781234567890" />

          <label for="category">Thể loại:</label>
          <input type="text" id="category" required placeholder="Khoa học, Lập trình, Kinh tế..." />

          <label for="description">Mô tả tóm tắt:</label>
          <textarea id="description" rows="3" placeholder="Mô tả nội dung sách..."></textarea>

          <label for="total_quantity">Tổng số lượng nhập kho:</label>
          <input type="number" id="total_quantity" min="1" value="1" required />

          <div style="display:flex; justify-content:flex-end; gap:0.5rem; margin-top:1rem;">
            <button type="button" class="btn btn-secondary" onclick="window.closeModal()">Hủy</button>
            <button type="submit" class="btn btn-primary">Lưu sách</button>
          </div>
        </form>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', formHtml);
  document.getElementById('add-book-form').addEventListener('submit', handleAddBook);
}

// Handle Add Book
async function handleAddBook(event) {
  event.preventDefault();

  const totalQty = parseInt(document.getElementById('total_quantity').value, 10) || 1;
  const bookData = {
    title: document.getElementById('title').value.trim(),
    author: document.getElementById('author').value.trim(),
    isbn: document.getElementById('isbn').value.trim(),
    category: document.getElementById('category').value.trim(),
    description: document.getElementById('description').value.trim(),
    total_quantity: totalQty,
    available_quantity: totalQty,
  };

  const result = await apiRequest('/books/', {
    method: 'POST',
    body: JSON.stringify(bookData),
  });

  if (result) {
    showToast('Thêm sách mới thành công!', 'success');
    closeModal();
    loadBooks();
  }
}

// Edit Book
function editBook(bookId) {
  closeModal();
  const book = books.find((b) => b.id === bookId);
  if (!book) return;

  const formHtml = `
    <div id="book-form-modal" class="modal">
      <div class="modal-content">
        <span class="close" onclick="window.closeModal()">&times;</span>
        <h3 style="margin-top:0;">Sửa thông tin sách</h3>
        <form id="edit-book-form">
          <input type="hidden" id="book-id" value="${book.id}">

          <label for="title">Tên sách:</label>
          <input type="text" id="title" value="${escapeHtml(book.title)}" required />

          <label for="author">Tác giả:</label>
          <input type="text" id="author" value="${escapeHtml(book.author)}" required />

          <label for="isbn">ISBN:</label>
          <input type="text" id="isbn" value="${escapeHtml(book.isbn)}" required />

          <label for="category">Thể loại:</label>
          <input type="text" id="category" value="${escapeHtml(book.category)}" required />

          <label for="description">Mô tả:</label>
          <textarea id="description" rows="3">${escapeHtml(book.description || '')}</textarea>

          <label for="total_quantity">Tổng số lượng:</label>
          <input type="number" id="total_quantity" min="1" value="${book.total_quantity}" required />

          <div style="display:flex; justify-content:flex-end; gap:0.5rem; margin-top:1rem;">
            <button type="button" class="btn btn-secondary" onclick="window.closeModal()">Hủy</button>
            <button type="submit" class="btn btn-primary">Cập nhật</button>
          </div>
        </form>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', formHtml);
  document.getElementById('edit-book-form').addEventListener('submit', handleEditBook);
}

async function handleEditBook(event) {
  event.preventDefault();

  const bookId = document.getElementById('book-id').value;
  const bookData = {
    title: document.getElementById('title').value.trim(),
    author: document.getElementById('author').value.trim(),
    isbn: document.getElementById('isbn').value.trim(),
    category: document.getElementById('category').value.trim(),
    description: document.getElementById('description').value.trim(),
    total_quantity: parseInt(document.getElementById('total_quantity').value, 10),
  };

  const result = await apiRequest(`/books/${bookId}/`, {
    method: 'PATCH',
    body: JSON.stringify(bookData),
  });

  if (result) {
    showToast('Cập nhật thông tin sách thành công!', 'success');
    closeModal();
    loadBooks();
  }
}

// Delete Book
async function deleteBook(bookId) {
  if (!confirm('Bạn có chắc chắn muốn xóa cuốn sách này khỏi hệ thống?')) return;

  const result = await apiRequest(`/books/${bookId}/`, {
    method: 'DELETE',
  });

  if (result !== null) {
    showToast('Đã xóa sách thành công.', 'info');
    loadBooks();
  }
}

// Direct Borrow Button from card
function borrowDirect(bookId) {
  showBorrowBookForm(bookId);
}

// Close modal helper
function closeModal() {
  const bookModal = document.getElementById('book-form-modal');
  if (bookModal) bookModal.remove();
  const borrowModal = document.getElementById('borrow-form-modal');
  if (borrowModal) borrowModal.remove();
}

// Show borrow book form
function showBorrowBookForm(preSelectedBookId = null) {
  closeModal();
  const today = new Date();
  const defaultDue = new Date(today.getTime() + 14 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

  const formHtml = `
    <div id="borrow-form-modal" class="modal">
      <div class="modal-content">
        <span class="close" onclick="window.closeModal()">&times;</span>
        <h3 style="margin-top:0;">Mượn sách</h3>
        <form id="borrow-book-form">
          <label for="borrow-book-select">Chọn sách mượn:</label>
          <select id="borrow-book-select" required>
            <option value="">-- Chọn sách --</option>
          </select>

          <label for="borrow-due-date">Hạn trả dự kiến:</label>
          <input type="date" id="borrow-due-date" value="${defaultDue}" required />

          <div style="display:flex; justify-content:flex-end; gap:0.5rem; margin-top:1rem;">
            <button type="button" class="btn btn-secondary" onclick="window.closeModal()">Hủy</button>
            <button type="submit" class="btn btn-success">Xác nhận mượn</button>
          </div>
        </form>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', formHtml);
  populateAvailableBooks(preSelectedBookId);
  document.getElementById('borrow-book-form').addEventListener('submit', handleBorrowBook);
}

// Populate Available Books
async function populateAvailableBooks(selectedId = null) {
  const select = document.getElementById('borrow-book-select');
  if (!select) return;

  while (select.options.length > 1) {
    select.remove(1);
  }

  books.forEach((book) => {
    if (book.available_quantity > 0) {
      const option = document.createElement('option');
      option.value = book.id;
      option.textContent = `${book.title} (${book.author}) - Còn ${book.available_quantity}`;
      if (selectedId && book.id === selectedId) {
        option.selected = true;
      }
      select.appendChild(option);
    }
  });
}

// Handle Borrow Book
async function handleBorrowBook(event) {
  event.preventDefault();

  const bookId = document.getElementById('borrow-book-select').value;
  const dueDate = document.getElementById('borrow-due-date').value;

  if (!bookId) {
    showToast('Vui lòng chọn sách cần mượn!', 'error');
    return;
  }

  const data = { book_id: parseInt(bookId, 10) };
  if (dueDate) {
    data.due_date = dueDate;
  }

  const result = await apiRequest('/loans/borrow/', {
    method: 'POST',
    body: JSON.stringify(data),
  });

  if (result) {
    showToast('Mượn sách thành công! Vui lòng trả sách đúng hạn.', 'success');
    closeModal();
    loadLoans();
    loadBooks();
  }
}

// Return Book
async function returnBook(loanId) {
  if (!confirm('Xác nhận bạn muốn trả cuốn sách này?')) return;

  const result = await apiRequest(`/loans/${loanId}/return_book/`, {
    method: 'POST',
  });

  if (result) {
    showToast('Trả sách thành công! Cảm ơn bạn.', 'success');
    loadLoans();
    loadBooks();
  }
}

// Load Users (Librarian only)
async function loadUsers() {
  const usersList = document.getElementById('users-list');
  if (!usersList) return;

  usersList.innerHTML = '<div class="empty-state"><p>Đang tải danh sách người dùng...</p></div>';
  const data = await apiRequest('/users/');
  if (data) {
    users = Array.isArray(data) ? data : data.results || [];
    displayUsers(users);
  }
}

function displayUsers(usersToShow) {
  const usersList = document.getElementById('users-list');
  if (!usersList) return;

  if (usersToShow.length === 0) {
    usersList.innerHTML = '<div class="empty-state"><p>Chưa có người dùng nào.</p></div>';
    return;
  }

  let html = `
    <div class="users-table-container">
      <table class="users-table">
        <thead>
          <tr>
            <th>Tên đăng nhập</th>
            <th>Họ và tên</th>
            <th>Email</th>
            <th>Vai trò</th>
            <th>Mã sinh viên</th>
          </tr>
        </thead>
        <tbody>
  `;

  usersToShow.forEach((u) => {
    const roleName = u.role === 'librarian' ? 'Thủ thư' : 'Sinh viên';
    html += `
      <tr>
        <td><strong>${escapeHtml(u.username)}</strong></td>
        <td>${escapeHtml((u.first_name || '') + ' ' + (u.last_name || ''))}</td>
        <td>${escapeHtml(u.email || '-')}</td>
        <td><span class="status-badge status-borrowed">${roleName}</span></td>
        <td>${escapeHtml(u.student_id || '-')}</td>
      </tr>
    `;
  });

  html += '</tbody></table></div>';
  usersList.innerHTML = html;
}

// Load Loans
async function loadLoans() {
  const loansList = document.getElementById('loans-list');
  if (loansList) {
    loansList.innerHTML = '<div class="empty-state"><p>Đang tải lịch sử mượn trả...</p></div>';
  }

  let data;
  if (currentUser && currentUser.role === 'student') {
    data = await apiRequest('/loans/my_loans/');
  } else {
    data = await apiRequest('/loans/');
  }

  if (data) {
    loans = Array.isArray(data) ? data : data.results || [];
    displayLoans(loans);
  }
}

// Display Loans
function displayLoans(loansToShow) {
  const loansList = document.getElementById('loans-list');
  if (!loansList) return;

  if (loansToShow.length === 0) {
    loansList.innerHTML = '<div class="empty-state"><p>Chưa có lượt mượn trả nào được ghi nhận.</p></div>';
    return;
  }

  let html = '<div class="loans-container">';

  loansToShow.forEach((loan) => {
    const isOverdue = loan.is_overdue;
    const statusText =
      loan.status === 'borrowed'
        ? isOverdue
          ? 'Quá hạn'
          : 'Đang mượn'
        : loan.status === 'returned'
          ? 'Đã trả'
          : 'Quá hạn';

    const statusBadgeClass =
      loan.status === 'returned'
        ? 'status-returned'
        : isOverdue
          ? 'status-overdue'
          : 'status-borrowed';

    const loanDate = loan.loan_date ? new Date(loan.loan_date).toLocaleDateString('vi-VN') : '-';
    const dueDate = loan.due_date ? new Date(loan.due_date).toLocaleDateString('vi-VN') : '-';
    const returnDate = loan.return_date ? new Date(loan.return_date).toLocaleDateString('vi-VN') : 'Chưa trả';

    const borrowerName = loan.user
      ? `${loan.user.first_name || ''} ${loan.user.last_name || loan.user.username}`
      : 'Ẩn danh';

    html += `
      <div class="loan-card ${isOverdue ? 'overdue' : ''}">
        <h4>${escapeHtml(loan.book ? loan.book.title : 'Sách')}</h4>
        <p><strong>Người mượn:</strong> ${escapeHtml(borrowerName)}</p>
        <p><strong>Ngày mượn:</strong> ${loanDate}</p>
        <p><strong>Hạn trả:</strong> ${dueDate}</p>
        <p><strong>Ngày trả:</strong> ${returnDate}</p>
        <p><strong>Trạng thái:</strong> <span class="status-badge ${statusBadgeClass}">${statusText}</span></p>
        ${isOverdue ? '<p class="overdue-warning">⚠️ Đã quá hạn trả sách!</p>' : ''}
        <div class="loan-actions">
          ${loan.status === 'borrowed' ? `<button class="btn btn-primary" onclick="window.returnBook(${loan.id})">Trả sách</button>` : ''}
        </div>
      </div>
    `;
  });

  html += '</div>';
  loansList.innerHTML = html;
}

// Escape HTML helper
function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Window global bindings
if (typeof window !== 'undefined') {
  window.editBook = editBook;
  window.deleteBook = deleteBook;
  window.returnBook = returnBook;
  window.closeModal = closeModal;
  window.borrowDirect = borrowDirect;
  window.switchTab = switchTab;
  window.filterBooks = filterBooks;
}
