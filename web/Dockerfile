FROM python:3.9-slim

# Tạo system user để tránh chạy bằng quyền root
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# Phân quyền thư mục cho user mới
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5000
CMD ["python", "main.py"]
