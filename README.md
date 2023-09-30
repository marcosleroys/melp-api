# MELP API

RESTful API for Melp application. Developed with Flask.

One model is implemented, the Restaurant model.

Current deployment is in Render, automatically deploys after any pus to main branch in the repo.

Main libraries used:
1. Flask - To handle API requests.
2. psycopg2 - library that adds support for postgreSQL.

* main.py - flask application initialization, with endpoints for API.
* initDB.py - simple script to initialize database from CSV file (restaurantes.csv)

## Running 

1. Clone repository.
2. `pip install requirements.txt`
3. Create `.env` file and add `DB_URL` variable
4. Run the server with the following command: `python main.py`



## Usage
### Restaurants endpoint
#### Get Restaurant by Id
GET https://melp-7rss.onrender.com/restaurants/{id}

RESPONSE
```json
{
    "restaurant": {
        "city": "Mateofurt",
        "email": "Brandon_Vigil@hotmail.com",
        "id": "4e17896d-a26f-44ae-a8a4-5fbd5cde79b0",
        "lat": 19.437904276995,
        "lng": -99.1286576775023,
        "name": "Hernández - Lira",
        "phone": "570 746 998",
        "rating": 0,
        "site": "http://graciela.com.mx",
        "state": "Hidalgo",
        "street": "93725 Erick Arroyo"
    }
}
```

#### Create restaurant
POST https://melp-7rss.onrender.com/restaurants/create

REQUEST
```json
{
    "rating" : 2,
    "name" : "Marcos Techy Soups", 
    "site" : "http://techysoups.com.mx", 
    "email" : "techysoups@gmail.com", 
    "phone" : "811 567 890", 
    "street" : "Revolucion", 
    "city" : "Monterrey", 
    "state" : "Nuevo Leon", 
    "lat" : 19.4400570537241, 
    "lng" : -99.1270470968249
}
```
RESPONSE
```json
{
    "message": "Created restaurant successfully",
    "name": "Marcos Techy Soups",
    "restaurant_id": "82efc378-323c-4a38-ac43-8c8d1a65d87b"
}
```
#### Delete restaurant by Id
DELETE https://melp-7rss.onrender.com/restaurants/{id}

RESPONSE
```json
{
    "deleted_id": "c0ffd058-e773-47f1-974b-42d41cb555bf",
    "message": " Successfully deleted the rows.",
    "rows_deleted": 1
}
```
#### Get restaurants in radius
GET https://melp-7rss.onrender.com/restaurants/statistics?longitude={lng}&latitude={lat}&radius={radius}

RESPONSE
```json
{
    "avg": 1.8,
    "count": 5,
    "restaurants": [],
    "std": 1.4832396974191326
}
```
