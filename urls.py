from uuid import UUID
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from utils import generate_recipe
import views
import schemas
from models import Product, UserProfile
from settings import get_db, get_current_user

router = APIRouter(
    prefix="/grosly_api_office",
    tags=["API"]
)

# ======================================================
# AUTH
# ======================================================
@router.post("/grosly_token_office", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return views.login_view(form_data, db)

@router.post("/grosly_token_refresh_office", response_model=schemas.Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    return views.refresh_token_view(refresh_token, db)

@router.get("/current_user", response_model=schemas.UserRead)
def current_user(current_user: UserProfile = Depends(get_current_user)):
    return current_user

# ======================================================
# USERS
# ======================================================
@router.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return views.create_user_view(user, db)

@router.get("/users/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    return views.get_user_view(user_id, db)

@router.put("/users/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: UUID, updates: schemas.UserUpdate, db: Session = Depends(get_db)):
    return views.update_user_view(user_id, updates, db)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    views.delete_user_view(user_id, db)

# ======================================================
# CATEGORIES
# ======================================================
@router.post("/categories", response_model=schemas.CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return views.create_category_view(category, db)

@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    return views.list_categories_view(db)

@router.get("/categories/{category_id}", response_model=schemas.CategoryRead)
def get_category(category_id: UUID, db: Session = Depends(get_db)):
    return views.get_category_view(category_id, db)

@router.put("/categories/{category_id}", response_model=schemas.CategoryRead)
def update_category(category_id: UUID, updates: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    return views.update_category_view(category_id, updates, db)

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: UUID, db: Session = Depends(get_db)):
    views.delete_category_view(category_id, db)

# ======================================================
# PRODUCTS
# ======================================================
@router.post("/products", response_model=schemas.ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return views.create_product_view(product, db)

# ✅ ROUTES SPÉCIFIQUES AVANT LES ROUTES AVEC {product_id}
@router.get("/products/todays-choice")
def get_todays_choice(db: Session = Depends(get_db)):
    return views.get_todays_choice_view(db)

@router.get("/products/limited-discount")
def get_limited_discount(db: Session = Depends(get_db)):
    return views.get_limited_discount_view(db)

@router.get("/products/cheapest")
def get_cheapest_products(db: Session = Depends(get_db)):
    return views.get_cheapest_products_view(db)

@router.get("/products")
def list_products(db: Session = Depends(get_db)):
    return views.list_products_view(db)

# ⚠️ CETTE ROUTE DOIT ÊTRE APRÈS LES ROUTES SPÉCIFIQUES
@router.get("/products/{product_id}", response_model=schemas.ProductRead)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    return views.get_product_view(product_id, db)

@router.put("/products/{product_id}", response_model=schemas.ProductRead)
def update_product(product_id: UUID, updates: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return views.update_product_view(product_id, updates, db)

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    views.delete_product_view(product_id, db)

# ======================================================
# PRODUCT IMAGES
# ======================================================
@router.post("/products/{product_id}/images", response_model=schemas.ProductImageRead, status_code=status.HTTP_201_CREATED)
def add_product_image(product_id: UUID, image: schemas.ProductImageCreate, db: Session = Depends(get_db)):
    return views.add_product_image_view(product_id, image.image_url, image.is_main, db)

@router.get("/products/{product_id}/images", response_model=list[schemas.ProductImageRead])
def get_product_images(product_id: UUID, db: Session = Depends(get_db)):
    return views.get_product_images_view(product_id, db)

# ======================================================
# CART
# ======================================================
@router.post("/cart/items", response_model=schemas.CartItemRead)
def add_to_cart(item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    return views.add_to_cart_view(item.user_id, item.product_id, item.quantity, item.price, db)

@router.get("/cart/{user_id}", response_model=schemas.CartRead)
def get_cart(user_id: UUID, db: Session = Depends(get_db)):
    return views.get_cart_view(user_id, db)

@router.delete("/cart/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(cart_id: UUID, db: Session = Depends(get_db)):
    views.clear_cart_view(cart_id, db)

# ======================================================
# ORDERS
# ======================================================
@router.post("/orders", response_model=schemas.OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return views.create_order_view(order.user_id, order.address_id, order.items, db)

# ======================================================
# PAYMENTS
# ======================================================
@router.post("/payments", response_model=schemas.PaymentRead, status_code=status.HTTP_201_CREATED)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    return views.create_payment_view(payment.order_id, payment.amount, payment.method, db)

# ======================================================
# REVIEWS
# ======================================================
@router.post("/reviews", response_model=schemas.ReviewRead, status_code=status.HTTP_201_CREATED)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return views.create_review_view(review.user_id, review.product_id, review.rating, review.comment, db)

# ======================================================
# CHATBOT
# ======================================================
@router.post("/chatbot")
def recipe_chatbot(request: schemas.ChatbotRequest, db: Session = Depends(get_db)):
    """
    Chatbot pour suggérer des recettes marocaines
    """
    print(f"📥 Requête chatbot reçue: {request.user_message}")
    
    # Récupérer tous les produits disponibles
    produits = db.query(Product).filter(Product.stock > 0).all()
    ingredients = [p.name for p in produits if p.name]

    if not ingredients:
        return {
            "ingredients": [],
            "chatbot_response": "Désolé, aucun ingrédient n'est disponible pour le moment."
        }
    
    print(f"📦 {len(ingredients)} ingrédients disponibles")
    
    # Générer la réponse du chatbot
    response = generate_recipe(ingredients, request.user_message)
    
    print(f"✅ Réponse générée: {response[:100]}...")
    
    return {
        "ingredients": ingredients,
        "chatbot_response": response
    }