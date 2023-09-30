import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd

load_dotenv()

db_url = os.getenv('DB_URL')

# Function used to populate database from csv when service is initialized
def initialize_database(db_url):
    conn = psycopg2.connect(db_url)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Enable postGIS
    cur.execute('CREATE EXTENSION IF NOT EXISTS postgis')

    # Execute a command: this creates a new table from blank
    cur.execute('DROP TABLE IF EXISTS Restaurants;')
    cur.execute('CREATE TABLE Restaurants (id text PRIMARY KEY,'
                                    'rating integer,'
                                    'name text,'
                                    'site text,'
                                    'email text,'
                                    'phone text,'
                                    'street text,'
                                    'city text,'
                                    'state text,'
                                    'lat float,'
                                    'lng float);'
                                    )

    filename = 'restaurantes.csv'
    # Open file with pandas
    df= pd.read_csv(filename)

    # Iterate the df to execute an insert into database for each row
    for i, row in df.iterrows():

        restaurant_id = row['id']
        rating = row['rating']
        name = row['name'].replace('"',"") # Csv file contains names with quotes and some without, removing for consistency
        site = row['site']
        email = row['email']
        phone = row['phone']
        street = row['street']
        city = row['city']
        state = row['state']
        lat = row['lat']
        lng = row['lng']

        # Insert row into the table

        cur.execute('INSERT INTO Restaurants (id, rating, name, site, email, phone, street, city, state, lat, lng)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (restaurant_id, rating, name, site, email, phone, street, city, state, lat, lng))


    conn.commit()

    cur.close()
    conn.close()

initialize_database(db_url)