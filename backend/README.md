---
title: Todo Management API
emoji: 📝
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "latest"
python_version: "3.11"
app_file: main.py
pinned: false
---

# Todo Management API

This is a FastAPI-based Todo Management API deployed on Hugging Face Spaces.

## API Features

- User authentication and registration
- Todo creation, reading, updating, and deletion (CRUD operations)
- Secure JWT-based authentication
- SQLModel-based database operations

## Endpoints

- `GET /` - Health check endpoint
- `/auth/` - Authentication routes (register, login, refresh token)
- `/todos/` - Todo management routes (create, read, update, delete)

## Tech Stack

- FastAPI - Modern, fast web framework for building APIs
- SQLModel - SQL databases with Python objects
- PostgreSQL - Production database
- Alembic - Database migration tool
- Pydantic - Data validation and settings management

## Configuration

The application is configured to run with:
- Python 3.11
- Uvicorn ASGI server
- Docker containerization
- Automatic HTTPS via Hugging Face Spaces

## Note

This backend has been fixed to resolve a previous deployment issue where the `ondelete` parameter was incorrectly used in SQLModel's Field function.