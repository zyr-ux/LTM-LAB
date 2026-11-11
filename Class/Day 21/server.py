from fastapi import FastAPI
from pydantic import BaseModel,Field

app = FastAPI(title='Simple FastAPI Server')


class Item(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(ge=1)


@app.get("/hello",status_code=200)
def hello():
    return {"message": "Hello World"}


@app.post("/post_data", response_model=Item,status_code=201)
def create_item(input_item_data: Item):
    return input_item_data

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('server:app',host='localhost',port=8000,reload=True)
