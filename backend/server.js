const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const path = require('path');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key'; // Cambia esto en producción

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

  // Seed demo users
  try {
    const demoUsers = [
      { username: 'admin', password: 'Admin@123', firstName: 'Admin', lastName: 'User', email: 'admin@example.com', age: 30, role: 'admin' },
      { username: 'user', password: 'User@123', firstName: 'Demo', lastName: 'User', email: 'user@example.com', age: 25, role: 'user' }
    ];

    for (const user of demoUsers) {
      const hashedPassword = await bcrypt.hash(user.password, 10);
      await pool.query(
        'INSERT IGNORE INTO users (username, password, firstName, lastName, email, age, role) VALUES (?, ?, ?, ?, ?, ?, ?)',
        [user.username, hashedPassword, user.firstName, user.lastName, user.email, user.age, user.role]
      );
    }
    console.log('Demo users seeded');

    // Seed demo products
    const demoProducts = [
      { name: 'Silver Necklace', category: 'Neckwear', price: 49.99, stock: 120, description: 'Elegant sterling silver necklace' },
      { name: 'Gold Ring', category: 'Rings', price: 199.99, stock: 40, description: 'Solid 14k gold wedding band' },
      { name: 'Diamond Earrings', category: 'Earrings', price: 499.99, stock: 20, description: 'Sparkling diamond studs' },
      { name: 'Pearl Bracelet', category: 'Bracelets', price: 79.99, stock: 75, description: 'Classic freshwater pearl bracelet' },
      { name: 'Ruby Pendant', category: 'Neckwear', price: 299.99, stock: 35, description: 'Heart-shaped ruby pendant' },
      { name: 'Sapphire Studs', category: 'Earrings', price: 349.99, stock: 50, description: 'Blue sapphire stud earrings' },
      { name: 'Leather Watch', category: 'Watches', price: 129.99, stock: 60, description: 'Men\'s leather strap watch' }
    ];

    for (const product of demoProducts) {
      await pool.query(
        'INSERT IGNORE INTO products (name, category, price, stock, description) VALUES (?, ?, ?, ?, ?)',
        [product.name, product.category, product.price, product.stock, product.description]
      );
    }
    console.log('Demo products seeded');
  } catch (err) {
    console.error('Failed to seed demo users', err);
  }
}

app.use(cors());
app.use(express.json());
// serve static files from website folder
app.use(express.static(path.join(__dirname, '..', 'website')));

// Middleware para verificar JWT
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Access token required' });

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ error: 'Invalid token' });
    req.user = user;
    next();
  });
}

// API endpoints

// Register
app.post('/api/register', async (req, res) => {
  const { firstName, lastName, email, age, username, password } = req.body;
  try {
    const hashedPassword = await bcrypt.hash(password, 10);
    const [result] = await pool.query(
      'INSERT INTO users (firstName, lastName, email, age, username, password) VALUES (?, ?, ?, ?, ?, ?)',
      [firstName, lastName, email, age, username, hashedPassword]
    );
    res.status(201).json({ message: 'User registered', userId: result.insertId });
  } catch (err) {
    console.error('Registration failed', err);
    res.status(500).json({ error: 'Registration failed' });
  }
});

// Login
app.post('/api/login', async (req, res) => {
  const { username, password } = req.body;
  try {
    const [rows] = await pool.query('SELECT * FROM users WHERE username = ?', [username]);
    if (rows.length === 0) return res.status(401).json({ error: 'Invalid credentials' });

    const user = rows[0];
    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) return res.status(401).json({ error: 'Invalid credentials' });

    const token = jwt.sign({ userId: user.user_id, username: user.username, role: user.role }, JWT_SECRET);
    res.json({ token, user: { userId: user.user_id, username: user.username, role: user.role } });
  } catch (err) {
    console.error('Login failed', err);
    res.status(500).json({ error: 'Login failed' });
  }
});

// Products
app.get('/api/products', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM products');
    res.json(rows);
  } catch (err) {
    console.error('DB query failed', err);
    res.status(500).json({ error: 'Database error' });
  }
});

app.post('/api/products', authenticateToken, async (req, res) => {
  if (req.user.role !== 'admin') return res.status(403).json({ error: 'Admin required' });
  const { name, category, price, stock, description } = req.body;
  try {
    const [result] = await pool.query(
      'INSERT INTO products (name, category, price, stock, description) VALUES (?, ?, ?, ?, ?)',
      [name, category, price, stock, description]
    );
    res.status(201).json({ message: 'Product added', productId: result.insertId });
  } catch (err) {
    console.error('Add product failed', err);
    res.status(500).json({ error: 'Database error' });
  }
});

// Cart
app.get('/api/cart', authenticateToken, async (req, res) => {
  try {
    const [rows] = await pool.query(
      'SELECT c.*, p.name, p.price FROM cart c JOIN products p ON c.product_id = p.product_id WHERE c.user_id = ?',
      [req.user.userId]
    );
    res.json(rows);
  } catch (err) {
    console.error('Get cart failed', err);
    res.status(500).json({ error: 'Database error' });
  }
});

app.post('/api/cart', authenticateToken, async (req, res) => {
  const { productId, quantity } = req.body;
  try {
    await pool.query(
      'INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE quantity = quantity + ?',
      [req.user.userId, productId, quantity, quantity]
    );
    res.status(201).json({ message: 'Item added to cart' });
  } catch (err) {
    console.error('Add to cart failed', err);
    res.status(500).json({ error: 'Database error' });
  }
});

app.put('/api/cart/:id', authenticateToken, async (req, res) => {
  const { quantity } = req.body;
  try {
    await pool.query('UPDATE cart SET quantity = ? WHERE cart_id = ? AND user_id = ?', [quantity, req.params.id, req.user.userId]);
    res.json({ message: 'Cart updated' });
  } catch (err) {
    console.error('Update cart failed', err);
    res.status(500).json({ error: 'Database error' });
  }
});

app.delete('/api/cart/:id', authenticateToken, async (req, res) => {
  try {
    await pool.query('DELETE FROM cart WHERE cart_id = ? AND user_id = ?', [req.params.id, req.user.userId]);
    res.json({ message: 'Item removed from cart' });
  } catch (err) {
    console.error('Remove from cart failed', err);
    res.status(500).json({ error: 'Database error' });
  }
});

// Checkout
app.post('/api/checkout', authenticateToken, async (req, res) => {
  try {
    const [cartItems] = await pool.query('SELECT * FROM cart WHERE user_id = ?', [req.user.userId]);
    if (cartItems.length === 0) return res.status(400).json({ error: 'Cart is empty' });

    const total = cartItems.reduce((sum, item) => sum + (item.quantity * item.price), 0); // Asumiendo que price está en cart, pero mejor calcular

    // Crear orden
    const [orderResult] = await pool.query('INSERT INTO orders (user_id, total) VALUES (?, ?)', [req.user.userId, total]);
    const orderId = orderResult.insertId;

    // Insertar detalles
    for (const item of cartItems) {
      await pool.query('INSERT INTO order_details (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)', [orderId, item.product_id, item.quantity, item.price]);
    }

    // Limpiar cart
    await pool.query('DELETE FROM cart WHERE user_id = ?', [req.user.userId]);

    res.json({ message: 'Checkout successful', orderId });
  } catch (err) {
    console.error('Checkout failed', err);
    res.status(500).json({ error: 'Checkout failed' });
  }
});

// Orders (for user profile)
app.get('/api/orders', authenticateToken, async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM orders WHERE user_id = ?', [req.user.userId]);
    res.json(rows);
  } catch (err) {
    console.error('Get orders failed', err);
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
