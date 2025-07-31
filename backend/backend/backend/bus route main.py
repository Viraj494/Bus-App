from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import hashlib

app = Flask(__name__)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(hashed_password, password):
    hashed_input = hash_password(password)
    return hashed_input == hashed_password


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port='3306',
            database='trace_route',
            user='root',
            password=''
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# Test API
@app.route('/test', methods=['GET'])
def test():
    print("Test API")
    return jsonify({"message": "Test API"}), 200


# Register API
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    foreigner = data.get('foreigner')

    # Check if username exists
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        return jsonify({"message": "Username already exists"}), 400

    # Hash the password
    hashed_password = hash_password(password)

    # Insert new user
    cursor.execute("INSERT INTO users (username, password, foreigner) VALUES (%s, %s, %s)",
                   (username, hashed_password, foreigner))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "User registered successfully"}), 201


# Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if user exists
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "Invalid username or password"}), 400

    # Verify password
    if check_password(user['password'], password) == False:
        return jsonify({"message": "Invalid username or password"}), 400

    cursor.close()
    connection.close()

    return jsonify({"message": "login success!"}), 200


# Check Username Availability API
@app.route('/username-available', methods=['GET'])
def username_available():
    username = request.args.get('username')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:
        return jsonify({"available": False, "message": "Username is already taken"}), 200
    else:
        return jsonify({"available": True, "message": "Username is available"}), 200


# Location List API
@app.route('/location-list', methods=['GET'])
def location_list():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select distinct(place) from halts")
    locationList = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify({"locationList": locationList}), 200


# Get routes from origin to destination API
@app.route('/get-routes-origin-to-destination', methods=['GET'])
def get_routes_origin_to_destination():
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT h1.route_no FROM halts h1 JOIN halts h2 ON h1.route_no = h2.route_no WHERE h1.place = %s AND h2.place = %s", (origin, destination))
    routes = cursor.fetchall()

    cursor.close()
    connection.close()

    if routes:
        return jsonify({"available": True, "routes": routes}), 200
    else:
        return jsonify({"available": False, "routes": []}), 200
    

if __name__ == '__main__':
    app.run(debug=True)