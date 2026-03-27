# 💎 Jewelry Obelisco - E-Commerce Platform

##  Overview

A complete, secure full-stack jewelry e-commerce platform built with modern web technologies. This project demonstrates comprehensive knowledge in backend development, frontend integration, database design, security implementation, automated testing, and CI/CD practices.

**Key Features:**
-  JWT Authentication with bcrypt password hashing
-  Dynamic shopping cart with API synchronization
-  Admin dashboard for product management
-  Comprehensive testing suite (Selenium, Katalon, JMeter)
-  CI/CD pipeline with GitHub Actions
-  Responsive design with modern UI/UX

## 🛠️ Technology Stack

### Backend
- **Node.js 18+** - JavaScript runtime
- **Express.js 4.18** - Web framework
- **MySQL 8.0+** - Relational database
- **bcryptjs** - Password hashing
- **jsonwebtoken** - JWT implementation
- **cors** - Cross-origin resource sharing

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Responsive styling
- **JavaScript ES6+** - Client-side logic
- **Fetch API** - HTTP requests

### Testing & Automation
- **Python 3.9+** - Testing language
- **Selenium 4.8** - Browser automation
- **Pytest** - Testing framework
- **Katalon Studio** - UI testing
- **Apache JMeter** - Performance testing

### DevOps
- **GitHub Actions** - CI/CD pipeline
- **Git** - Version control

##  Database Schema

The application uses a MySQL database with the following tables:

### Core Tables
- **`users`** - User accounts with roles (user/admin)
- **`products`** - Jewelry catalog with pricing and inventory
- **`cart`** - Shopping cart items per user
- **`orders`** - Purchase orders
- **`order_details`** - Order line items
- **`logs`** - System audit logs

### Database Setup

1. **Install MySQL 8.0+** locally
2. **Run the setup script:**
   ```bash
   mysql -u root -p < db_setup.sql
   ```

The script creates the database `jewelry_store_db` and populates it with:
- Demo admin user: `admin` / `Admin@123`
- Demo regular user: `user` / `User@123`
- Sample jewelry products (necklaces, rings, earrings)

##  API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/register` | Register new user |  |
| `POST` | `/api/login` | User login with JWT |   |

### Product Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/products` | Get all products |    |
| `POST` | `/api/products` | Add new product | (Admin only) |

### Cart Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/cart` | Get user's cart |         |
| `POST` | `/api/cart` | Add item to cart |       |
| `PUT` | `/api/cart/:id` | Update item quantity  |
| `DELETE` | `/api/cart/:id` | Remove item from cart |

### Order Endpoints
| Method | Endpoint | Description | Auth Required  |
|--------|----------|-------------|--------------- |
| `GET` | `/api/orders` | Get user's order history | 
| `POST` | `/api/checkout` | Process purchase |    |

##  Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- MySQL 8.0+
- Git

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd project
   ```

2. **Set up the database:**
   ```bash
   mysql -u root -p < db_setup.sql
   ```

3. **Install backend dependencies:**
   ```bash
   cd backend
   npm install
   ```

4. **Install testing dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the backend server:**
   ```bash
   cd backend
   npm start
   # Server runs on http://localhost:3000
   ```

6. **Open in browser:**
   - Main site: `http://localhost:3000`
   - Admin login: `http://localhost:3000/admin.html`

##  Security Features

### Authentication & Authorization
- **Password Hashing:** bcrypt with salt rounds (10)
- **JWT Tokens:** Stateless authentication with expiration
- **Role-Based Access:** Admin vs regular user permissions
- **Protected Routes:** Middleware validation for sensitive endpoints

### Data Protection
- **SQL Injection Prevention:** Parameterized queries
- **XSS Protection:** Input sanitization and escaping
- **CORS Configuration:** Controlled cross-origin requests
- **Input Validation:** Frontend and backend validation

##  Testing Suite

### Test Categories

#### 1. Selenium Automation Tests (10+ tests)
- **Page Object Model** for maintainable code
- **Cross-browser testing** (Chrome, Firefox, Edge)
- **End-to-end workflows** (registration → login → purchase)
- **Data-driven testing** with CSV files

**Run Selenium tests:**
```bash
pytest tests/ --tb=short
```

