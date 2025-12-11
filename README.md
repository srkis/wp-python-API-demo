📘 Python Products API – README

1. Overview

This is a lightweight Python-based API used for serving electronic products to a WordPress plugin.
The API:

- Reads product data from products.json

- Exposes product data through secure HTTP endpoints

- Requires a secret API token

- Allows fetching:

  - all products

  - a single product by ID

  - (Optional) Allows adding new products via POST and updating products.json

The WordPress plugin communicates with this API using GET and POST requests.

2. Project Structure
```
python-api-demo/
│── app.py
│── products.json
│── requirements.txt
│── README.md
│── venv/ (optional)
```

3. Requirements

Your system must have:

- Python 3.10+

- pip (Python package manager)

4. Install Dependencies

Inside the python-api-demo folder run:

```bash
pip install -r requirements.txt
```

This installs:

- FastAPI

- uvicorn

- Python libraries for JSON file manipulation

5. Creating & Activating a Virtual Environment
Create venv:

```bash
python3 -m venv venv
```

Activate venv (Linux/MacOS):

```bash
source venv/bin/activate
```

Activate venv (Windows):

```powershell
venv\Scripts\activate
```

If `venv/bin/activate` gives "No such file or directory", you probably created venv in a different folder.
Make sure you create it inside the `python-api-demo` folder.

6. Running the API Server

Start the application with:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Now the API is available at:

http://127.0.0.1:8000/

7. Authentication – API Token

All endpoints require a token:

`?token=MY_SECRET_TOKEN_123`

If the token is missing or incorrect, the API responds with:

```json
{ "detail": "Invalid API token" }
```

8. Endpoints
GET /products

Returns all products from products.json.

Example Request:
`GET /products?token=MY_SECRET_TOKEN_123`

Example Response:
```json
[
  {
    "id": 1,
    "name": "Gaming Laptop X15",
    "price": 1200.99,
    "image": "https://placehold.co/600x400?text=Laptop",
    "stock": 30
  }
]
```

GET /product/{id}

Returns a single product by its ID.

Example Request:
`GET /product/2?token=MY_SECRET_TOKEN_123`

Example Response:
```json
{
  "id": 2,
  "name": "4K OLED Monitor",
  "price": 899.50,
  "image": "https://placehold.co/600x400?text=Monitor",
  "stock": 12
}
```

If product doesn’t exist:

```json
{ "detail": "Product not found" }
```

POST /product/add

Adds a new product into products.json.

Example Request:
`POST /product/add?token=MY_SECRET_TOKEN_123`
Content-Type: application/json

JSON Body:
```json
{
  "name": "Wireless Gaming Mouse",
  "price": 49.99,
  "image": "https://placehold.co/600x400?text=Mouse",
  "stock": 100
}
```

Example Response:
```json
{
  "detail": "Product added",
  "product_id": 7
}
```

The API automatically assigns a new ID
(max existing ID + 1).

9. JSON File Format (products.json)
```json
[
  {
    "id": 1,
    "name": "Gaming Laptop X15",
    "price": 1200.99,
    "image": "https://placehold.co/600x400?text=Laptop",
    "stock": 30
  }
]
```

10. Using the API from WordPress Plugin

Your WP plugin uses:

- `wp_remote_get()` for GET endpoints

- `wp_remote_post()` for POST

Example (GET all products):
```php
$response = wp_remote_get(
    "http://127.0.0.1:8000/products?token=" . $token
);
```

Example (POST new product):
```php
$response = wp_remote_post(
    "http://127.0.0.1:8000/product/add?token=" . $token,
    [
        'headers' => ['Content-Type' => 'application/json'],
        'body'    => json_encode($data)
    ]
);
```

11. Testing the API Manually
Browser:
`http://127.0.0.1:8000/products?token=MY_SECRET_TOKEN_123`

cURL:
```bash
curl "http://127.0.0.1:8000/product/1?token=MY_SECRET_TOKEN_123"
```

Postman:

Create GET or POST request

Add `?token=YOUR_TOKEN`

For POST: set JSON body

12. Notes

✔ Always keep your token secret
✔ Do not expose API publicly without extra security
✔ products.json must have valid JSON format

13. Troubleshooting
❌ venv/bin/activate – No such file or directory

Likely caused by running the command in the wrong folder.

Run:

```bash
ls
```

Make sure you SEE the `venv/` folder.

If not, create it again in the correct folder.
