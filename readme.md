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
     - `AUTH0_CLIENT_ID`: Your Application Client ID

3. **Login Method: <a name="login" id="login"></a>**
   - Use the following link to access application using Auth0 login method to generate JWT tokens.

    ```
    https://{{YOUR_DOMAIN}}/authorize?audience={{API_AUDIENCE}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
    ```
  - For the current deployed application you can use:
    1. url to login:
    ```
    https://dev-uda-fsnd.us.auth0.com/authorize?response_type=token&client_id=mXCarDz9poBmP7znSgT91KA1ErjtlVVE&redirect_uri=http://localhost:5000/login-results&audience=casting-capstone
    ```
    2. On successful verification you would get below callback url, with token:
    ```
      http://localhost:5000/login-results#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVOZkxXa2hKZTZfSzF5TDhFRVBHWiJ9.eyJpc3MiOiJodHRwczovL2Rldi11ZGEtZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjYwNDE0ZGFiMGQ3Nzc0ZmZjMWM2MmZkIiwiYXVkIjoiY2FzdGluZy1jYXBzdG9uZSIsImlhdCI6MTcxMTczMDE3NSwiZXhwIjoxNzExODE2NTc1LCJzY29wZSI6IiIsImF6cCI6Im1YQ2FyRHo5cG9CbVA3em5TZ1Q5MUtBMUVyanRsVlZFIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsInBvc3Q6YWN0b3JzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.MSUJ6gpoNklIcnRscAXgpdSG2MbctZNtxZL1kf5RO9oa7iFdr-tJAjhNyP6JRhG3rPzl2gpOA8gfocqO7LveW4RNZRm0K7QAYrO4DLFQwkYMDHGHPQ1LHI6Pg7bSWtIS9lZZlF2bIaFKhhDXcYG5HZzy101QRmTPX-tlrtwRu73vNEimck_sFXDGqVKcpruCcjSB2I3MXuUbKLw3UuTKS31J1ZDUhUkUtCPNHTeXhEzx_ES3oDlL_ujCY36eNSDMKxrUfd9GZlUc8Sg6J6V2EJApigQc-osRn4tMCv1Um8iLgkYnmXARtb62p_W_J_kA5J8gDL34rgOLZI4Aqvipvg&expires_in=86400&token_type=Bearer
    ```
    3. Copy the access_token to be used as jwt_token in Auth headers accross the application.
    ```
    eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVOZkxXa2hKZTZfSzF5TDhFRVBHWiJ9.eyJpc3MiOiJodHRwczovL2Rldi11ZGEtZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjYwNDE0ZGFiMGQ3Nzc0ZmZjMWM2MmZkIiwiYXVkIjoiY2FzdGluZy1jYXBzdG9uZSIsImlhdCI6MTcxMTczMDE3NSwiZXhwIjoxNzExODE2NTc1LCJzY29wZSI6IiIsImF6cCI6Im1YQ2FyRHo5cG9CbVA3em5TZ1Q5MUtBMUVyanRsVlZFIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsInBvc3Q6YWN0b3JzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.MSUJ6gpoNklIcnRscAXgpdSG2MbctZNtxZL1kf5RO9oa7iFdr-tJAjhNyP6JRhG3rPzl2gpOA8gfocqO7LveW4RNZRm0K7QAYrO4DLFQwkYMDHGHPQ1LHI6Pg7bSWtIS9lZZlF2bIaFKhhDXcYG5HZzy101QRmTPX-tlrtwRu73vNEimck_sFXDGqVKcpruCcjSB2I3MXuUbKLw3UuTKS31J1ZDUhUkUtCPNHTeXhEzx_ES3oDlL_ujCY36eNSDMKxrUfd9GZlUc8Sg6J6V2EJApigQc-osRn4tMCv1Um8iLgkYnmXARtb62p_W_J_kA5J8gDL34rgOLZI4Aqvipvg
    ```
   
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

##### Permissions

Following permissions should be created under created API settings.

* `view:actors`
* `view:movies`
* `delete:actors`
* `post:actors`
* `update:actors`
* `update:movies`
* `post:movies`
* `delete:movies`

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


