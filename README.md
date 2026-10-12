# Đề tài 01 — Dockerized Online Bookstore

## 1. Giới thiệu hệ thống
Hệ thống bán sách trực tuyến đơn giản được đóng gói hoàn toàn bằng Docker, triển khai theo mô hình multi-container gồm các thành phần:
- **nginx**: Web / Reverse Proxy (Cổng truy cập: `8080`).
- **web**: Ứng dụng API (Python Flask) quản lý sách (Thêm, sửa, xóa, xem danh sách).
- **db**: Cơ sở dữ liệu PostgreSQL sử dụng Named Volume để lưu trữ dữ liệu bền vững.

## 2. Các yêu cầu Docker đã thực hiện
1. **Dockerfile**: Xây dựng image tùy chỉnh cho ứng dụng Python Flask.
2. **Docker Compose**: Quản lý và khởi chạy toàn bộ hệ thống (`nginx`, `web`, `db`).
3. **Docker Network**: `bookstore-net` giúp các container giao tiếp nội bộ an toàn.
4. **Named Volume**: `postgres_data` bảo toàn dữ liệu database khi container bị xóa.
5. **Bind Mount**: Ánh xạ thư mục mã nguồn `./web/app` giúp cập nhật code linh hoạt.
6. **Nâng cao**: 
   - **Healthcheck**: Kiểm tra trạng thái sẵn sàng của database trước khi khởi động web.
   - **Docker Secrets**: Bảo mật mật khẩu database thông qua thư mục `secrets/` (mật khẩu: `123`).

## 3. Hướng dẫn triển khai trên Ubuntu
1. Clone mã nguồn về máy và di chuyển vào thư mục dự án:
   ```bash
   cd online-bookstore
