# Thư viện số FBU

> Dự án giúp sinh viên tra cứu và mượn trả sách, hỗ trợ thủ thư quản lý kho sách một cách số hóa và tiện lợi.

---

## 1. Giới thiệu tổng quan (Overview)

**Thư viện số FBU** là hệ thống quản lý thư viện số hóa phục vụ Trường Đại học Tài chính - Ngân hàng Hà Nội (FBU). Hệ thống giải quyết các vấn đề:
- Giảm tải thời gian thủ thư quản lý kho sách và theo dõi hạn trả thủ công.
- Giúp sinh viên dễ dàng tìm kiếm sách phù hợp theo chuyên ngành và sở thích.
- Tích hợp trợ lý ảo thông minh (AI Chatbox) gợi ý sách theo từ khóa và chủ đề học tập.
- Theo dõi trạng thái mượn trả và cảnh báo quá hạn chính xác.

---

## 2. Công nghệ sử dụng (Tech Stack)

| Tầng (Layer) | Công nghệ / Thư viện | Ghi chú |
| ------------ | -------------------- | ------- |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla ES6+) | Tối ưu, nhẹ, chuẩn Responsive Mobile/Desktop |
| **Backend** | Python 3.12+, Django 6.x, Django REST Framework | RESTful API, SimpleJWT Token Auth |
| **Database** | SQLite (môi trường Dev), PostgreSQL (Production) | Lưu trữ người dùng, sách và giao dịch mượn trả |
| **DevOps & Deploy** | WhiteNoise, Gunicorn, Docker, Railway, GitHub Actions | CI/CD build & test tự động, GitHub Pages |
| **Testing** | Pytest, Pytest-Django, Vitest | Unit & Integration tests |

---

## 3. Cài đặt và Chạy hệ thống (Getting Started)

### 3.1 Yêu cầu môi trường (Prerequisites)
- **Node.js**: v18+ và **npm**
- **Python**: v3.12+ (kèm `pip`)

### 3.2 Cài đặt Backend
```bash
# 1. Cài đặt thư viện Python
pip install -r requirements.txt

# 2. Khởi tạo cơ sở dữ liệu
python manage.py migrate

# 3. Tạo dữ liệu mẫu (nếu cần)
python populate_data.py

# 4. Khởi động Backend API server (mặc định cổng 8000)
python manage.py runserver
```
Backend API sẽ hoạt động tại: `http://127.0.0.1:8000/api/`  
Trang quản trị Django Admin: `http://127.0.0.1:8000/admin/`  
Kiểm tra sức khỏe hệ thống: `http://127.0.0.1:8000/health/`

### 3.3 Cài đặt Frontend
```bash
# 1. Cài đặt npm dependencies
npm install

# 2. Khởi động Frontend dev server (cổng 3000)
npm run dev
```
Trình duyệt sẽ mở giao diện tại: `http://localhost:3000`

---

## 4. Kiểm thử & Đóng gói (Testing & Build)

### Kiểm thử Backend (Pytest):
```bash
pytest
```
Chạy toàn bộ 38 test cases (Auth, Book, Loan, Chat Recommendation, Inventory Consistency) với độ bao phủ > 80%.

### Kiểm thử Frontend (Vitest):
```bash
npm test
```

### Kiểm tra cú pháp (Lint):
```bash
npm run lint
```

### Đóng gói Production (Build):
```bash
npm run build
```
Mã nguồn frontend sau khi build sẽ được đóng gói tự động vào thư mục `/dist`.

---

## 5. Cấu trúc thư mục (Project Structure)

```
thuvienso-master/
├── library/                 # Ứng dụng Django cốt lõi (Models, Views, Serializers, Permissions)
├── thuvienso_backend/       # Cấu hình Django Project (settings, urls, wsgi, asgi)
├── src/                     # Mã nguồn Frontend (index.html, app.js, chatbox.js, styles.css)
├── dist/                    # Bản build production của Frontend
├── tests/                   # Bộ test suite cho Backend (test_api, test_models) & Frontend
├── scripts/                 # Kịch bản hỗ trợ build cross-platform
├── docs/                    # Tài liệu kỹ thuật & hướng dẫn sử dụng
├── manage.py                # Điểm khởi chạy Django CLI
├── requirements.txt         # Danh sách dependencies Python
├── package.json             # Cấu hình dependencies & scripts npm
└── db.sqlite3               # Cơ sở dữ liệu SQLite phát triển cục bộ
```

---

## 6. Biến môi trường (Environment Variables)

| Tên biến | Mặc định | Mô tả |
| -------- | -------- | ----- |
| `SECRET_KEY` | Development key | Khóa bảo mật của Django |
| `DEBUG` | `True` | Bật/tắt chế độ debug |
| `DATABASE_URL` | None (dùng SQLite) | URL kết nối PostgreSQL (vd: Railway) |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Danh sách hosts được phép truy cập |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000` | Danh sách domain frontend được phép gọi API |
