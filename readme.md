# Casting Agency API

## Motivation
This project serves as the capstone project for Udacity's Full Stack Developer Nanodegree. The Casting Agency API is a backend application that allows users to manage actors and movies within the context of a casting agency. It provides endpoints for retrieving, creating, updating, and deleting actors and movies. Additionally, it implements Role-Based Access Control (RBAC) to control access to these endpoints based on user roles.

## Hosted API
The API is currently hosted on render. You can access it at the following URL:
[https://casting-capstone.onrender.com](https://casting-capstone.onrender.com)

## Authentication Setup
The application uses Auth0 for authentication. To set up authentication and test the endpoints, follow these steps:

1. **Auth0 Setup:**
   - Sign up or log in to your Auth0 account.
   - Create a new API and note down the following details:
     - Domain
     - API Audience
   - Create three different roles: Casting Assistant, Casting Director, and Executive Producer, each with their respective permissions.

2. **Environment Variables:**
   - Set the following environment variables with your Auth0 details:
     - `AUTH0_DOMAIN`: Your Auth0 domain.
     - `API_AUDIENCE`: Your API Audience.

3. **Login Method:**
   - Use the provided Auth0 login method to generate JWT tokens for testing the endpoints.
   
4. **Update Role Tokens:**
   - Update the `role_token.json` file with the generated tokens for each role.

## RBAC Details

- **Casting Assistant:**
  - Permissions:
    - View actors and movies.

- **Casting Director:**
  - Permissions (in addition to Casting Assistant):
    - Add or delete an actor from the database.
    - Modify actors or movies.

- **Executive Producer:**
  - Permissions (in addition to Casting Director):
    - Add or delete a movie from the database.

## Local Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Tia18s/casting_capstone.git
   cd casting_capstone
   ```

2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables Setup:**
   - Run the `setup.sh` script to set up environment variables required for local development.

5. **Database Setup:**
   - You can create DB with empty tables using:
      - login to psql DB
      - execute below script to create a new DB
      ```
      CREATE DATABASE <database_name>
      ```
      - follow steps in [Database Migrations](#data-migrations) to setup and perform migrations.

    ***or to use default data and schema:***
   - Run the `setup_db.sh` script to initialize the database and populate initial data.

6. **Running the Server:**
   - Execute the `run.sh` script to start the development server.


# Database Migrations <a name="data-migrations"></a>

## Prerequisites
Make sure you have Flask-Migrate installed in your virtual environment. If not, you can install it using pip:

```bash
pip install Flask-Migrate
```

## Performing Migrations

1. **Initialize Migration Repository:**
   If you haven't already initialized the migration repository, you can do so by running:
   
   ```bash
   flask db init
   ```

2. **Generate Migration Script:**
   Whenever you make changes to your database models, you need to generate a migration script. Run the following command to generate the migration script:
   
   ```bash
   flask db migrate -m "Your migration message"
   ```

3. **Apply Migration:**
   Once the migration script is generated, you can apply the migration to your database by running:
   
   ```bash
   flask db upgrade
   ```

4. **Downgrade Migration (if needed):**
   In case you need to revert the changes made by a migration, you can downgrade the migration by running:
   
   ```bash
   flask db downgrade
   ```

5. **View Migration History:**
   To view the migration history and check the status of migrations, you can use the following command:
   
   ```bash
   flask db history
   ```

These commands will help you manage your database migrations effectively when making changes to your application's database models.

## Unit Testing

1. **Database Setup for Testing:**
   - Run the `setup_test_db.sh` script to set up the test database.

2. **Environment Variables for Testing:**
   - Run the `setup.sh` script to set up environment variables required for testing.

3. **Running Tests:**
   - Execute the `run_test.sh` script to run the unit tests.

## API Documentation

### Endpoints

#### GET /actors
- **Description:** Retrieves a list of all actors.
- **Permissions Required:** `get:actors`
- **Sample Request:**
  ```bash
  curl -X GET https://casting-capstone.onrender.com/actors -H "Authorization: Bearer <YOUR_TOKEN>"
  ```
- **Sample Response (Success):**
  ```json
  {
      "actors": [
          {
              "id": 1,
              "name": "Anne Hathaway"
          },
          {
              "id": 2,
              "name": "Matthew McConaughey"
          }
      ],
      "success": true
  }
  ```
- **Sample Response (Error):**
  ```json
  {
      "error": "Not Found",
      "message": "No actors"
  }
  ```

#### POST /actors
- **Description:** Creates a new actor.
- **Permissions Required:** `post:actor`
- **Sample Request:**
  ```bash
  curl -X POST https://casting-capstone.onrender.com/actors -H "Authorization: Bearer <YOUR_TOKEN>" -H "Content-Type: application/json" -d '{"name": "Ana de Armas", "date_of_birth": "April 30, 1988"}'
  ```
- **Sample Response (Success):**
  ```json
  {
      "created_actor_id": 3,
      "success": true
  }
  ```
- **Sample Response (Error):**
  ```json
  {
      "error": "Bad Request",
      "message": "Name, age, and gender are required"
  }
  ```

#### PATCH /actors/{actor_id}

- **Description:** Updates the information of a specific actor.
- **Permissions Required:** `patch:actor`
- **Sample Request:**
  ```bash
  curl -X PATCH https://casting-capstone.onrender.com/actors/1 -H "Authorization: Bearer <YOUR_TOKEN>" -H "Content-Type: application/json" -d '{"full_name": "Anne Jacqueline Hathaway"}'
  ```
- **Sample Response (Success):**
  ```json
  {
      "actor_info": {
          "id": 1,
          "name": "Anne Hathaway",
          "date_of_birth": "November 12, 1982",
          "movies": ["Serenity"]
      },
      "success": true
  }
  ```
- **Sample Response (Error):**
  ```json
  {
      "error": "Not Found",
      "message": "Actor not found"
  }
  ```

#### DELETE /actors/{actor_id}

- **Description:** Deletes a specific actor.
- **Permissions Required:** `delete:actor`
- **Sample Request:**
  ```bash
  curl -X DELETE https://casting-capstone.onrender.com/actors/1 -H "Authorization: Bearer <YOUR_TOKEN>"
  ```
- **Sample Response (Success):**
  ```json
  {
      "deleted_actor_id": 1,
      "success": true
  }
  ```
- **Sample Response (Error):**
  ```json
  {
      "error": "Not Found",
      "message": "Actor not found"
  }
  ```

#### GET /movies

- **Description:** Retrieves a list of all movies.
- **Permissions Required:** `get:movies`
- **Sample Request:**
  ```bash
  curl -X GET https://casting-capstone.onrender.com/movies -H "Authorization: Bearer <YOUR_TOKEN>"
  ```
- **Sample Response (Success):**
  ```json
  {
      "movies": [
          {
              "id": 1,
              "title": "Serenity",
              "release_year": 2019
          },
          {
              "id": 2,
              "title": "Birds of Prey",
              "release_year": 2020
          }
      ],
      "success": true
  }
  ```
- **Sample Response (Error):**
  ```json
  {
      "error": "Not Found",
      "message": "No movies"
  }
  ```

#### POST /movies

- **Description:** Creates a new movie.
- **Permissions Required:** `post:movie`
- **Sample Request:**
  ```bash
  curl -X POST https://casting-capstone.onrender.com/movies -H "Authorization: Bearer <YOUR_TOKEN>" -H "Content-Type: application/json" -d '{"title": "Knives Out", "duration": 130, "release_year": 2019, "imdb_rating": 7.9, "cast": ["Ana de Armas"]}'
  ```
- **Sample Response (Success):**
  ```json
  {
      "created_movie_id": 3,
      "success": true
  }
  ```
- **Sample Response (Error):**
  ```json
  {
      "error": "Bad Request",
      "message": "Title and release_date are required"
  }
  ```

#### PATCH /movies/{movie_id}

- **Description:** Updates the information of a specific movie.
- **Permissions Required:** `patch:movie`
- **Sample Request:**
  ```bash
  curl -X PATCH https://casting-capstone.onrender.com/movies/1 -H "Authorization: Bearer <YOUR_TOKEN>" -H "Content-Type: application/json" -d '{"imdb_rating": 8.1}'
  ```
- **Sample Response (Success):**
  ```json
  {
      "movie_info": {
          "id": 1,
          "title": "Serenity",
          "duration": 106,
          "imdb_rating": 8.1,
          "release_year": 2019,
          "cast": ["Anne Hathaway", "Matthew McConaughey"]
      },
      "success": true
  }
  ```
- **Sample Response (Error):**
  ```json
  {
      "error": "Not Found",
      "message": "Movie not found"
  }
  ```

#### DELETE /movies/{movie_id}

- **Description:** Deletes a specific movie.
- **Permissions Required:** `delete:movie`
- **Sample Request:**
  ```bash
  curl -X DELETE https://casting-capstone.onrender.com/movies/1 -H "Authorization: Bearer <YOUR_TOKEN>"
  ```
- **Sample Response (Success):**
  ```json
  {
      "deleted_movie_id": 1,
      "success": true
  }
  ```
- **Sample Response (Error):**
  ```json
  {
      "error": "Not Found",
      "message": "Movie not found"
  }
  ```

