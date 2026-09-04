# 🎬 Movie Watchlist API

A RESTful API built with **FastAPI** for managing a personal movie watchlist.

Users can create accounts, authenticate using JWT tokens, manage their movies, filter and search movies, and like or unlike movies.

---

## 🚀 Features

- 🔐 User registration and authentication
- 🔑 JWT-based authentication
- 🔒 Password hashing using bcrypt
- 🎬 Create multiple movies
- 📋 Retrieve movies with pagination
- 🔎 Search movies by title
- 🎭 Filter movies by genre
- 👀 Filter movies based on watched status
- ⭐ Sort movies by rating, release year, or title
- ✏️ Update movies
- 🗑️ Delete movies
- 👤 Movie ownership authorization
- 👍 Like and unlike movies
- ❤️ View movie like counts
- 🗄️ PostgreSQL database
- 🔄 Database migrations using Alembic
- 📚 Interactive API documentation using Swagger UI

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| FastAPI | Backend Framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Alembic | Database Migrations |
| Pydantic | Data Validation |
| JWT | Authentication |
| Passlib + bcrypt | Password Hashing |
| Uvicorn | ASGI Server |
| UV | Python Package Management |

---

## 📂 Project Structure

```text
Movie_Watchlist_API/
│
├── alembic/
│   └── versions/
│
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── movie.py
│   │   ├── user.py
│   │   └── vote.py
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
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
