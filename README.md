# Grosly Backend API

> *High-performance REST API powering Morocco's smart grocery delivery platform*

## Overview

Grosly Backend is a robust FastAPI-based REST API that serves as the backbone for the Grosly grocery delivery application. Built with modern Python technologies, it handles user authentication, product management, shopping cart operations, and AI-powered recipe suggestions.

---

## Core Features

### Authentication & Security
- **JWT-based Authentication** - Secure token-based user sessions
- **Password Hashing** - Bcrypt encryption for user credentials
- **Token Refresh** - Automatic session management
- **Role-based Access** - User authorization system

### Product Management
- **Full CRUD Operations** - Complete product lifecycle management
- **Category Organization** - Hierarchical product categorization
- **Image Management** - Multiple images per product with primary image support
- **Stock Tracking** - Real-time inventory management
- **Dynamic Pricing** - Support for promotional pricing and discounts

### Shopping Experience
- **Smart Cart System** - Persistent shopping cart with user session
- **Order Processing** - Complete order creation and management
- **Payment Integration** - Support for multiple payment methods
- **Price Calculation** - Automatic total and discount computation

### AI Integration
- **Recipe Chatbot** - AI-powered Moroccan recipe suggestions using Groq API
- **Ingredient Matching** - Smart recipe recommendations based on available products
- **Natural Language Processing** - Conversational interface for recipe discovery

### Advanced Features
- **Filtered Endpoints** - Curated product collections (Today's Choice, Limited Discount, Cheapest)
- **Search & Filtering** - Advanced product discovery capabilities
- **Review System** - Customer feedback and ratings

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | FastAPI 0.104+ | High-performance async web framework |
| **Database** | PostgreSQL (Supabase) | Relational data storage |
| **ORM** | SQLAlchemy 2.0+ | Database abstraction layer |
| **Authentication** | JWT (python-jose) | Secure token-based auth |
| **Validation** | Pydantic 2.5+ | Request/response data validation |
| **Server** | Uvicorn | ASGI server for production |
| **AI Engine** | Groq API | Recipe generation with LLaMA models |
| **Password Security** | Passlib (bcrypt) | Secure password hashing |

---

## API Endpoints

### Authentication (`/grosly_api_office`)

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `POST` | `/users` | Register new user | Public |
| `POST` | `/grosly_token_office` | User login | Public |
| `POST` | `/grosly_token_refresh_office` | Refresh access token | Required |
| `GET` | `/current_user` | Get authenticated user info | Required |

### Products

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `GET` | `/products` | List all products | Public |
| `GET` | `/products/{id}` | Get product details | Public |
| `GET` | `/products/todays-choice` | Featured products | Public |
| `GET` | `/products/limited-discount` | Discounted products | Public |
| `GET` | `/products/cheapest` | Budget-friendly options | Public |
| `POST` | `/products` | Create new product | Admin |
| `PUT` | `/products/{id}` | Update product | Admin |
| `DELETE` | `/products/{id}` | Delete product | Admin |

### Shopping Cart

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `GET` | `/cart/{user_id}` | Get user's cart | Required |
| `POST` | `/cart/items` | Add item to cart | Required |
| `DELETE` | `/cart/{cart_id}` | Clear cart | Required |

### Categories

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `GET` | `/categories` | List all categories | Public |
| `GET` | `/categories/{id}` | Get category details | Public |
| `POST` | `/categories` | Create category | Admin |

### AI Chatbot

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `POST` | `/chatbot` | Get recipe suggestions | Public |

### Orders & Payments

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `POST` | `/orders` | Create new order | Required |
| `POST` | `/payments` | Process payment | Required |
| `POST` | `/reviews` | Submit product review | Required |

---

## Getting Started

### Prerequisites

- **Python** 3.9 or higher
- **PostgreSQL** database (Supabase recommended)
- **pip** package manager
- **Virtual environment** tool

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ImaneBenchrif/grosly_backend.git
cd grosly_backend
```

2. **Create and activate virtual environment**

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the root directory:
```env
# Database Configuration
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOST=your_postgres_host
DB_PORT=5432
DB_NAME=your_database_name

# JWT Configuration
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# AI Configuration
GROQ_API_KEY=your_groq_api_key
```

5. **Launch the server**

**Development mode:**
```bash
uvicorn main:grosly_app --reload --host 0.0.0.0 --port 8000
```

**Production mode:**
```bash
uvicorn main:grosly_app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Database Schema

### Core Tables

- **users** - User accounts with authentication credentials
- **produits** - Product catalog with pricing and stock
- **categories** - Product categorization system
- **product_images** - Multiple images per product
- **carts** - Shopping cart sessions
- **cart_items** - Individual cart entries
- **orders** - Order records
- **payments** - Payment transactions
- **reviews** - Product reviews and ratings

### Sample Data

The database includes pre-populated data:
- 8+ product categories (Fruits, Vegetables, Meat, Seafood, etc.)
- 50+ products with real images from Unsplash
- Test user account for development

---

## API Documentation

Once the server is running, explore the interactive API documentation:

- **Swagger UI** (Interactive): [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc** (Alternative): [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Project Architecture
```
grosly_backend/
├── .env                    # Environment variables (not tracked)
├── .gitignore             # Git ignore rules
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
│
├── main.py                # FastAPI application entry point
├── urls.py                # API route definitions
├── views.py               # Business logic & route handlers
├── models.py              # SQLAlchemy database models
├── schemas.py             # Pydantic validation schemas
├── settings.py            # Configuration & database setup
└── utils.py               # Helper functions (AI, auth, etc.)
```

---

## Testing

### Test Account Credentials

For development and testing purposes:
```
Email: amaaz@gmail.com
Password: 12345678
```

### Manual Testing

Use the Swagger UI at `/docs` to test all endpoints interactively.

### Example API Call
```bash
# Login
curl -X POST "http://localhost:8000/grosly_api_office/grosly_token_office" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=amaaz@gmail.com&password=12345678"

# Get products
curl -X GET "http://localhost:8000/grosly_api_office/products"
```

---

## Deployment

### Environment Variables

Ensure all production environment variables are properly configured:
- Use strong `SECRET_KEY` (generate with `openssl rand -hex 32`)
- Configure production database credentials
- Set up proper CORS origins for your frontend domain

### Production Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use environment variables for all secrets
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up database backups
- [ ] Enable API rate limiting
- [ ] Configure logging and monitoring
- [ ] Set up error tracking (e.g., Sentry)

---

## Related Repositories

**Frontend Application**: [grosly-app](https://github.com/ImaneBenchrif/grosly-app)  
*Flutter mobile application that consumes this API*

---

## Development Team

**Imane Benchrif**  
GitHub: [@ImaneBenchrif](https://github.com/ImaneBenchrif)

**Imane Amaaz**  
GitHub: [@ImaneAmaaz](https://github.com/Imaneamaaz)

---

## License

This project is developed for educational purposes as part of an academic program.

---

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation at `/docs`
- Review the API specification at `/redoc`

---

<p align="center">
  <em>Made with ❤️ for Morocco's grocery shoppers</em>
</p>
