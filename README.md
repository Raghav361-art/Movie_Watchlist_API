# 🎬 Movie Watchlist API

A full-stack movie watchlist application built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.

The project provides a REST API for user authentication, movie management, filtering, pagination, and movie likes. It also includes a simple web interface for interacting with the watchlist.

---

## ✨ Features

### 🔐 Authentication

- User registration
- JWT-based authentication
- Secure password hashing with bcrypt
- Protected endpoints
- User ownership and authorization
- Token expiration

### 🎬 Movie Management

- Create multiple movies in a single request
- Retrieve movies
- Retrieve a movie by ID
- Update movies
- Delete movies
- Movies belong to their creating user

### 🔎 Search & Filtering

- Search movies by title
- Filter by genre
- Filter by watched status
- Pagination with `limit` and `offset`
- Sort by:
  - Rating
  - Release year
  - Title

### 👍 Likes

- Like movies
- Unlike movies
- Prevent duplicate likes
- Display the number of likes for each movie

### 🗄️ Database

- PostgreSQL
- SQLAlchemy ORM
- Async database operations
- Alembic database migrations
- Foreign-key relationships
- Cascading deletes

### 🎨 Web Interface

- Server-rendered HTML templates
- Static CSS and JavaScript
- Movie dashboard
- Authentication interface
- Light/Dark theme toggle
- Responsive design

### 📚 API Documentation

FastAPI automatically provides interactive API documentation through Swagger UI.

Once the application is running:

- `/docs` — Swagger UI
- `/redoc` — ReDoc

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Programming language |
| FastAPI | Web framework |
| SQLAlchemy | ORM |
| PostgreSQL | Database |
| asyncpg | Async PostgreSQL driver |
| Alembic | Database migrations |
| Pydantic | Data validation |
| Pydantic Settings | Environment configuration |
| JWT | Authentication |
| Passlib + bcrypt | Password hashing |
| Uvicorn | ASGI server |
| Gunicorn | Production process manager |
| Docker | Containerization |
| Jinja2 | HTML templating |
| HTML / CSS / JavaScript | Frontend |

---

## 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │     Browser      │
                    │ HTML/CSS/JS      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     FastAPI      │
                    │     Routers      │
                    └────────┬─────────┘
                             │
                 ┌───────────┴───────────┐
                 │                       │
                 ▼                       ▼
        ┌────────────────┐      ┌────────────────┐
        │ Authentication │      │   SQLAlchemy   │
        │      JWT       │      │  AsyncSession  │
        └────────────────┘      └───────┬────────┘
                                        │
                                        ▼
                                 ┌──────────────┐
                                 │   asyncpg    │
                                 └──────┬───────┘
                                        │
                                        ▼
                                 ┌──────────────┐
                                 │  PostgreSQL  │
                                 └──────────────┘


## 📂 Project Structure

```text
Movie_Watchlist_API/
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── movie.py
│   │   ├── user.py
│   │   └── vote.py
│   │
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   │
│   ├── templates/
│   │   ├── layouts.html
│   │   ├── home.html
│   │   └── dashboard.html
│   │
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── oauth2.py
│   ├── schemas.py
│   └── utils.py
│
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md