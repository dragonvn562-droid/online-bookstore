import os
from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)
def get_db_password():
    secret_path = '/run/secrets/db_password'
    if os.path.exists(secret_path):
        with open(secret_path, 'r') as f:
            return f.read().strip()
    return os.environ.get('DB_PASSWORD', 'postgres')

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'bookstore'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=get_db_password()  # Sử dụng hàm lấy mật khẩu bảo mật ở trên
    )
    return conn
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(150) NOT NULL,
            author VARCHAR(100) NOT NULL,
            price NUMERIC(10, 2) NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    return jsonify({"message": "Welcome to Online Bookstore API"})

@app.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, title, author, price FROM books;')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": b[0], "title": b[1], "author": b[2], "price": float(b[3])} for b in books])

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO books (title, author, price) VALUES (%s, %s, %s) RETURNING id;',
                (data['title'], data['author'], data['price']))
    book_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": book_id, "title": data['title'], "author": data['author'], "price": data['price']}), 201

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, title, author, price FROM books WHERE id = %s;', (book_id,))
    b = cur.fetchone()
    cur.close()
    conn.close()
    if b is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"id": b[0], "title": b[1], "author": b[2], "price": float(b[3])})

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE books SET title = %s, author = %s, price = %s WHERE id = %s;',
                (data['title'], data['author'], data['price'], book_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Book updated successfully"})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM books WHERE id = %s;', (book_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Book deleted successfully"})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
