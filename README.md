# fs-nd-eventos
## Project Description
- EventOS is an event management API that allows the users to create events and register on them. The backend is designed to work for different user types including admins, managers, participants in addition to public users.
- a live version can be found here: https://fs-nd-eventos.herokuapp.com
- _This project was part of Udacity Full Stack Developer Nanodegree._
## Getting Started
### Requirements
- PostgreSQL
- Python3
#### Key Dependencies
- Flask
- SQLAlchemy
- Flask-CORS
- Psycopg2
### Installation
After installing the requirements, preparing the environment, cloning or downloading the repository, you need setup the database and the application.
#### Database Setup
1. Run `pg_ctl -D <your DB Server Name> start`, to start your DB server.
    > Note: you might need to change your working directory to where you have initiated the DB Server.
2. Run `createdb eventos`, to create a DB with the name `eventos`.
3. Run `psql eventos < eventos.psql`, to populate tables with some predefined data.
    > Note: you need to change your working directory to the root `/` directory of the project.
#### Application Setup
1. Navigate to the root `/` directory of the project.
2. Run `pip install -r requirements.txt`, to install the required dependencies for the application.
3. Go `models/models.py` and set the following variables:
    ```python
    database_name = "eventos"
    #this must be the same name as you have created earlier
    database_path = "postgresql://{}/{}".format('localhost:5432', database_name)
    #db_url follows '[dialec]+[DBAPI(optional)]://[username]:[password(optional)]@[host]:[port]/[database_name]'
    ```
4. Run `FLASK_APP=app.api FLASK_DEBUG=true FLASK_ENV=development flask run --reload`, to start the flask application
## Testing
The testing of all endpoints was implemented with `unittest`. Each endpoint can be tested with one success test case and one error test case. RBAC feature can also be tested for participant, manager, and admin.
#### Testing Setup
1. Run `createdb test_eventos`, to create a DB with the name `test_eventos` for testing purpose.
2. Run `psql eventos < eventos.psql`, to populate tables with some predefined data.
3. Run `python3 test_app.py`, to execute test cases
## Data Models
#### events
- Description: an event is the core data of the system.
- Relations: an event has one manager, an event has many participants.
- Attributes:
    ```json
    id: integer
    name: string
    genre: [string]
    province: string
    city: string
    date: datetime
    image_link: string
    manager_id: integer
    ```
#### managers
- Description: a manager is the creator and moderator of the event.
- Relations: a manager can create many events.
- Attributes:
    ```json
    id: integer
    name: string
    phone: string
    website: string
    image_link: string
    ```
#### participants
- Description: a participant is a user that registered on an event.
- Relations: a participant can join many events.
- Attributes:
    ```json
    id: integer
    name: string
    phone: string
    ```
## RBAC credentials and roles
Auth0 was set up to manage role-based access control for three users. The API documentation below describes, among others, by which user the endpoints can be accessed. Access credentials and permissions are handled with JWT tokens which must be included in the request header.
### Permissions
- There are publicly available endpoints that do not require authorization. This is done to ensure every user can see the general information about events and event creators.
- There are some endpoints which requires the user to have certain permissions, as follows.
#### Participant
- `post:participant` : create a new participant
- `delete:participant` : delete a participant
#### Manager
- participant permissions
- `post:event` : create a new event
- `delete:event` : delete an event
- `patch:event` : edit and update an event
#### Admin
- manager and participant permissions
- `post:manager` : create a new manager
- `delete:manager` : delete a manager
## API Reference
All requests and responses are JSON
### Endpoints
#### Event
#### `GET /`
- description: test the api
- request: N/A
- response: `success: boolean`
- sample request: N/A
- sample response:
    ```json
    {
        "success": true
    }
    ```
#### `GET /event`
- description: get the list of all events
- request: N/A
- response: `success: boolean` , `events: event`
- sample request: N/A
- sample response:
    ```json
    {
        "success": true,
        "events": [
            {
            "id": 1,
            "name": "event-1",
            "genre": ["Music"],
            "province": "Makkah",
            "city": "Jeddah",
            "date": 02-28-2021,
            "image_link": null,
            "manager_id": 1
            }
        ]
    }
    ```
#### `POST /event`
- description: create a new event
- request: `name: string` , `genre: [string]` , `province: string` , `city: string` , `date: datetime` , `image_link: string` , `manager_id: integer`
- response: `success: boolean` , `event: event`
- sample request:
    ```json
    {
        "event": {
            "name": "event-1",
            "genre": ["Music"],
            "province": "Makkah",
            "city": "Jeddah",
            "date": 02-28-2021,
            "image_link": null,
            "manager_id": 1
        }
    }
    ```
