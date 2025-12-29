from sqlalchemy.orm import Session
from settings import verify_password, hash_password
import models
from groq import Groq # type: ignore
import os

import uuid

# ======================================================
# AUTH / USERS
# ======================================================
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.UserProfile).filter(models.UserProfile.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def reset_password(db: Session, user_id: str, new_password: str):
    user = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    if not user:
        return None
    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user

# ======================================================
# CRUD USERS
# ======================================================
def create_user(db: Session, user):
    if not user.termes_active:
        raise ValueError("User must accept terms and conditions")
    hashed_password = hash_password(user.password)
    db_user = models.UserProfile(
        userlastname=user.userlastname,
        userfirstname=user.userfirstname,
        email=user.email,
        phone_number=user.phone_number,
        pays=user.pays,
        indicatif_pays=user.indicatif_pays,
        adresse=user.adresse,
        termes_active=user.termes_active,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: str):
    return db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()

def update_user(db: Session, user_id: str, updates):
    user = get_user(db, user_id)
    if not user:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        if key == "password":
            setattr(user, "hashed_password", hash_password(value))
        else:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: str):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user

# ======================================================
# CRUD CATEGORIES
# ======================================================
def create_category(db: Session, category):
    slug = category.name.lower().replace(" ", "-")
    db_category = models.Category(
        name=category.name,
        slug=slug,
        is_active=category.is_active
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: str):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def update_category(db: Session, category_id: str, updates):
    category = get_category(db, category_id)
    if not category:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category_id: str):
    category = get_category(db, category_id)
    if category:
        db.delete(category)
        db.commit()
    return category

# ======================================================
# CRUD PRODUITS
# ======================================================
def create_product(db: Session, product):
    slug = product.name.lower().replace(" ", "-")
    db_product = models.Product(
        name=product.name,
        slug=slug,
        description=product.description,
        price=product.price,
        promo_price=product.promo_price,
        stock=product.stock,
        is_active=product.is_active,
        category_id=product.category_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: str):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def update_product(db: Session, product_id: str, updates):
    product = get_product(db, product_id)
    if not product:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: str):
    product = get_product(db, product_id)
    if product:
        db.delete(product)
        db.commit()
    return product

# ======================================================
# CRUD IMAGES PRODUITS
# ======================================================
def add_product_image(db: Session, product_id: str, image_url: str, is_main: bool = False):
    db_image = models.ProductImage(
        product_id=product_id,
        image_url=image_url,
        is_main=is_main
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_product_images(db: Session, product_id: str):
    return db.query(models.ProductImage).filter(models.ProductImage.product_id == product_id).all()

# ======================================================
# CRUD PANIER
# ======================================================
def add_to_cart(db: Session, user_id: str, product_id: str, quantity: int, price: float):
    """Ajoute un produit au panier, crée le panier s'il n'existe pas"""
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).first()
    if not cart:
        cart = models.Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    item = models.CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity, price=price)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_cart(db: Session, user_id: str):
    """Récupère le panier d'un utilisateur, le crée s'il n'existe pas"""
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).first()
    
    # ✅ Si le panier n'existe pas, le créer
    if not cart:
        print(f"ℹ️ Création d'un nouveau panier pour l'utilisateur {user_id}")
        cart = models.Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    return cart

def clear_cart(db: Session, cart_id: str):
    """Vide le panier en supprimant tous ses items"""
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if cart:
        for item in cart.items:
            db.delete(item)
        db.commit()
    return cart

# ======================================================
# CRUD COMMANDES
# ======================================================
def create_order(db: Session, user_id: str, address_id: str, items: list):
    """Crée une commande avec les items du panier"""
    total_amount = sum([item.price * item.quantity for item in items])
    db_order = models.Order(user_id=user_id, address_id=address_id, total_amount=total_amount)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    for item in items:
        order_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(order_item)
    db.commit()
    return db_order

# ======================================================
# CRUD PAIEMENTS
# ======================================================
def create_payment(db: Session, order_id: str, amount: float, method: str = "Livraison"):
    """Crée un paiement pour une commande"""
    db_payment = models.Payment(
        order_id=order_id,
        amount=amount,
        method=method,
        status="pending"
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

# ======================================================
# CRUD REVIEWS
# ======================================================
def create_review(db: Session, user_id: str, product_id: str, rating: int, comment: str = None):
    """Crée un avis pour un produit"""
    db_review = models.Review(
        user_id=user_id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# ======================================================
# CHATBOT - GROQ API
# ======================================================
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.1-8b-instant"

def generate_recipe(ingredients: list[str], user_message: str) -> str:
    """
    Génère une suggestion de recette marocaine basée sur les ingrédients disponibles
    et le message de l'utilisateur
    """
    ingredients_text = ", ".join(ingredients)

    prompt = f"""
You are a strict Moroccan cooking assistant.

USER INTENT:
{user_message}

RULES:
- Respect the user request strictly.
- Suggest ONE realistic Moroccan dish.
- Use ONLY available ingredients.
- Do NOT invent ingredients.
- Do NOT suggest dishes requiring dough, flour, semolina, bread.

AVAILABLE INGREDIENTS:
{ingredients_text}

RESPONSE FORMAT:

Bismillah,
Suggested dish: <dish name>
Used ingredients: <only used ingredients>
Missing ingredients: <only complementary ingredients>
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a strict Moroccan chef."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f" Erreur lors de la génération de recette: {e}")
        return "Désolé, je ne peux pas générer de recette pour le moment. Veuillez réessayer."