# Database Migrations <a name="data-migrations" id="data-migrations"></a>

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
**Role specific postman collections are available for all the end points along with tests. please refer [Testing with Postman](#postman-collections) for details**
### Endpoints

#### GET /actors
- **Description:** Retrieves a list of all actors.
- **Permissions Required:** `view:actors`
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
              "name": "Anne Hathaway",
              "gender": "Female",
              "age": 52
          },
          {
              "id": 2,
              "name": "Matthew McConaughey",
              "gender": "Male",
              "age": 47
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
- **Permissions Required:** `post:actors`
- **Sample Request:**
  ```bash
  curl -X POST https://casting-capstone.onrender.com/actors -H "Authorization: Bearer <YOUR_TOKEN>" -H "Content-Type: application/json" -d '{"name": "Ana de Armas", "age": 33, "gender: "Female"}'
  ```
- **Sample Response (Success):**
  ```json
  {
      "actor_id": 3,
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
- **Permissions Required:** `update:actors`
- **Sample Request:**
  ```bash
  curl -X PATCH https://casting-capstone.onrender.com/actors/1 -H "Authorization: Bearer <YOUR_TOKEN>" -H "Content-Type: application/json" -d '{"full_name": "Anne Jacqueline Hathaway"}'
  ```
- **Sample Response (Success):**
  ```json
  {
      "success": true,
      "updated_actor": [{
          "id": 1,
          "name": "Anne Hathaway",
          "gender": "Female",
          "age": 52
      }]
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
- **Permissions Required:** `delete:actors`
- **Sample Request:**
  ```bash
  curl -X DELETE https://casting-capstone.onrender.com/actors/1 -H "Authorization: Bearer <YOUR_TOKEN>"
  ```
- **Sample Response (Success):**
  ```json
  {
      "message": "Actor {actor_id} deleted",
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
- **Permissions Required:** `view:movies`
- **Sample Request:**
  ```bash
  curl -X GET https://casting-capstone.onrender.com/movies -H "Authorization: Bearer <YOUR_TOKEN>"
  ```
- **Sample Response (Success):**
  ```json
  {
      "movies": [
          {
            "actors": [
                "Brad Pitt"
            ],
            "id": 351,
            "release_date": "1994-09-23",
            "title": "The Shawshank Redemption"
        },
        {
            "actors": [
                "Leonardo DiCaprio"
            ],
            "id": 352,
            "release_date": "1972-03-24",
            "title": "The Godfather"
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
- **Permissions Required:** `post:movies`
- **Sample Request:**
  ```bash
  curl -X POST https://casting-capstone.onrender.com/movies -H "Authorization: Bearer <YOUR_TOKEN>" -H "Content-Type: application/json" -d '{"title": "Knives Out", "duration": 130, "release_year": 2019, "imdb_rating": 7.9, "cast": ["Ana de Armas"]}'
  ```
- **Sample Response (Success):**
  ```json
  {
      "movie_id": 3,
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
- **Permissions Required:** `update:movies`
- **Sample Request:**
  ```bash
  curl -X PATCH https://casting-capstone.onrender.com/movies/1 -H "Authorization: Bearer <YOUR_TOKEN>" -H "Content-Type: application/json" -d '{"title": "Updated Movie Title", "release_date": "2024-03-27"}'
  ```
- **Sample Response (Success):**
  ```json
  {
      "updated_movie": {
          "id": 1,
          "title": "Serenity",
          "release_date": "2024-03-27",
          "actors": ["Anne Hathaway", "Matthew McConaughey"]
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
- **Permissions Required:** `delete:movies`
- **Sample Request:**
  ```bash
  curl -X DELETE https://casting-capstone.onrender.com/movies/1 -H "Authorization: Bearer <YOUR_TOKEN>"
  ```
- **Sample Response (Success):**
  ```json
  {
      "message": "Movie {{movie_id}} deleted",
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

## Using Postman Collection <a name="postman-collections" id="postman-collections"></a>
- The repository contains 3 different collection for each role, with automated tests written to verify all the endpoints. The different collections are:
1. `Casting Assistant Actor-Movie CRUD with RBAC Tests.postman_collection.json`
2. `Casting Director Actor-Movie CRUD with RBAC Tests.postman_collection.json`
3. `Executive Producer Actor-Movie CRUD with RBAC Tests.postman_collection.json`

- To execute the test, please imprt the json in postman and follow below steps:
  - Login to application with the user of correct role profile, refer [Login to application](#login).
  - Once the jwt_token is retrieved, open the Variables section of the collection and update current value for ```jwt_token``` field
  - After the token is set, save the updated collection.
  - Run the Post man collection to execute automated tests or use the dedicated url endpoint test specific cases.