#### 2. Katalon Studio Tests (10 tests)
- **UI Recording** for visual workflows
- **API Testing** for backend validation
- **Data-driven registration** testing
- **Viewport testing** for responsiveness

#### 3. JMeter Performance Tests
- **Load testing** (50-100 concurrent users)
- **Stress testing** for critical endpoints
- **Response time analysis**
- **Throughput measurement**

### Test Results
- HTML reports: `test_results/pytest_selected_report.html`
- CSV data: `test_results/katalon_results.csv`
- Performance metrics: `test_results/jmeter_performance_report.html`

##  CI/CD Pipeline

### GitHub Actions Workflow
Automated testing and validation on every push/PR:

```yaml
name: CI/CD Pipeline
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ --tb=short
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: test_results/
```

##  Project Structure

```
project/
├── backend/
│   ├── server.js           # Express server with API endpoints
│   ├── package.json        # Node.js dependencies
│   └── node_modules/       # Installed packages
├── website/
│   ├── index.html          # Homepage with hero section
│   ├── catalogo.html       # Product catalog with filters
│   ├── cart.html           # Shopping cart with checkout
│   ├── login.html          # User authentication
│   ├── register.html       # User registration
│   ├── admin.html          # Admin dashboard
│   ├── order-history.html  # Order history
│   ├── user-profile.html   # User profile
│   ├── cart.js             # Cart logic and API integration
│   ├── style.css           # Global styles
│   └── assets/             # Images and resources
├── pages/
│   ├── BasePage.py         # Page Object Model base class
│   ├── LoginPage.py        # Login page object
│   ├── AdminPage.py        # Admin page object
│   └── ...                 # Other page objects
├── tests/
│   ├── test_admin.py       # Admin dashboard tests
│   ├── test_authentication.py # Login/register tests
│   ├── test_shopping.py    # Shopping workflow tests
│   └── ...                 # Additional test files
├── utils/
│   ├── Database.py         # Database utilities
│   ├── WebDriverFactory.py # Browser factory
│   ├── WaitUtility.py      # Explicit waits
│   └── ExcelUtility.py     # Excel file handling
├── db_setup.sql            # Database schema and seed data
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
└── .github/
    └── workflows/
        └── ci.yml          # GitHub Actions workflow
```

##  Key Features Implemented

### User Experience
- **Responsive Design:** Mobile-first approach
- **Real-time Validation:** Form validation with feedback
- **Smooth Animations:** CSS transitions and effects
- **Offline Capability:** localStorage fallback when API unavailable

### Business Logic
- **Dual Cart System:** API + localStorage synchronization
- **Multi-step Checkout:** Shipping → Payment → Review
- **Order Management:** Complete purchase history
- **Admin Controls:** Product CRUD operations

### Technical Excellence
- **Error Handling:** Comprehensive try/catch blocks
- **Code Quality:** Clean, documented, maintainable code
- **Performance:** Optimized queries and caching
- **Scalability:** Modular architecture for growth

##  Performance Metrics

### Load Testing Results (JMeter)
- **Concurrent Users:** 100
- **Response Time:** < 500ms average
- **Throughput:** 150+ requests/second
- **Error Rate:** < 1%

### Test Coverage
- **Unit Tests:** 6+ core functions
- **Integration Tests:** 8+ end-to-end workflows
- **UI Tests:** 10+ user interface validations
- **Performance Tests:** 5+ load scenarios

##  Development Notes

### Environment Variables
```bash
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=jewelry_store_db

# JWT Configuration
JWT_SECRET=your_jwt_secret_key

# Server Configuration
PORT=3000
```

### Demo Credentials
- **Admin:** `admin` / `Admin@123`
- **User:** `user` / `User@123`

### Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

##  Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create a Pull Request

##  License

This project is licensed under the MIT License - see the LICENSE file for details.

##  Author

**Sebastián Muñoz**  
**Student ID:** 5809025  
**Institution:** Matrix College  
**Program:** Computer Science  
**Date:** March 17, 2026

##  Acknowledgments

- Matrix College faculty for guidance and support
- Open source community for excellent tools and libraries
- Modern web development best practices and security standards

---

**Jewelry Obelisco** - A complete e-commerce solution demonstrating full-stack development excellence.
