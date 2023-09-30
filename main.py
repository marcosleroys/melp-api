import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras
import uuid
import statistics
from initDB import initialize_database

load_dotenv()

app = Flask(__name__)

db_url = os.getenv('DB_URL')

def get_db_connection():
    conn = psycopg2.connect(db_url)
    return conn

@app.route('/restaurants/create', methods=['POST'])
def create_restaurant():
    data = request.get_json()

    params = ('rating', 'name', 'site', 'email', 'phone', 'street', 'city', 'state', 'lat', 'lng')

    # When all parameters are included in the request, insert into database
    if all(key in data for key in params):
        conn = get_db_connection()
        cur = conn.cursor()

        # create uuid for restaurant
        restaurant_id = str(uuid.uuid4())
        
        cur.execute('INSERT INTO Restaurants (id, rating, name, site, email, phone, street, city, state, lat, lng)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (restaurant_id, data['rating'], data['name'], data['site'], data['email'], data['phone'], data['street'], data['city'], data['state'], data['lat'], data['lng']))
    else:
        return jsonify({'error': "Parameters missing in body"}), 400
    
    result = {
        'restaurant_id': restaurant_id,
        'name' : data['name'],
        'message' : "Created restaurant successfully"
    }

    conn.commit()

    cur.close()
    conn.close()

    return jsonify(result), 201

@app.route('/restaurants/<restaurant_id>', methods=['GET'])
def get_restaurant_by_id(restaurant_id):
    data = {}

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    query = f"SELECT * FROM Restaurants WHERE id = '{restaurant_id}';"

    cur.execute(query)
    results = cur.fetchall()

    row_count = cur.rowcount

    if row_count == 0:
        return jsonify({'error': "Id does not exist in database"}), 400

    row = results[0]
    data['restaurant'] = {
        'id' : row['id'],
        'rating' : row['rating'],
        'name' : row['name'],
        'site' : row['site'],
        'email' : row['email'],
        'phone' : row['phone'],
        'street' : row['street'],
        'city' : row['city'],
        'state' : row['state'],
        'lat' : row['lat'],
        'lng' : row['lng']
    }

    cur.close()
    conn.close()

    return jsonify(data), 200

@app.route('/restaurants/<restaurant_id>', methods=['DELETE'])
def delete_restaurant_by_id(restaurant_id):
    conn = get_db_connection()
    cur = conn.cursor()

    query = f"DELETE FROM Restaurants WHERE id = '{restaurant_id}';"

    cur.execute(query)

    rows_deleted = cur.rowcount

    if rows_deleted == 0:
        return jsonify({'error': "Id does not exist in database"}), 400
    
    conn.commit()

    cur.close()
    conn.close()

    result = {
        'rows_deleted' : rows_deleted,
        'deleted_id' : restaurant_id,
        'message': " Successfully deleted the rows."
    }

    return jsonify(result), 201

# Get statistics of restaurants within circle of parameters
@app.route('/restaurants/statistics', methods=['GET'])
def get_statistics():

    # Get parameters and return error if missing parameters
    if 'latitude' in request.args:
        latitude = request.args.get("latitude")
    else:
        return jsonify({'error': "No latitude parameter in request"}), 400
    
    if 'longitude' in request.args:
        longitude = request.args.get("longitude")
    else:
        return jsonify({'error': "No longitude parameter in request"}), 400

    if 'radius' in request.args:
        radius = request.args.get("radius")
    else:
        return jsonify({'error': "No radius parameter in request"}), 400
    
    data = {'restaurants':[]}

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    
    query = f"SELECT * FROM Restaurants WHERE ST_DistanceSphere(ST_MakePoint(lng,lat), ST_MakePoint({longitude},{latitude})) <= {radius};"

    cur.execute(query)
    results = cur.fetchall()

    row_count = cur.rowcount

    rating_list = []

    for row in results:
        data['restaurants'].append({
            'id' : row['id'],
            'rating' : row['rating'],
            'name' : row['name'],
            'site' : row['site'],
            'email' : row['email'],
            'phone' : row['phone'],
            'street' : row['street'],
            'city' : row['city'],
            'state' : row['state'],
            'lat' : row['lat'],
            'lng' : row['lng']
        })

        rating_list.append(row['rating'])

    cur.close()
    conn.close()

    data['count'] = row_count

    data['avg'] = statistics.mean(rating_list)
    data['std'] = statistics.stdev(rating_list)

    return jsonify(data), 200

initialize_database(db_url)
print("Database initialized and populated, postGIS enabled")

if __name__ == '__main__':
    app.run(debug=True)