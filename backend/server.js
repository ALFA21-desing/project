const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// simple pool with environment‑driven configuration
const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || '3306',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '',
  database: process.env.DB_NAME || 'jewelry_store_db',
};
let pool;

async function initDb() {
  pool = mysql.createPool({
    ...dbConfig,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0,
  });
}

app.use(cors());
app.use(express.json());
// serve static files from website folder
app.use(express.static(path.join(__dirname, '..', 'website')));

// API endpoints
app.get('/api/products', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM products');
    res.json(rows);
  } catch (err) {
    console.error('DB query failed', err);
    res.status(500).json({ error: 'Database error' });
  }
});

app.listen(PORT, async () => {
  try {
    await initDb();
    console.log(`Server listening on port ${PORT}`);
  } catch (err) {
    console.error('Failed to initialize database pool', err);
    process.exit(1);
  }
});
