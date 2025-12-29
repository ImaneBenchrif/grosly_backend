from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from settings import create_access_token, create_refresh_token, decode_access_token
import utils
import models

# ======================================================
# AUTH
# ======================================================
def login_view(form_data: OAuth2PasswordRequestForm, db: Session):
    user = utils.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

def refresh_token_view(refresh_token: str, db: Session):
    try:
        payload = decode_access_token(refresh_token)
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

# ======================================================
# USERS
# ======================================================
def create_user_view(user, db: Session):
    return utils.create_user(db, user)

def get_user_view(user_id: str, db: Session):
    user = utils.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user_view(user_id: str, updates, db: Session):
    user = utils.update_user(db, user_id, updates)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def delete_user_view(user_id: str, db: Session):
    user = utils.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}

# ======================================================
# CATEGORIES
# ======================================================
def create_category_view(category, db: Session):
    return utils.create_category(db, category)

def get_category_view(category_id: str, db: Session):
    category = utils.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def update_category_view(category_id: str, updates, db: Session):
    category = utils.update_category(db, category_id, updates)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def delete_category_view(category_id: str, db: Session):
    category = utils.delete_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"detail": "Category deleted"}

def list_categories_view(db: Session):
    """Liste toutes les catégories"""
    categories = db.query(models.Category).all()
    return categories

# ======================================================
# PRODUCTS
# ======================================================
def create_product_view(product, db: Session):
    return utils.create_product(db, product)

def get_product_view(product_id: str, db: Session):
    product = utils.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def update_product_view(product_id: str, updates, db: Session):
    product = utils.update_product(db, product_id, updates)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def delete_product_view(product_id: str, db: Session):
    product = utils.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}

def list_products_view(db: Session):
    """Liste tous les produits avec leurs images (OPTIMISÉ)"""
    from sqlalchemy.orm import joinedload
    
    # Récupérer tous les produits avec leurs images en UNE SEULE requête
    products = db.query(models.Product).options(
        joinedload(models.Product.images)
    ).all()
    
    result = []
    for product in products:
        # Trouver l'image principale ou la première disponible
        main_image = None
        if product.images:
            # Chercher l'image principale
            main_image = next((img for img in product.images if img.is_main), None)
            # Si pas d'image principale, prendre la première
            if not main_image and len(product.images) > 0:
                main_image = product.images[0]
        
        # Construire le dictionnaire du produit
        product_dict = {
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "promo_price": product.promo_price,
            "stock": product.stock,
            "category_id": str(product.category_id) if product.category_id else None,
            "weight": product.weight if hasattr(product, 'weight') else "1kg",
            "image": main_image.image_url if main_image else "https://via.placeholder.com/150"
        }
        result.append(product_dict)
    
    return result

# ======================================================
# PRODUCT IMAGES
# ======================================================
def add_product_image_view(product_id: str, image_url: str, is_main: bool, db: Session):
    return utils.add_product_image(db, product_id, image_url, is_main)

def get_product_images_view(product_id: str, db: Session):
    return utils.get_product_images(db, product_id)

# ======================================================
# CART
# ======================================================
def add_to_cart_view(user_id: str, product_id: str, quantity: int, price: float, db: Session):
    return utils.add_to_cart(db, user_id, product_id, quantity, price)

def get_cart_view(user_id: str, db: Session):
    cart = utils.get_cart(db, user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

def clear_cart_view(cart_id: str, db: Session):
    cart = utils.clear_cart(db, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return {"detail": "Cart cleared"}

# ======================================================
# ORDERS
# ======================================================
def create_order_view(user_id: str, address_id: str, items: list, db: Session):
    return utils.create_order(db, user_id, address_id, items)

# ======================================================
# PAYMENTS
# ======================================================
def create_payment_view(order_id: str, amount: float, method: str, db: Session):
    return utils.create_payment(db, order_id, amount, method)

# ======================================================
# REVIEWS
# ======================================================
def create_review_view(user_id: str, product_id: str, rating: int, comment: str, db: Session):
    return utils.create_review(db, user_id, product_id, rating, comment)

# ======================================================
# FILTERED PRODUCTS (Today's choice, Limited discount, Cheapest)
# ======================================================
def get_todays_choice_view(db: Session):
    """Récupère 10 produits de différentes catégories pour Today's choice"""
    # Récupérer toutes les catégories
    categories = db.query(models.Category).all()
    
    if not categories:
        return []
    
    result = []
    products_per_category = max(1, 10 // len(categories))
    
    for category in categories:
        # Prendre quelques produits de chaque catégorie
        products = db.query(models.Product).filter(
            models.Product.category_id == category.id,
            models.Product.stock > 0
        ).limit(products_per_category).all()
        
        for product in products:
            # Récupérer l'image du produit
            main_image = db.query(models.ProductImage).filter(
                models.ProductImage.product_id == product.id,
                models.ProductImage.is_main == True
            ).first()
            
            if not main_image:
                main_image = db.query(models.ProductImage).filter(
                    models.ProductImage.product_id == product.id
                ).first()
            
            result.append({
                "id": str(product.id),
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "promo_price": product.promo_price,
                "stock": product.stock,
                "category_id": str(product.category_id),
                "weight": product.weight if hasattr(product, 'weight') else "1kg",
                "image": main_image.image_url if main_image else "https://via.placeholder.com/150"
            })
            
            if len(result) >= 10:
                break
        
        if len(result) >= 10:
            break
    
    return result


def get_limited_discount_view(db: Session):
    """Récupère les 10 produits avec promo"""
    products = db.query(models.Product).filter(
        models.Product.promo_price.isnot(None),
        models.Product.stock > 0
    ).limit(10).all()
    
    result = []
    for product in products:
        # Récupérer l'image du produit
        main_image = db.query(models.ProductImage).filter(
            models.ProductImage.product_id == product.id,
            models.ProductImage.is_main == True
        ).first()
        
        if not main_image:
            main_image = db.query(models.ProductImage).filter(
                models.ProductImage.product_id == product.id
            ).first()
        
        result.append({
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "promo_price": product.promo_price,
            "stock": product.stock,
            "category_id": str(product.category_id) if product.category_id else None,
            "weight": product.weight if hasattr(product, 'weight') else "1kg",
            "image": main_image.image_url if main_image else "https://via.placeholder.com/150"
        })
    
    return result


def get_cheapest_products_view(db: Session):
    """Récupère les 10 produits les moins chers"""
    from sqlalchemy import case

    
    
    # Utiliser le prix promo s'il existe, sinon le prix normal
    products = db.query(models.Product).filter(
        models.Product.stock > 0
    ).order_by(
        case(
            (models.Product.promo_price.isnot(None), models.Product.promo_price),
            else_=models.Product.price
        )
    ).limit(10).all()
    
    result = []
    for product in products:
        # Récupérer l'image du produit
        main_image = db.query(models.ProductImage).filter(
            models.ProductImage.product_id == product.id,
            models.ProductImage.is_main == True
        ).first()
        
        if not main_image:
            main_image = db.query(models.ProductImage).filter(
                models.ProductImage.product_id == product.id
            ).first()
        
        result.append({
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "promo_price": product.promo_price,
            "stock": product.stock,
            "category_id": str(product.category_id) if product.category_id else None,
            "weight": product.weight if hasattr(product, 'weight') else "1kg",
            "image": main_image.image_url if main_image else "https://via.placeholder.com/150"
        })
    
    return result