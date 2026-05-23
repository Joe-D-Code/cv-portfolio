# Grocery Store Web System

> A full-stack grocery ordering web application built with PHP, MySQL, and React, featuring user authentication, product browsing, order management, and a separate admin view.

---

## Overview

Using a PHP backend with a MySQL database, this system allows users to register, browse grocery products, and place orders through a session-authenticated interface. An admin role, verified against the database on every request, provides a separate view of all orders across all customers. The frontend combines server-rendered PHP templates with React components for interactive forms, served via a local Apache environment.

---

## Features

**User-facing**
- Registration with real-time client-side validation covering name, phone, email, and password format
- CAPTCHA verification on login to prevent automated access
- Session-based authentication that persists across pages
- Product browsing with category filtering (Meat and Vegetables)
- Authenticated order placement linked to the logged-in user's account
- Personal order history view showing product, price, and date

**Admin**
- Role-based access controlled by a database flag verified server-side on every request
- Full order table showing all customers, products, prices, and dates
- Live order search by order ID

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | PHP 8, MySQLi / PDO |
| Database | MySQL |
| Frontend | HTML, CSS, JavaScript, React 17 (via CDN) |
| Templating | PHP server-rendered templates |
| Auth | PHP sessions with CAPTCHA |
| Environment | Apache (XAMPP or equivalent) |

---

## Project Structure

```
grocery_store/
├── api/
│   ├── add_order.php          # Authenticated order creation endpoint
│   ├── get_products.php       # Product listing with category filter
│   ├── login.php              # Login handler with CAPTCHA verification
│   ├── logout.php             # Session destruction
│   ├── order.php              # Order retrieval with pagination and filtering
│   └── register.php           # User registration with duplicate email check
├── assets/
│   ├── captcha_images/        # Static CAPTCHA image set
│   ├── css/style.css          # Global stylesheet
│   ├── images/                # Product images
│   └── js/
│       ├── admin-order_search.js  # Admin order search
│       ├── burgerMenu.js          # Responsive navigation toggle
│       ├── index.js               # Product table and category filter
│       ├── login.js               # React login form component
│       └── register.js            # React registration form component
├── includes/
│   ├── admin_auth.php         # Admin role verification guard
│   ├── captcha.php            # CAPTCHA image generator
│   ├── db_connect.php         # Database connection configuration
│   ├── error_handler.php      # Global error and exception handlers
│   ├── footer.php             # Shared page footer
│   ├── header.php             # Shared navigation header
│   └── logged_check.php       # Redirect guard for already-logged-in users
├── logs/                      # Server-side error logs (gitignored)
└── templates/
    ├── admin_order.php        # Admin order management view
    ├── index.php              # Product listing page
    ├── login.php              # Login page
    ├── order.php              # User order history page
    └── register.php           # Registration page
```

---

## How to Run

### Prerequisites

- [XAMPP](https://www.apachefriends.org/) or any Apache and MySQL stack
- PHP 8.0+

### Setup

1. Clone or copy the `grocery_store` folder into your Apache `htdocs` directory
2. Start Apache and MySQL via XAMPP
3. Create a MySQL database and import the schema (see Database Setup below)
4. Open `includes/db_connect.php` and update the credentials:

```php
$servername = "localhost";
$username   = "your_username";
$password   = "your_password";
$dbname     = "your_database_name";
```

5. Visit `http://localhost/grocery_store/templates/index.php` in your browser

### Database Setup

The database requires two tables with the following structure:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin TINYINT(1) DEFAULT 0
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category ENUM('Meat', 'Vegetables') NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    image VARCHAR(255)
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_email VARCHAR(150) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

To create an admin account, register normally then update the `is_admin` flag directly in the database:

```sql
UPDATE users SET is_admin = 1 WHERE email = 'your@email.com';
```

---

## Security Approach

Given that this is a locally run academic project rather than a production deployment, the following measures were applied as good practice:

- Passwords stored using `password_hash()` and verified with `password_verify()`
- All database queries use PDO prepared statements with parameterised inputs, preventing SQL injection
- Category filter uses a server-side whitelist rather than passing user input directly to the query
- CAPTCHA cleared from session immediately after verification to prevent replay attacks
- Output passed through `htmlspecialchars()` throughout templates, preventing XSS
- Admin access verified against the database on every page load, not relying on session data alone
- Sensitive error details logged server-side only, with generic messages shown to the user

---

## Skills Demonstrated

- Full-stack web development with PHP and MySQL
- RESTful API design with JSON responses
- Session-based authentication and role management
- React component integration within a server-rendered PHP application
- Client-side and server-side input validation
- Prepared statements and parameterised queries
- Responsive UI with a mobile burger menu