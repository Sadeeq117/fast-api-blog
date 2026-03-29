from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# To make serve up and running.
app = FastAPI()

# Dummy Data to show in UI
posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]


'''
1. we are doing multi stacking of routes. so now with mutiple routes also it return same data.
2. resposne_class is making us to give response as HTML.
3. include in schema bool value will make does this end point need to be part of API Docs are not.
'''


@app.get("/", response_class= HTMLResponse, include_in_schema=False)
@app.get("/post", response_class= HTMLResponse, include_in_schema=False)
def get_ui():
    return f"<h1>My Blog website</h1>"

@app.get('api/post', include_in_schema=True)
def get_posts():
    return posts

