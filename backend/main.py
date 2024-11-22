from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt

# Security configurations
SECRET_KEY = "your-secret-key-here"  # In production, use a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="NextShop API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class User(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    full_name: str
    is_active: bool = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ProductBase(BaseModel):
    name: str
    price: float
    category: str
    description: str
    features: List[str]
    specifications: dict
    image: Optional[str] = None

class Product(ProductBase):
    id: int

class CartItem(BaseModel):
    product_id: int
    quantity: int

class OrderItem(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    image: Optional[str] = None

class OrderDetails(BaseModel):
    firstName: str
    lastName: str
    email: str
    address: str
    city: str
    country: str
    zipCode: str

class Order(BaseModel):
    id: int
    user_id: int
    items: List[OrderItem]
    total: float
    details: OrderDetails
    status: str
    created_at: datetime

# Mock database
users = []
products = [
    {
        "id": 1,
        "name": "Wireless Headphones",
        "price": 99.99,
        "category": "Electronics",
        "description": "High-quality wireless headphones with noise cancellation",
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
        "features": [
            "Active Noise Cancellation",
            "40-hour battery life",
            "Bluetooth 5.0",
            "Built-in microphone",
        ],
        "specifications": {
            "brand": "NextAudio",
            "model": "WH-1000",
            "weight": "250g",
            "connectivity": "Wireless",
        }
    },
    {
        "id": 2,
        "name": "Smart Watch",
        "price": 199.99,
        "category": "Electronics",
        "description": "Feature-rich smartwatch with health tracking",
        "image": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500",
        "features": [
            "Heart rate monitoring",
            "Sleep tracking",
            "Water resistant",
            "5-day battery life",
        ],
        "specifications": {
            "brand": "NextWear",
            "model": "SW-200",
            "weight": "45g",
            "connectivity": "Bluetooth",
        }
    },
    {
        "id": 3,
        "name": "Laptop Backpack",
        "price": 49.99,
        "category": "Accessories",
        "description": "Durable and spacious laptop backpack",
        "image": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=500",
        "features": [
            "Fits 15-inch laptops",
            "Water-resistant material",
            "Multiple compartments",
            "Padded straps",
        ],
        "specifications": {
            "brand": "NextPack",
            "model": "BP-100",
            "capacity": "25L",
            "material": "Polyester",
        }
    },
    {
        "id": 4,
        "name": "Mechanical Keyboard",
        "price": 129.99,
        "category": "Electronics",
        "description": "Premium mechanical keyboard with RGB lighting",
        "image": "https://images.unsplash.com/photo-1601445638532-3c6f6c3aa1d6?w=500",
        "features": [
            "Cherry MX switches",
            "RGB backlighting",
            "Aluminum frame",
            "Programmable keys",
        ],
        "specifications": {
            "brand": "NextType",
            "model": "MK-300",
            "layout": "Full size",
            "switch_type": "Mechanical",
        }
    },
    {
        "id": 5,
        "name": "Wireless Mouse",
        "price": 39.99,
        "category": "Electronics",
        "description": "Ergonomic wireless mouse with precision tracking",
        "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500",
        "features": [
            "12000 DPI sensor",
            "6 programmable buttons",
            "Ergonomic design",
            "Long battery life",
        ],
        "specifications": {
            "brand": "NextPoint",
            "model": "WM-100",
            "weight": "95g",
            "connectivity": "2.4GHz wireless",
        }
    },
    {
        "id": 6,
        "name": "4K Monitor",
        "price": 349.99,
        "category": "Electronics",
        "description": "27-inch 4K IPS monitor with HDR support",
        "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500",
        "features": [
            "4K UHD resolution",
            "HDR10 support",
            "1ms response time",
            "FreeSync technology",
        ],
        "specifications": {
            "brand": "NextView",
            "model": "MN-400",
            "size": "27 inches",
            "resolution": "3840x2160",
        }
    },
    {
        "id": 7,
        "name": "Laptop Stand",
        "price": 29.99,
        "category": "Accessories",
        "description": "Adjustable aluminum laptop stand",
        "image": "https://images.unsplash.com/photo-1619725002198-6a689b72f41d?w=500",
        "features": [
            "Adjustable height",
            "Aluminum construction",
            "Portable design",
            "Heat dissipation",
        ],
        "specifications": {
            "brand": "NextDesk",
            "model": "LS-100",
            "material": "Aluminum",
            "weight_capacity": "10kg",
        }
    },
    {
        "id": 8,
        "name": "USB-C Hub",
        "price": 59.99,
        "category": "Electronics",
        "description": "7-in-1 USB-C hub with power delivery",
        "image": "https://images.unsplash.com/photo-1636389657461-7ecf7c88c60c?w=500",
        "features": [
            "4K HDMI output",
            "100W Power Delivery",
            "USB 3.0 ports",
            "SD card reader",
        ],
        "specifications": {
            "brand": "NextConnect",
            "model": "UC-700",
            "ports": "7 ports",
            "power_delivery": "100W",
        }
    }
]

orders: List[Order] = []
next_order_id = 1
next_user_id = 1

# Security functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_email(email: str):
    return next((user for user in users if user.email == email), None)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# Auth endpoints
@app.post("/api/auth/register", response_model=Token)
async def register_user(user_data: UserCreate):
    if get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    global next_user_id
    user = User(
        id=next_user_id,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name
    )
    users.append(user)
    next_user_id += 1

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name
    }

# Existing endpoints
@app.get("/")
async def read_root():
    return {"message": "Welcome to NextShop API"}

@app.get("/api/products", response_model=List[Product])
async def get_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    filtered_products = products

    if category:
        filtered_products = [p for p in filtered_products if p["category"].lower() == category.lower()]
    
    if min_price is not None:
        filtered_products = [p for p in filtered_products if p["price"] >= min_price]
    
    if max_price is not None:
        filtered_products = [p for p in filtered_products if p["price"] <= max_price]

    return filtered_products

@app.get("/api/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/api/categories")
async def get_categories():
    categories = set(p["category"] for p in products)
    return list(categories)

@app.post("/api/orders")
async def create_order(
    items: List[CartItem],
    details: OrderDetails,
    current_user: User = Depends(get_current_user)
):
    global next_order_id
    
    if not items:
        raise HTTPException(status_code=400, detail="Order must contain items")
    
    total = sum(item.price * item.quantity for item in items)
    
    order = Order(
        id=next_order_id,
        user_id=current_user.id,
        items=[OrderItem(id=item.product_id, name="Product", price=0.0, quantity=item.quantity) for item in items],
        total=total,
        details=details,
        status="pending",
        created_at=datetime.now()
    )
    
    orders.append(order)
    next_order_id += 1
    
    return order

@app.get("/api/orders/me")
async def get_my_orders(current_user: User = Depends(get_current_user)):
    user_orders = [order for order in orders if order.user_id == current_user.id]
    return user_orders

@app.get("/api/orders/{order_id}")
async def get_order(order_id: int, current_user: User = Depends(get_current_user)):
    order = next((o for o in orders if o.id == order_id and o.user_id == current_user.id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/api/orders/new")
async def create_new_order(
    items: List[OrderItem],
    details: OrderDetails,
    current_user: User = Depends(get_current_user)
):
    global next_order_id
    
    if not items:
        raise HTTPException(status_code=400, detail="Order must contain items")
    
    total = sum(item.price * item.quantity for item in items)
    
    order = Order(
        id=next_order_id,
        user_id=current_user.id,
        items=items,
        total=total,
        details=details,
        status="pending",
        created_at=datetime.now()
    )
    
    orders.append(order)
    next_order_id += 1
    
    return order

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
