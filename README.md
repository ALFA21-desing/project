# project
# 💎 Jewelry E-Commerce Web Application

## 📌 Overview
Secure full-stack Jewelry E-Commerce platform built with:
- Node.js
- Express.js
- MySQL
- JWT Authentication
- Selenium Automation
- JMeter Performance Testing

## 🚀 Features
- User Registration & Login (JWT)
- Product Management
- Shopping Cart
- Checkout System
- Admin Dashboard
- Security Protection (SQL Injection & XSS)
- Automation Testing
- Performance Testing

## 🛠️ Tech Stack
Frontend: HTML, CSS, JavaScript  
Backend: Node.js, Express  
Database: MySQL  
Testing: Selenium, Katalon, JMeter  
CI/CD: GitHub Actions  

## 🗄️ Database Setup
A MySQL database is used by the back end.  A helper script is provided
to create the schema used by the sample application.

1. Make sure MySQL/MariaDB is running locally or adjust connection
   parameters as needed.
2. Execute the SQL file from a shell:

```bash
mysql -u root -p < db_setup.sql
```

If you prefer to inspect the DDL the file contains the full definition of
users, products, cart, orders, order_details and logs tables.

### Python integration

The repository now includes a lightweight Python helper located in
``utils/Database.py`` which wraps ``mysql-connector-python``.  Install the
extra dependency by running ``pip install -r requirements.txt``.
Connection parameters default to environment variables
(``DB_HOST``, ``DB_USER`` etc.) and the database name
``jewelry_store_db`` is used by default.

You can simply import and use it in automation or scripts:

```python
from utils.Database import get_db

with get_db() as db:
    cur = db.execute("SELECT * FROM users LIMIT 1")
    print(cur.fetchone())
```



## ▶️ Run Backend

The repository now includes a minimal Node/Express server that serves the
static front-end and exposes a simple API to the MySQL database.  To start
it:

```bash
cd backend
npm install      # install dependencies (express, mysql2, cors)
npm start        # or node server.js
```

By default the server listens on port 3000.  It will automatically serve the
`website/` directory, so you can open URLs such as
`http://localhost:3000/login.html` and `http://localhost:3000/admin.html`.

### Admin dashboard

A special page `admin.html` is available once you sign in as the demo
user **admin**.  After logging in you will be redirected to this dashboard
which pulls the product list over `/api/products` from the MySQL database.

The schema file even includes a few sample products (silver necklace,
gold ring, diamond earrings) so you'll see data on the admin dashboard
after running it.  You can modify or add more products directly via SQL
or extend the backend with additional endpoints if needed.  The database
schema is defined in `db_setup.sql`.

API base URL:

http://localhost:3000/api


## 🔐 Security
- Passwords hashed using bcrypt
- JWT Authentication
- Protected routes
- Parameterized SQL queries

## 🧪 Testing
- 20+ automation tests
- Performance testing (100 users)
- Unit testing
- Security validation

## 👨‍💻 Author
Sebastián Muñoz  
Student ID: 5809025  
2026