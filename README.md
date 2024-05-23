# Rate-Limit

We all understand the basics of APIs, but what about the Rate Limit?
API creation is not a significant deal, but the right standard format for creating APIs
It's a challenging section.

# Prerequisites:
 1. Python
 2. Docker
 3. Basic knowledge about Rate Limit

# Python frameworks included are:
In application we are use one librarie.
 1. Flask (microservice framework)

# Follow Below steps to run game.
 1. Create folder and clone repo.
 2. Create environment.
    ```bash
    python3 -m venv env
    ```
 3. Activate environment.
    ```bash
    source env/bin/activate
    ```
 4. Install requirement.txt.
    ```bash
    pip install requirement.txt
    ```
 5. Run game.
    ```bash
    python app.py
    ```

# Build application with docker file.
 1. Create folder and clone repo.
 2. Active application.
   ```bash
   docker compose up
   ```

# Note: 

 1. By default, the application uses the `fix window rate limit` algorithm.
 2. In the application, we built a rate limit algorithm on middleware.

## What is the middleware?
Middleware is the bridge 🧐

Bridge: Yes, a bridge with one part connected to the application and the other to the users.
Every request and response should pass via middleware. Middleware is optional, such as counting incoming users' IP addresses. 
Use middleware to fetch IP addresses for each user.
