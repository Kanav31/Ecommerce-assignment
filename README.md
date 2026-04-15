# Order Management System

A full-stack order management application built with Django REST Framework and React. Supports three user roles — admin, customer, and delivery — each with their own scoped views and permissions.

---

## What it does

- Customers can browse products and place orders
- Admins can add products, view all orders, and assign delivery personnel
- Delivery staff can view their assigned orders and mark them as delivered
- JWT authentication via HttpOnly cookies.
- Role-based access on every API endpoint

---

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Python 3.11, Django 4.2, Django REST Framework |
| Auth | `djangorestframework-simplejwt` (HttpOnly cookies) |
| Database | PostgreSQL 15 |
| Cache | Redis 7 (product list caching — app works without it) |
| API Docs | drf-spectacular (Swagger UI) |
| Frontend | React 19, Vite, React Router, Axios |

---

## Prerequisites

Make sure you have these installed before starting:

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose (for PostgreSQL and Redis)
- `pip` and `venv`

---

## Getting started

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd Ecom-assignment
```

### 2. Start PostgreSQL and Redis

The project ships with a `docker-compose.yml` that runs both services locally.

```bash
docker compose up -d
```

This starts:
- PostgreSQL on `localhost:5432` (db: `ecom_db`, user: `ecom_user`, pass: `ecom_pass`)
- Redis on `localhost:6379`

### 3. Set up the backend

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# .env is pre-filled with values that match docker-compose — no edits needed for local dev

# Run migrations
python manage.py migrate

# Create an admin user
python manage.py createsuperuser
# It will ask for name, email, and password
# Use role: admin — or create one via the /register endpoint with role="admin"

# Start the server
python manage.py runserver
```

Backend runs at `http://localhost:8000`

### 4. Set up the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

---

## Environment variables

The `.env.example` file has all required variables with defaults that work out of the box with `docker-compose`.

To generate a secure `SECRET_KEY`:

```bash
node -e "console.log(require('crypto').randomBytes(50).toString('hex'))"
```

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | use the one generated above | Django secret key — change in production |
| `DEBUG` | `True` | Set to `False` in production |
| `DATABASE_URL` | `postgres://ecom_user:ecom_pass@localhost:5432/ecom_db` | Matches docker-compose defaults |
| `REDIS_URL` | `redis://localhost:6379/0` | Matches docker-compose defaults |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated list |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173` | Must match your frontend URL exactly |

---

## Creating test users

Register users via the frontend `/register` page or directly through the API:

---

## Order flow

```
Customer places order  →  status: pending
Admin assigns delivery person  →  status: assigned
Delivery person marks delivered  →  status: delivered
```

---

## API reference

Swagger UI is available at `http://localhost:8000/api/docs/` once the backend is running.

| Method | Endpoint | Role | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | Public | Register |
| POST | `/api/auth/login/` | Public | Login (sets cookies) |
| POST | `/api/auth/logout/` | Auth | Logout |
| GET | `/api/auth/me/` | Auth | Current user |
| GET | `/api/auth/delivery-users/` | Admin | List delivery staff |
| GET | `/api/products/` | Auth | List products (paginated) |
| POST | `/api/products/` | Admin | Add product |
| GET | `/api/orders/` | Auth | List orders (scoped by role) |
| POST | `/api/orders/` | Customer | Place order |
| POST | `/api/orders/{id}/assign/` | Admin | Assign delivery person |
| PATCH | `/api/orders/{id}/status/` | Delivery | Mark as delivered |

---

## Role permissions summary

| Feature | Admin | Customer | Delivery |
|---|---|---|---|
| Browse products | yes | yes | no |
| Add products | yes | no | no |
| Place orders | no | yes | no |
| View all orders | yes | no | no |
| View own orders | — | yes | — |
| View assigned deliveries | no | no | yes |
| Assign delivery person | yes | no | no |
| Mark order delivered | no | no | yes |

---

## Project structure

```
Ecom-assignment/
├── apps/
│   ├── accounts/       # Auth, users, JWT, role permissions
│   ├── orders/         # Order lifecycle, assignment, status
│   └── products/       # Product catalogue
├── config/             # Django settings, root urls, wsgi
├── core/               # Shared: exceptions, pagination, base classes
├── frontend/           # React app (Vite)
│   └── src/
│       ├── api/        # Axios instance
│       ├── components/ # Navbar, ProtectedRoute
│       ├── context/    # AuthContext
│       └── pages/      # Login, Register, Products, Cart, Orders
├── docker-compose.yml  # PostgreSQL + Redis
├── manage.py
└── requirements.txt
```
