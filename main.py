import uvicorn
from fastapi import FastAPI

from resources import auth, some_routes

# Create metadata for tags
# The order of each tag metadata dictionary also defines the order shown in the docs UI.
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

# app = FastAPI(
#         title:str="Sample App", 
#         description:str="My fastapi trial app", 
#         version:str="0.1.0", 
#         openapi_tags=tags_metadata, 
#         openapi_url="/api/v1/openapi.json"
#     )
app = FastAPI()

def configure():
    app.include_router(auth.router)
    app.include_router(some_routes.router)

configure()

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)