- sample response:
    ```json
    {
        "success": true,
        "event": {
            "id": 1,
            "name": "event-1",
            "genre": ["Music"],
            "province": "Makkah",
            "city": "Jeddah",
            "date": 02-28-2021,
            "image_link": null,
            "manager_id": 1
        }
    }
    ```
#### `DELETE /event`
- description: delete an event
- request: `id: integer`
- response: `success: boolean` , `deleted: event`
- sample request:
    ```json
    {
        "id": 1
    }
    ```
- sample response:
    ```json
    {
        "success": true,
        "deleted": {
            "id": 1,
            "name": "event-1",
            "genre": ["Music"],
            "province": "Makkah",
            "city": "Jeddah",
            "date": 02-28-2021,
            "image_link": null,
            "manager_id": 1
        }
    }
    ```
#### `PATCH /event`
- description: edit and update an event
- request: `id: integer` , `name: string` , `genre: [string]` , `province: string` , `city: string` , `date: datetime` , `image_link: string` , `manager_id: integer`
- response: `success: boolean` , `event: event`
- sample request:
    ```json
    {
        "id": 1,
        "name": "event-2",
        "genre": ["Movie"],
        "province": "Makkah",
        "city": "Jeddah",
        "date": 02-28-2021,
        "image_link": null,
        "manager_id": 1
    }
    ```
- sample response:
    ```json
    {
        "success": true,
        "event": {
            "city": "Jeddah",
            "date": 02-28-2021,
            "genre": ["Makkah"],
            "id": 1,
            "image_link": null,
            "manager_id": 1,
            "name": "event-2",
            "province": "Makkah"
        }
    }
    ```
#### `GET /manager`
- description: get the list of all managers
- request: N/A
- response: `success: boolean` , `managers: manager`
- sample request: N/A
- sample response:
    ```json
    {
        "success": true,
        "managers": [
            {
            "id": 1,
            "name": "event-1",
            "phone": "0501234567",
            "website": null,
            "image_link": null
            }
        ]
    }
    ```
#### `POST /manager`
- description: create a new manager
- request: `name: string` , `phone: string` , `website: string` , `image_link: string`
- response: `success: boolean` , `manager: manager`
- sample request:
    ```json
    {
        "manager": {
            "name": "manager-1",
            "phone": "0501234567",
            "website": null,
            "image_link": null
        }
    }
    ```
- sample response:
    ```json
    {
        "success": true,
        "manager": {
            "id": 1,
            "name": "manager-1",
            "phone": "0501234567",
            "website": null,
            "image_link": null
        }
    }
    ```
#### `DELETE /manager`
- description: delete a manager
- request: `id: integer`
- response: `success: boolean` , `deleted: manager`
- sample request:
    ```json
    {
        "id": 1
    }
    ```
- sample response:
    ```json
    {
        "success": true,
        "deleted": {
            "id": 1,
            "name": "manager-1",
            "phone": "0501234567",
            "website": null,
            "image_link": null
        }
    }
    ```
#### `GET /participant`
- description: get the list of all participants
- request: N/A
- response: `success: boolean` , `participants: participant`
- sample request: N/A
- sample response:
    ```json
    {
        "success": true,
        "participants": [
            {
                "id": 1,
                "name": "participant-1",
                "phone": "0501234567"
            }
        ]
    }
    ```
#### `POST /participant`
- description: create a new participant
- request: `name: string` , `phone: string`
- response: `success: boolean` , `participant: participant`
- sample request:
    ```json
    {
        "participant": {
            "name": "participant-1",
            "phone": "0501234567"
        }
    }
    ```
- sample response:
    ```json
    {
        "success": true,
        "participant": {
            "id": 1,
            "name": "participant-1",
            "phone": "0501234567"
        }
    }
    ```
#### `DELETE /participant`
- description: delete a participant
- request: `id: integer`
- response: `success: boolean` , `deleted: participant`
- sample request:
    ```json
    {
        "id": 1
    }
    ```
- sample response:
    ```json
    {
        "success": true,
        "deleted": {
            "id": 1,
            "name": "participant-1",
            "phone": "0501234567"
        }
    }
    ```
### Error Handling
- response: `success: boolean` , `error: integer` , `message: string`
- sample response:
    ```json
    {
        "success": false,
        "error": 400,
        "message": "Bad Request"
    }
    ```
