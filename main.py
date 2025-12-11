from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from auth import validate_token
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Error handler for rate limit
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests. Please try again later."}
    )

# CORS middleware (optional, useful for WordPress local testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for POST request
class Product(BaseModel):
    name: str
    slug: str
    price_eur: float
    description: str
    image: str
    category: str
    in_stock: bool
    rating: float

# Funkcije za rad sa JSON fajlom - NE koristi globalnu varijablu
def load_products():
    with open("products.json", "r") as f:
        return json.load(f)

def save_products(products):
    with open("products.json", "w") as f:
        json.dump(products, f, indent=4)

# --------------------
# GET all products
# --------------------
@app.get("/products")
@limiter.limit("10/minute")   # max 10 requests per minute
def get_products(request: Request, token: str = None):
    if not validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid API token")
    
    # Uvek učitaj sveže podatke iz fajla
    products = load_products()
    return {"products": products}

# --------------------
# GET single product by ID
# --------------------
@app.get("/product/{product_id}")
@limiter.limit("10/minute")
def get_product(product_id: int, request: Request, token: str = None):
    if not validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid API token")
    
    # Uvek učitaj sveže podatke iz fajla
    products = load_products()
    
    for product in products:
        if product["id"] == product_id:
            return product
    
    raise HTTPException(status_code=404, detail="Product not found")

# --------------------
# POST add new product
# --------------------
@app.post("/product/add")
@limiter.limit("5/minute")
def add_product(request: Request, product: Product, token: str = None):
    if not validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid API token")
    
    # Učitaj trenutne proizvode
    products = load_products()
    
    # Generiši novi ID
    new_id = max([p["id"] for p in products] + [0]) + 1
    
    new_product = {
        "id": new_id,
        "name": product.name,
        "slug": product.slug or product.name.lower().replace(" ", "-"),
        "price_eur": product.price_eur,
        "description": product.description or "",
        "image": product.image,
        "category": product.category or "Uncategorized",
        "in_stock": product.in_stock,
        "rating": product.rating or 0
    }
    
    products.append(new_product)
    save_products(products)
    
    return {"detail": "Product added", "product_id": new_id}