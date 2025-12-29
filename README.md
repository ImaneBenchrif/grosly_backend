#  Grosly Backend API

FastAPI backend for the Grosly grocery delivery application with PostgreSQL database.

##  Features

- User authentication (JWT)
- Product management (CRUD)
- Category management
- Shopping cart system
- Order management
- AI Chatbot integration
- Filtered product endpoints (Today's Choice, Limited Discount, Cheapest)

##  Technologies

- **FastAPI** - Modern Python web framework
- **PostgreSQL** (Supabase) - Database
- **SQLAlchemy** - ORM
- **JWT** - Authentication
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

##  API Endpoints

### Authentication
- `POST /users` - Register new user
- `POST /grosly_token_office` - Login
- `GET /current_user` - Get current user

### Products
- `GET /products` - Get all products
- `GET /products/{id}` - Get product by ID
- `GET /products/todays-choice` - Get today's choice products
- `GET /products/limited-discount` - Get discounted products
- `GET /products/cheapest` - Get cheapest products

### Cart
- `GET /cart/{user_id}` - Get user cart
- `POST /cart/items` - Add item to cart
- `DELETE /cart/{cart_id}` - Clear cart

### Categories
- `GET /categories` - Get all categories

### Chatbot
- `POST /chatbot` - Get recipe suggestions

##  Installation

### Prerequisites

- Python 3.9+
- PostgreSQL database (Supabase)
- pip

### Setup

1. Clone the repository
```bash
git clone https://github.com/ImaneBenchrif/grosly_backend.git
cd grosly_backend
```

2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create `.env` file

Create a `.env` file at the root with the following content:
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

# API Keys
GROQ_API_KEY=your_groq_api_key
```

5. Run the server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

##  Database

The database is hosted on Supabase and includes:
-  Products with images (Fruits, Vegetables, Meat, Seafood, Protein)
-  Categories
-  User accounts
-  Shopping carts
-  Product images from Unsplash

### Test Account
- **Email**: `amaaz@gmail.com`
- **Password**: `12345678`

##  API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

##  Project Structure
```
grosly_backend/
├── .env                  # Environment variables (not in repo)
├── .gitignore           # Git ignore file
├── README.md            # This file
├── requirements.txt     # Python dependencies
├── main.py             # FastAPI application entry point
├── models.py           # SQLAlchemy database models
├── schemas.py          # Pydantic schemas for validation
├── views.py            # API route handlers
├── settings.py         # Application settings
├── utils.py            # Utility functions
└── urls.py             # URL routing configuration
```

##  Related Repositories

### Frontend
 **Flutter Mobile App**: [grosly-app](https://github.com/ImaneBenchrif/grosly-app)

The Flutter application that consumes this API.

##  Author

**Imane Benchrif** **Imane Amaaz**
- GitHub: [@ImaneBenchrif](https://github.com/ImaneBenchrif)
- GitHub: [@ImaneAmaaz](https://github.com/Imaneamaaz)

##  License

This project is for educational purposes.
