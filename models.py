import uuid
from sqlalchemy import (
    Column, String, Float, Boolean, DateTime,
    ForeignKey, Integer, Text, func, event
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from slugify import slugify

Base = declarative_base()


# ------------------------------
# Utils
# ------------------------------
def generate_slug(name: str) -> str:
    return slugify(name)


#------------------------------
# Users
#------------------------------
class UserProfile(Base):
    __tablename__ = 'profiles_utilisateurs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hashed_password = Column(String(255), nullable=False)
    userlastname = Column(String(100), nullable=False)
    userfirstname = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=True)
    pays = Column(String(100), nullable=False)
    indicatif_pays = Column(String(10), nullable=True)
    adresse = Column(String(255), nullable=True)
    termes_active = Column(Boolean, default=True)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())

# ------------------------------
# Categories
# ------------------------------
class Category(Base):
    __tablename__ = "categories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    slug = Column(String(160), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    produits = relationship("Product", back_populates="category")

# ------------------------------
# Produits
# ------------------------------
class Product(Base):
    __tablename__ = "produits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text)

    price = Column(Float, nullable=False)
    promo_price = Column(Float)

    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), index=True)
    weight = Column(String(50), default="1kg")  # ✅ Ajout du champ weight
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="produits")
    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan"
    )
    reviews = relationship("Review", back_populates="product")


# Slug automatique
@event.listens_for(Product, "before_insert")
def set_product_slug(mapper, connection, target):
    if not target.slug:
        target.slug = generate_slug(target.name)


# ------------------------------
# Images Produits
# ------------------------------
class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("produits.id", ondelete="CASCADE"))

    image_url = Column(String(500), nullable=False)
    is_main = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="images")


# ------------------------------
# Panier
# ------------------------------
class Cart(Base):
    __tablename__ = "paniers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles_utilisateurs.id"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserProfile")
    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan"
    )


# ------------------------------
# Items Panier
# ------------------------------
class CartItem(Base):
    __tablename__ = "panier_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("paniers.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("produits.id"))

    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")


# ------------------------------
# Adresses
# ------------------------------
class Address(Base):
    __tablename__ = "adresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles_utilisateurs.id"), index=True)

    full_name = Column(String(255))
    phone = Column(String(20))
    city = Column(String(100))
    country = Column(String(100))
    address_line = Column(String(255))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserProfile")
    orders = relationship("Order", back_populates="address")


# ------------------------------
# Commandes
# ------------------------------
class Order(Base):
    __tablename__ = "commandes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles_utilisateurs.id"), index=True)
    address_id = Column(UUID(as_uuid=True), ForeignKey("adresses.id"))

    total_amount = Column(Float, nullable=False)
    status = Column(String(30), default="pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserProfile")
    address = relationship("Address", back_populates="orders")
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
    payment = relationship(
        "Payment",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan"
    )


# ------------------------------
# Items Commande
# ------------------------------
class OrderItem(Base):
    __tablename__ = "commande_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("commandes.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("produits.id"))

    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")


# ------------------------------
# Paiements
# ------------------------------
class Payment(Base):
    __tablename__ = "paiements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("commandes.id"), unique=True)

    amount = Column(Float, nullable=False)
    method = Column(String(50), default="Livraison")
    status = Column(String(30), default="pending")
    reference = Column(String(100), unique=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="payment")


# ------------------------------
# Avis Produits
# ------------------------------
class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles_utilisateurs.id"), index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("produits.id"), index=True)

    rating = Column(Integer)  # 1 à 5
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserProfile")
    product = relationship("Product", back_populates="reviews")
# ------------------------------