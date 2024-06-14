# Django Social Network Application

### Prerequisites
- Python 3.11.4
- Docker
- Postgresql 16

## Description

This project is a social networking application API built with Django and Django Rest Framework. It includes functionalities for user authentication, sending and accepting friend requests, and searching for users.

## Features

- User authentication (signup, login)
- Friend request management (send, accept, reject)
- User search by email and name

## Installation Steps

1. **Clone the repository:**
    ```sh
    git clone https://github.com/sethu45/social_network.git
    cd social_network
    ```

2. **Create a virtual environment and activate it (Optional if using Docker):**
    ```sh
    python3 -m venv venv  
    `venv\Scripts\activate` # activate virtual environment on Windows
    ```

3. **Install dependencies (Optional if using Docker):**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run migrations (Optional if using Docker):**
    ```sh
    python manage.py migrate
    ```

5. **Create a superuser (Optional if using Docker):**
    ```sh
    python manage.py createsuperuser
    ```

6. **Start the development server (Optional if using Docker):**
    ```sh
    python manage.py runserver
    ```

## Docker

To containerize the application, use the provided `docker-compose.yml` and `Dockerfile`.
before running build command, change postgres detail in db name, username, password in `docker-compose.yml` and setting.py

### Build and Run

1. **Build Docker containers:**
    ```sh
    docker-compose build
    ```

2. **Run Docker containers:**
    ```sh
    docker-compose up
    ```


3.  **Run Migrate command in another cmd :**
    ```sh
    docker exec -it <container-name> /bin/bash 
    (or)
    docker exec -it <container-name> /bin/sh
    ```

## API Endpoints

### Auth Endpoints
- `POST /signup/`: Register a new user.
- `POST /login/`: Log in and obtain authentication tokens.

### User Endpoints
- `GET /search/`: List users with pagination and search.
- `POST /send_requests/`: Send a friend request.
- `POST /accept_requests/`: Accept a friend request.
- `POST /reject_request/`: Reject a friend request.
- `GET /list_friends/`: List all friends that accepted by user.
- `GET /pending_list/`: List all pending friend list that need to be accept or reject.

## Postman Collection

The Postman collection for the API endpoints can be found in the `postman_collection.json` file in the root directory.

