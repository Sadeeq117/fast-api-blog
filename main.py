from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse,JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException



# To make serve up and running.
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name= "static")
templates = Jinja2Templates(directory="templates")

# Dummy Data to show in UI
posts: list[dict] = [
    {
        "id": 1,
        "author": "Sadeeq Shaik",
        "title": "Getting Started with FastAPI",
        "content": "FastAPI allows you to build APIs quickly with automatic validation and async support.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Sadeeq Shaik",
        "title": "Understanding Async in Python",
        "content": "Async programming helps handle multiple requests efficiently without blocking execution.",
        "date_posted": "April 21, 2025",
    },
    {
        "id": 3,
        "author": "Sadeeq Shaik",
        "title": "Why Pydantic Matters",
        "content": "Pydantic ensures data validation and serialization, making APIs more reliable.",
        "date_posted": "April 22, 2025",
    },
    {
        "id": 4,
        "author": "Sadeeq Shaik",
        "title": "Building REST APIs with FastAPI",
        "content": "FastAPI simplifies REST API development with automatic docs and type hints.",
        "date_posted": "April 23, 2025",
    },
    {
        "id": 5,
        "author": "Sadeeq Shaik",
        "title": "Dependency Injection in FastAPI",
        "content": "Dependency injection helps manage shared logic like database connections efficiently.",
        "date_posted": "April 24, 2025",
    },
    {
        "id": 6,
        "author": "Sadeeq Shaik",
        "title": "Working with SQLAlchemy",
        "content": "SQLAlchemy helps interact with databases using Python objects instead of raw SQL.",
        "date_posted": "April 25, 2025",
    },
    {
        "id": 7,
        "author": "Sadeeq Shaik",
        "title": "Handling Authentication with JWT",
        "content": "JWT tokens are commonly used for securing APIs and managing user sessions.",
        "date_posted": "April 26, 2025",
    },
    {
        "id": 8,
        "author": "Sadeeq Shaik",
        "title": "API Versioning Best Practices",
        "content": "Versioning ensures backward compatibility and smooth API evolution.",
        "date_posted": "April 27, 2025",
    },
    {
        "id": 9,
        "author": "Sadeeq Shaik",
        "title": "Pagination and Filtering",
        "content": "Pagination improves performance by limiting data, and filtering refines results.",
        "date_posted": "April 28, 2025",
    },
    {
        "id": 10,
        "author": "Sadeeq Shaik",
        "title": "Deploying FastAPI Applications",
        "content": "Deploy FastAPI apps using Uvicorn, Docker, and cloud platforms for scalability.",
        "date_posted": "April 29, 2025",
    },
]



@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/icons/favicon.ico")


@app.get("/",  include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request : Request):
    return templates.TemplateResponse(request, "home.html", {"title": "Home" ,"posts" : posts})

@app.get('/posts/{post_id}', include_in_schema=False)
def posts_page(request: Request, post_id : int):
    for post in posts:
        if post['id'] == post_id:
            title = post['title'][:50]
            return templates.TemplateResponse(request, "post.html", {"title": title ,"post" : post})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not found.")



@app.get('/api/posts', include_in_schema=True)
def get_posts():
    return posts


@app.get('/api/posts/{post_id}', include_in_schema=True)
def get_posts(post_id : int):
    for post in posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not found.")

@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )       

