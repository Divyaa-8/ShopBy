# 🛍️ Shopzy – Django E-Commerce Store

A fun, beginner-friendly e-commerce store built with **Django + SQLite**.

## 📁 Project Structure

```
shopzy_django/
├── manage.py               ← Django's main command tool
├── requirements.txt        ← Python packages needed
├── setup.bat               ← One-click Windows setup script
├── db.sqlite3              ← Database (auto-created)
│
├── shopzy/                 ← Project settings
│   ├── settings.py
│   └── urls.py
│
└── store/                  ← Our main app
    ├── models.py           ← Database models (Product, Order, etc.)
    ├── views.py            ← Page logic
    ├── urls.py             ← URL routes
    ├── admin.py            ← Admin panel setup
    ├── fixtures/
    │   └── initial_data.json   ← Sample products
    ├── templates/store/    ← HTML templates
    │   ├── base.html
    │   ├── home.html
    │   ├── shop.html
    │   ├── product_detail.html
    │   ├── cart.html
    │   ├── checkout.html
    │   ├── order_success.html
    │   ├── orders.html
    │   ├── login.html
    │   └── register.html
    └── static/store/
        ├── css/style.css
        └── js/app.js
```

---

## 🚀 Setup (Step by Step)

### Prerequisites
- Python 3.10 or newer → https://www.python.org/downloads/
- Make sure to check **"Add Python to PATH"** during install!

---

### Option A – Easy (Windows, double-click)
Just double-click **`setup.bat`** and it does everything automatically!
Then run:
```
python manage.py runserver
```

---

### Option B – Manual (Terminal / VS Code)

**Step 1** – Open terminal in the `shopzy_django` folder

**Step 2** – Install Django:
```bash
pip install -r requirements.txt
```

**Step 3** – Set up database:
```bash
python manage.py makemigrations
python manage.py migrate
```

**Step 4** – Load sample products:
```bash
python manage.py loaddata store/fixtures/initial_data.json
```

**Step 5** – Create admin account:
```bash
python manage.py createsuperuser
```
(Enter any username/email/password you want)

**Step 6** – Start the server:
```bash
python manage.py runserver
```

**Step 7** – Open browser:
- 🛍️ Store → http://127.0.0.1:8000
- 🔧 Admin → http://127.0.0.1:8000/admin

---

## ✨ Features

| Feature | Details |
|---|---|
| 🏠 Home | Hero section + featured products |
| 🏪 Shop | All products, search, category filter |
| 📄 Product detail | Full info + quantity selector |
| 🛒 Shopping cart | Session-based, update quantities |
| 💳 Checkout | Review order and confirm |
| 📦 Orders | View your order history |
| 🔑 Login / Register | Django auth with hashed passwords |
| 🔧 Admin panel | Manage products, orders, users |

---

## 🗄️ Database Models

| Model | Fields |
|---|---|
| `Category` | name |
| `Product` | name, description, price, emoji, category, stock |
| `Order` | user, status, total, created_at |
| `OrderItem` | order, product, quantity, price |

---

## 🔧 Admin Panel

Visit http://127.0.0.1:8000/admin
- Add/edit/delete products
- Change order status (pending → shipped → delivered)
- View all users and orders
