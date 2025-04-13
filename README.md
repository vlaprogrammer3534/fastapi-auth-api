# 🔐 Auth API with FastAPI

This is a secure authentication system built using **FastAPI**. It uses **JWT (JSON Web Tokens)** for managing user sessions and includes essential authentication features like login, secure data access, refresh token handling, and logout.

---

## 🚀 Features

- ✅ Client Login using `client_key`
- 🔐 Access Secure Data with Bearer Token
- 🔁 Refresh Expired Access Token
- 👤 Fetch Current Authenticated Client
- 🚪 Logout with Token Invalidation
- 🧪 Fully Tested with Postman (Collection Included)

---

## 📦 Tech Stack

- **Python 3.11+**           ➤ Latest Python version for backend development.
- **FastAPI**                ➤ Lightweight, high-performance web framework for APIs.
- **Uvicorn**                ➤ ASGI server to run FastAPI apps.
- **JWT (python-jose)**      ➤ For generating and verifying access & refresh tokens.
- **Passlib (bcrypt)**       ➤ For secure password hashing (if added later).
- **SQLAlchemy**             ➤ ORM for database interactions.
- **SQLite**                 ➤ Lightweight relational DB for local development.
- **Pydantic**               ➤ Data validation & serialization.
- **python-multipart**       ➤ Required to handle form-data in FastAPI.

---

## 📁 Folder Structure
secure_api_project/
│
├── main.py               # Entry point for the FastAPI application
├── models.py             # SQLAlchemy models & DB setup
├── auth.py               # Authentication & token logic
├── routes/               # All API routes like login, register, refresh-token etc.
├── utils.py              # Utility functions (optional)
├── requirements.txt      # All dependencies listed
└── README.md             # Project documentation (to be written)

---

## 📬 API Endpoints

| Method | Endpoint             | Description                      |
|--------|----------------------|----------------------------------|
| POST   | `/login`             | Login with `client_key` and receive tokens |
| GET    | `/secure-data`       | Protected route (requires token) |
| GET    | `/me`                | Get current client info          |
| POST   | `/refresh-token`     | Generate new access token        |
| POST   | `/logout`            | Logout and invalidate token      |

---

## 🔐 Authentication Flow

1. 🔑 **Login:**
   - Send `client_key` to `/login`
   - Get back:
     - `access_token`
     - `refresh_token`
     - `user_id`

2. 📦 **Access Secure Route:**
   - Use `Authorization: Bearer <access_token>` in headers
   - Access `/secure-data` or `/me`

3. 🔄 **Refresh Token:**
   - Send `refresh_token` to `/refresh-token`
   - Get new `access_token`

4. 🚪 **Logout:**
   - Send `access_token` to `/logout`
   - Client should delete token from frontend

---

## 🧪 Postman Testing

We’ve included a Postman Collection for easy testing:


You can import this file into Postman to test:
- Login
- Token Refresh
- Secure Data Access
- Logout

---

## 💡 Developer Notes

- JWT tokens are signed and verified using a secret key.
- `refresh_token` has longer expiry than `access_token`.
- This API can be easily extended with user database, password authentication, roles, etc.

---

## 👨‍💻 Developed By

> **Mudassir Ijaz**  
> For: Client (Germany-based IT Office)  
> Stack: FastAPI + JWT + Postman  
> 📅 April 2025

---

## 📄 License

This project is private and built specifically for the client. Do not reuse without permission.
