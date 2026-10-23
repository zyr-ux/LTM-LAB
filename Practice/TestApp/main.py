from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message":"hello"}

@app.get("/about")
def about():
    return {
        "framework": "FastAPI",
        "purpose": "Building HTTP APIs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {
        "product_id": product_id,
        "message": "Product retrieved"
    }