const express = require('express');
const { Pool } = require('pg');

const app = express();
const port = 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

const pool = new Pool({
  user: 'postgres',
  host: 'db',
  database: 'bookstore',
  password: '123',
  port: 5432,
});

async function connectWithRetry() {
  const maxRetries = 30;
  let retries = 0;
  while (retries < maxRetries) {
    try {
      await pool.query('SELECT NOW()');
      console.log("Kết nối cơ sở dữ liệu PostgreSQL thành công!");
      await initDB();
      return;
    } catch (err) {
      retries++;
      console.log(`Đang chờ Database sẵn sàng (Thử lần ${retries}/${maxRetries})...`);
      await new Promise(resolve => setTimeout(resolve, 3000));
    }
  }
  console.error("Không thể kết nối đến cơ sở dữ liệu sau nhiều lần thử.");
}

async function initDB() {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        price NUMERIC NOT NULL
      );
    `);
    console.log("Đã khởi tạo bảng books thành công.");
  } catch (err) {
    console.error("Lỗi khởi tạo bảng:", err);
  }
}

connectWithRetry();

app.get('/', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM books ORDER BY id DESC');
    let html = `
      <h2>Ứng dụng Quản lý Cửa hàng Sách (Docker)</h2>
      <form action="/add" method="POST" style="margin-bottom: 20px;">
        <input type="text" name="title" placeholder="Tên sách" required />
        <input type="text" name="author" placeholder="Tác giả" required />
        <input type="number" name="price" placeholder="Giá tiền" required />
        <button type="submit">Thêm sách</button>
      </form>
      <table border="1" cellpadding="8" cellspacing="0">
        <tr><th>ID</th><th>Tên sách</th><th>Tác giả</th><th>Giá</th><th>Hành động</th></tr>
    `;
    result.rows.forEach(book => {
      html += `<tr>
        <td>${book.id}</td>
        <td>${book.title}</td>
        <td>${book.author}</td>
        <td>${book.price}</td>
        <td><a href="/delete/${book.id}">Xóa</a></td>
      </tr>`;
    });
    html += `</table>`;
    res.send(html);
  } catch (err) {
    console.error(err);
    res.status(500).send("Lỗi kết nối cơ sở dữ liệu!");
  }
});

app.post('/add', async (req, res) => {
  const { title, author, price } = req.body;
  try {
    await pool.query('INSERT INTO books (title, author, price) VALUES ($1, $2, $3)', [title, author, price]);
    res.redirect('/');
  } catch (err) {
    console.error(err);
    res.status(500).send("Lỗi khi thêm sách!");
  }
});

app.get('/delete/:id', async (req, res) => {
  const { id } = req.params;
  try {
    await pool.query('DELETE FROM books WHERE id = $1', [id]);
    res.redirect('/');
  } catch (err) {
    console.error(err);
    res.status(500).send("Lỗi khi xóa sách!");
  }
});

app.listen(port, () => {
  console.log(`Server đang chạy tại cổng ${port}`);
});
