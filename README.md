📘 Python Products API

Lightweight FastAPI application for serving product data to external services (e.g., WordPress plugin).
Products are stored in a local products.json file and exposed through secure HTTP endpoints.

🚀 Features

Read products from products.json

Return all products or single product by ID

Add new products via POST request

Token-based authentication (?token=YOUR_SECRET)

Rate-limited endpoints

Fully JSON-based storage (no database needed)

Easy integration with WordPress or any frontend/backend system

📂 Project Structure

python-api-demo/
│── app.py                # Main FastAPI application
│── products.json         # Product database (JSON)
│── requirements.txt      # Python dependencies
│── README.md             # Documentation
└── venv/                 # Optional: Virtual environment (NOT included in repo)

🛠 Requirements

You need:

Python 3.10+

pip

(recommended) Virtual environment (venv)

⚡ Quick Start
1️⃣ Clone repository
git clone https://github.com/USERNAME/python-api-demo.git
cd python-api-demo

2️⃣ Create & activate virtual environment

💡 Virtual environment is NOT inside the repo. You must create it manually.

Linux / MacOS:

python3 -m venv venv
source venv/bin/activate


Windows (PowerShell):

python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run API server
uvicorn app:app --host 0.0.0.0 --port 8000 --reload


API now runs at:

👉 http://127.0.0.1:8000/

🔐 Authentication: API Token

Every request must include a valid token:

?token=MY_SECRET_TOKEN_123


If missing or invalid, server returns:

{ "detail": "Invalid API token" }


Token is defined inside app.py.

📡 Endpoints
GET /products

Returns all products.

Example:

GET /products?token=MY_SECRET_TOKEN_123


Response:

[
  {
    "id": 1,
    "name": "Gaming Laptop X15",
    "price": 1200.99,
    "image": "https://example.com/laptop.jpg",
    "stock": 30
  }
]

GET /product/{id}

Returns single product.

Example:

GET /product/2?token=MY_SECRET_TOKEN_123


Response:

{
  "id": 2,
  "name": "4K OLED Monitor",
  "price": 899.50,
  "image": "https://example.com/monitor.jpg",
  "stock": 12
}


If product not found:

{ "detail": "Product not found" }

POST /product/add

Adds new product to products.json.

Request:

POST /product/add?token=MY_SECRET_TOKEN_123
Content-Type: application/json


Body:

{
  "name": "Wireless Gaming Mouse",
  "price": 49.99,
  "image": "https://example.com/mouse.jpg",
  "stock": 100
}


Response:

{
  "detail": "Product added",
  "product_id": 7
}


The server automatically assigns id = highest existing + 1.

📁 JSON File Format

Example structure of products.json:

[
  {
    "id": 1,
    "name": "Gaming Laptop X15",
    "price": 1200.99,
    "image": "https://example.com/laptop.jpg",
    "stock": 30
  }
]

🧪 Testing the API
Browser:
http://127.0.0.1:8000/products?token=MY_SECRET_TOKEN_123

cURL:
curl "http://127.0.0.1:8000/product/1?token=MY_SECRET_TOKEN_123"

Postman:

Method: GET or POST

URL: /products or /product/add

Add token as query param

POST requires JSON body

🔧 Troubleshooting
❌ Error: “Address already in use”

Port 8000 is already busy.
Run:

sudo lsof -i :8000
sudo kill -9 PID


Or start API on another port:

uvicorn app:app --port 8001

❌ venv/bin/activate: No such file or directory

You created venv in the wrong folder.

Check:

ls


If venv/ is missing → create it again.

🔐 Security Notes

Do NOT expose this API publicly without HTTPS

Token should be long, random, and secret

Add CORS rules if used on public websites

Rate limit is enabled (5/minute)

🤝 Integration With WordPress Plugin

The WP plugin uses:

wp_remote_get() for fetching products

wp_remote_post() for adding products

Example GET:

$response = wp_remote_get(
    "http://127.0.0.1:8000/products?token=$token"
);


Example POST:

$response = wp_remote_post(
    "http://127.0.0.1:8000/product/add?token=$token",
    [
        'headers' => ['Content-Type' => 'application/json'],
        'body' => json_encode($data)
    ]
);
