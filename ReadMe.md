# Flask JWT Authentication API Demo

## Overview
This is a demo **API** application built using **Flask**, **JWT (JSON Web Tokens)**, and **SQLAlchemy** with SQLite and Redis. 
The application follows best practices for user authentication and password management, including salting and hashing passwords.
It implements key **design patterns** and ensures token-based security using JWT.

## Features

- **API-based** user authentication using JWT.
- **Token-based** access control for all user actions.
- **Salting** and hashing of passwords for enhanced security.
- **Full CRUD** operations on the User model (create, read, update, delete).
- **Redis** integration for token revocation and renewal management.
- **Token expiry** and refresh functionality.
- **Implements Facade Pattern** for handling authentication and business logic.

## Design Patterns Used

- **Facade Pattern**: The authentication logic is encapsulated in a facade (`AuthFacade`), making the API structure more modular and separating concerns.
- **Singleton Pattern**: The `AuthService` and the `UserService` classes are implemented as singleton to ensure only one instance handles authentication logic or user logic, respectively, reducing overhead.
  
## Prerequisites
- Python 3.x
- pip (Python package manager)
- Redis (For token management)
## Token Renewal

The application uses JSON Web Tokens (JWT) for secure user authentication. Each token has an expiration time for security purposes. Once a token expires, the user can renew it to continue accessing protected routes without having to re-authenticate. Here’s how token renewal is handled:

### Token Expiration and Renewal Process

- **Token Expiration**: Each JWT token contains an `exp` field (expiration time) that defines how long the token is valid. Once this time is reached, the token becomes invalid.
- **Renewal Mechanism**: When a token is close to expiration or has expired, the user can request a new token. The `AuthFacade` handles this through the `renew_token` method, which verifies the current token and issues a new one with an extended expiration time.

### How Token Renewal Works

1. **Validate the Token**: When a request is made with a token, the `jwt_required` decorator validates whether the token is still valid or has expired.
   
2. **Renew the Token**: If the token is valid, the system issues a new JWT with a refreshed `exp` (expiration) value. The renewal process generates a new token using the `renew_token` method from the `AuthService` class. The new token includes:
   - The user’s ID (`user_id`)
   - A new expiration timestamp (`exp`)
   - A new token identifier (`jti`)

3. **Set Token in Redis**: After generating the new token, the system stores it in Redis, associating it with the new expiration timestamp to ensure it’s only valid for the specified time.

### Security Considerations for Token Renewal

- **Short-Lived Tokens**: Tokens are deliberately kept short-lived (e.g., 35 minutes) to limit the potential damage if a token is compromised. Users must request a new token if their current token expires.
- **Revoking Tokens**: If a token is revoked, it will be removed from Redis, and the user must re-authenticate to obtain a new token. This ensures that expired or revoked tokens cannot be reused.

## Routes Documentation
### User Routes
- **POST /user**: Create a new user.
  - Request Body: `{ "username": "string", "password": "string" }`
  - Response: `{ "message": "User created successfully" }`

- **GET /user**: Get the current user's information.
  - Headers: `Authorization: Bearer <token>`
  - Response: `{ "user": { "id": "int", "username": "string" }, "token": "string" }`

- **PUT /user**: Update the current user's information.
  - Headers: `Authorization: Bearer <token>`
  - Request Body: `{ "username": "string", "password": "string" }`
  - Response: `{ "message": "User updated successfully", "token": "string" }`

- **DELETE /user**: Delete the current user's account.
  - Headers: `Authorization: Bearer <token>`
  - Response: `{ "message": "User deleted successfully" }`

### Authentication Routes
- **POST /authenticate_user**: Authenticate a user and get a token.
  - Request Body: `{ "username": "string", "password": "string" }`
  - Response: `{ "token": "string" }`

- **POST /validate_token**: Validate a token.
  - Request Body: `{ "token": "string" }`
  - Response: `{ "message":"Token is valid": "token":"sting" }`

- **POST /logout**: Logout a user.
  - Request Body: `{ "token": "string" }`
  - Response: `{ "message": "Logged out successfully" }`
## Project Structure
The project is structured as follows:
```
├── main.py                  # Main application file
├── models
│   └── user.py             # User model and database definitions
├── services
│   └── auth_service.py      # Authentication logic and JWT handling
│   └── user_service.py      # User CRUD operations
├── facades
│   └── auth_facade.py       # Facade layer for login and validation
│   └── user_facade.py       # Facade layer for user operations
├── tests
│   └── test_auth.py         # Unit tests
├── README.md                # Project README
└── .env (optional)          # Environment variables (not committed- developmet default are located in auth_service.py)

```
### .env File
The `.env` file is used to store environment variables for the application. The following variables are used:
- 'JWT_KEY': The secret key used to sign JWT tokens.
- 'REDIS_HOST': The Redis server host.
- 'REDIS_PORT': The Redis server port.

## Password Salting and Hashing
- **Salting**: Before storing the user's password, the system generates a random salt (a sequence of random bytes) and concatenates it with the password. This helps protect against rainbow table attacks.
- **Hashing**: The salted password is hashed using the PBKDF2 (Password-Based Key Derivation Function 2) algorithm with the SHA-256 hashing function.
Token Management
- **Redis**: Tokens are stored and managed in Redis. When a token is created, its jti (JWT ID) is stored in Redis with an expiration time. If a token is revoked, the jti is removed from Redis.
- **Token Expiry**: Tokens expire after 35 minutes, but users can renew them within the application.
## Running tests
To run the tests, use the following command:
```python -m unittest tests/test_auth.py```
## Running the Demo
in the root directory, run the following command:
```python main.py```
### Prerequisites
- Python 3.10+
- `pip` (Python package installer)
- Redis server
### Sqlite Database
The application uses an SQLite database to store user information. 
The database file (`users.db`) 
for creating the BD file a db_creator.py could be used to create the database file.
the command to create the database file is:
```python db_creator.py```
#### config
the database configuration is located in the main.py file:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
```
## Contributing
Feel free to fork the project and submit pull requests for improvements or bug fixes.

## License
This project is open-source and available under the MIT License.