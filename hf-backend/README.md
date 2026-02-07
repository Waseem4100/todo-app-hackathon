---
title: Todo Management API
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# Todo Management API

A FastAPI-based todo management backend deployed on Hugging Face Spaces.

## API Endpoints

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `GET /todos` - Get all user's todos
- `POST /todos` - Create a new todo
- `GET /todos/{id}` - Get a specific todo
- `PUT /todos/{id}` - Update a specific todo
- `DELETE /todos/{id}` - Delete a specific todo
- `PATCH /todos/{id}/toggle-complete` - Toggle todo completion status

## Environment Variables

Set these in your Space settings:
- `DATABASE_URL`: PostgreSQL database URL
- `SECRET_KEY`: Secret key for JWT tokens
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Note

This backend is designed to work with the Todo frontend deployed separately.