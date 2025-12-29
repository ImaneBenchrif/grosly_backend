from __future__ import annotations
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
import uuid
from datetime import datetime

# ======================================================
# AUTH
# ======================================================
class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


# ======================================================
# USERS
# ======================================================
class UserBase(BaseModel):
    userlastname: str
    userfirstname: str
    email: EmailStr
    phone_number: Optional[str] = None
    pays: str
    indicatif_pays: Optional[str] = None
    adresse: Optional[str] = None
    termes_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    userlastname: Optional[str] = None
    userfirstname: Optional[str] = None
    phone_number: Optional[str] = None
    pays: Optional[str] = None
    indicatif_pays: Optional[str] = None
    adresse: Optional[str] = None


class UserRead(UserBase):
    id: uuid.UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ======================================================
# CATEGORIES
# ======================================================
class CategoryBase(BaseModel):
    name: str
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryRead(CategoryBase):
    id: uuid.UUID
    slug: str
    created_at: datetime

    class Config:
        from_attributes = True


# ======================================================
# PRODUCTS
# ======================================================
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    promo_price: Optional[float] = None
    stock: int = 0
    is_active: bool = True
    category_id: uuid.UUID


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: uuid.UUID
    slug: str
    created_at: datetime
    images: List[ProductImageRead] = []

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    promo_price: Optional[float] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None
    category_id: Optional[uuid.UUID] = None

# ======================================================
# PRODUCT IMAGES
# ======================================================
class ProductImageBase(BaseModel):
    image_url: str
    is_main: bool = False


class ProductImageCreate(ProductImageBase):
    product_id: uuid.UUID


class ProductImageRead(ProductImageBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


# ======================================================
# CART & CART ITEMS
# ======================================================
class CartItemBase(BaseModel):
    product_id: uuid.UUID
    quantity: int = Field(gt=0)


class CartItemCreate(CartItemBase):
    pass


class CartItemRead(CartItemBase):
    id: uuid.UUID
    price: float

    class Config:
        from_attributes = True


class CartRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    items: List[CartItemRead] = []

    class Config:
        from_attributes = True


# ======================================================
# ADDRESSES
# ======================================================
class AddressBase(BaseModel):
    full_name: str
    phone: str
    city: str
    country: str
    address_line: str


class AddressCreate(AddressBase):
    pass


class AddressRead(AddressBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


# ======================================================
# ORDERS & ORDER ITEMS
# ======================================================
class OrderItemBase(BaseModel):
    product_id: uuid.UUID
    quantity: int
    price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    address_id: uuid.UUID


class OrderRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemRead] = []
    payment: Optional[PaymentRead] = None

    class Config:
        from_attributes = True


# ======================================================
# PAYMENTS
# ======================================================
class PaymentCreate(BaseModel):
    order_id: uuid.UUID
    method: str = "Livraison"


class PaymentRead(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID
    amount: float
    method: str
    status: str
    reference: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ======================================================
# REVIEWS
# ======================================================
class ReviewBase(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    product_id: uuid.UUID


class ReviewRead(ReviewBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Permet les forward references
OrderRead.update_forward_refs()

# ======================================================
# CHATBOT
# ======================================================
class ChatbotRequest(BaseModel):
    user_message: str