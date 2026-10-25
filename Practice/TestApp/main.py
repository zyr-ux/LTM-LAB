from fastapi import FastAPI

app = FastAPI()

products = {
    1: {"name": "Keyboard", "price": 1500},
    2: {"name": "Mouse", "price": 800}
}

@app.get("/")
def home():
    return {"message":"hello"}

@app.get("/products")
def get_products():
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    return products.get(product_id, {"error": "Product not found"})

@app.post("/products")
def create_product(product: dict):
    product_id = max(products.keys(), default=0) + 1
    products[product_id] = product

    return {"id": product_id, **product}

@app.put("/products/{product_id}")
def replace_product(product_id: int, product: dict):
    if product_id not in products:
        return {"error": "Product not found"}

    products[product_id] = product
    return products[product_id]

@app.patch("/products/{product_id}")
def update_product(product_id: int, product: dict):
    if product_id not in products:
        return {"error": "Product not found"}

    products[product_id].update(product)
    return products[product_id]

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    if product_id not in products:
        return {"error": "Product not found"}

    deleted = products.pop(product_id)
    return {"message": "Product deleted", "product": deleted}