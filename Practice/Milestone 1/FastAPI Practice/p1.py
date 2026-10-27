from typing import Optional

from fastapi import FastAPI

app = FastAPI()

users = {
    1: {'id':1,'name': 'Siddhartha', 'company': 'LTM'},
    2: {'id':2,'name': 'Shubh', 'company': 'Coforge'},
    3: {'id':3,'name': 'Rohan', 'company':'Accenture'}
}

@app.get('/')
def hello():
    return{
        'message':'hello'
    }

@app.get('/about')
def about():
    return {
        'message':'Learning FastAPI'
    }

# @app.get('/users/{user_id}')
# def get_all_users(user_id:int):
#     return {
#         'user_id':user_id
#     }

# @app.get('/users/{user_id}/orders/{order_id}')
# def get_order_of_user(user_id:int, order_id:int):
#     return {
#         'user_id':user_id,
#         'order_id':order_id
#     }

# @app.get('/users/query/{user_id}/orders/{order_id}')
# def get_order_of_user_with_queries(user_id:int, order_id:int,limit:int,skip:Optional[int] = 0):
#     return {
#         'user_id':user_id,
#         'order_id':order_id,
#         'limit':limit,
#         'skip':skip
#     }

@app.get('/users')
def get_all_users():
    return users

@app.get('/users/{user_id}')
def get_user_by_id(user_id:int):
    return users[user_id]




