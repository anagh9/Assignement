# My Django Project

## Overview

This is a Django project that provides functionality for a social networking application. It includes APIs for user authentication, friend requests, and searching users.

## Getting Started

### Prerequisites

- Docker (v20.10 or later)
- Docker Compose (optional, if you prefer to use Docker Compose)

### Setting Up the Project

1. **Clone the Repository**

   First, clone the repository to your local machine:

   ```bash
   git clone https://github.com/anagh9/Assignement.git
   cd Assignement

2. **Run this to build and start the Docker container **
    ```bash
    docker-compose up --build

3. **List of all Apis**

    ```bash
    User Signup: 
    POST /api/signup/ - Create a new user account.
    
    User Login: 
    POST /api/login/ - Authenticate a user and receive access and refresh tokens.

    User Search:
    GET /api/search/?search="name" - Searches for users based on the search query parameter. If the query matches an exact email (case-insensitive), it returns that user. If the query contains any part of a user’s name, it returns a list of users with names that match the query. Results are paginated with a default limit of 10 records per page

    Send Friend Request: 
    POST /api/friend-request/send/<user_id>/ - Send a friend request to a user.

    Accept Friend Request:
    POST /api/friend-request/accept/<user_id>/ - Accept a friend request.

    Reject Friend Request:
    POST /api/friend-request/reject/<user_id>/ - Reject a friend request.

    List Friends:
    GET /api/friends/ - Get a list of friends.

    List Pending Friend Requests:
    GET /api/friend-requests/pending/ - Get a list of pending friend requests.

## 

"The collection has already been uploaded. Import it into Postman and use it."
