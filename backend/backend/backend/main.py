from flask import Flask, request, jsonify, render_template, redirect, session
from flask_session import Session
import mysql.connector
from mysql.connector import Error
import hashlib
import os
import random
import string
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from datetime import datetime
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


app = Flask(__name__)
app.secret_key = "trace-route"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

UPLOAD_FOLDER = "uploads"
UPLOAD_TEMPLATE_FOLDER = "uploads\\template"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

###########################################################################################
###########################################################################################
###########################################################################################
# Mobile app backend APIs - Begin
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


# Get buses to travel API
@app.route('/get-buses-to-travel', methods=['GET'])
def get_buses_to_travel():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    routeNo = request.args.get('routeNo')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT CASE WHEN h1.seq_no < h2.seq_no THEN 'FORWARD' WHEN h1.seq_no > h2.seq_no THEN 'BACKWARD' ELSE 'INVALID' END AS direction FROM halts h1 JOIN halts h2 ON h1.route_no = h2.route_no WHERE h1.place = %s AND h2.place = %s AND h1.route_no = %s", (origin, destination, routeNo))
    directionItem = cursor.fetchone()

    if directionItem == None:
        return jsonify({"message": "No buses available now"}), 200
    elif directionItem["direction"] == "FORWARD":
        cursor.execute("select halt_id from halts h1 where h1.route_no = %s and h1.seq_no <= (select seq_no from halts h2 where h2.place = %s and h2.route_no = %s)", (routeNo, origin, routeNo))
        previousHaltsItem = cursor.fetchall()
    elif directionItem["direction"] == "BACKWARD":
        cursor.execute("select halt_id from halts h1 where h1.route_no = %s and h1.seq_no >= (select seq_no from halts h2 where h2.place = %s and h2.route_no = %s)", (routeNo, origin, routeNo))
        previousHaltsItem = cursor.fetchall()
    else:
        return jsonify({"message": "No buses available now"}), 200

    haltIdStringList = ""
    for previousHalts in previousHaltsItem:
        haltIdStringList += str(previousHalts["halt_id"]) + ","
    haltIdStringList = haltIdStringList.rstrip(' ,')

    if(haltIdStringList == ""):
        return jsonify({"message": "No buses available now"}), 200
    else:
        if directionItem["direction"] == "FORWARD":
            cursor.execute("select b.route_no, t.bus_no, t.available_seats, t.latitude, t.longitude, t.next_halt_id, h.place from trips t, buses b, halts h where b.bus_no = t.bus_no and h.halt_id = t.next_halt_id and t.direction = %s and b.route_no = %s and available_seats > 0 and t.next_halt_id in ("+haltIdStringList+") order by t.next_halt_id desc", (directionItem["direction"], routeNo))
        else:
            cursor.execute("select b.route_no, t.bus_no, t.available_seats, t.latitude, t.longitude, t.next_halt_id, h.place from trips t, buses b, halts h where b.bus_no = t.bus_no and h.halt_id = t.next_halt_id and t.direction = %s and b.route_no = %s and available_seats > 0 and t.next_halt_id in ("+haltIdStringList+") order by t.next_halt_id asc", (directionItem["direction"], routeNo))
        busListItem = cursor.fetchall()

    cursor.close()
    connection.close()

    if busListItem:
        return jsonify({"message":"buses available", "busList":busListItem}), 200
    else:
        return jsonify({"message": "No buses available now"}), 200


# Halt List by route number API
@app.route('/halt-list-by-route-no', methods=['GET'])
def halt_list_by_route_no():
    route_no = request.args.get('route_no')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from halts where route_no = %s order by seq_no", (route_no,))
    hallList = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify({"hallList": hallList}), 200


# Find available seats by bus number API
@app.route('/seats-by-bus-no', methods=['GET'])
def available_seats_by_bus_no():
    bus_no = request.args.get('bus_no')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select available_seats, longitude, latitude from trips where bus_no = %s", (bus_no,))
    seatsData = cursor.fetchone()

    cursor.close()
    connection.close()

    if seatsData:
        seatsData["message"] = "Seats fetched"
        return jsonify(seatsData), 200
    else:
        return jsonify({"message": "Invalid bus number"}), 200


# find reservation details by user-id and bus_no
@app.route('/reservation-by-user-id-and-bus-no', methods=['GET'])
def reservation_by_user_id_and_bus_no():
    user_id = request.args.get('user_id')
    bus_no = request.args.get('bus_no')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from reservation where user_id = %s and bus_no = %s and status in ('RESERVED', 'TRAVEL')", (user_id,bus_no,))
    reservation = cursor.fetchone()

    cursor.close()
    connection.close()

    if reservation:
        reservation["message"] = "Reservation details available"
        return jsonify(reservation), 200
    else:
        return jsonify({"message": "Reservation details not available"}), 200


# change reservation API
@app.route('/change-reservation-status', methods=['POST'])
def change_reservation_status():
    data = request.json
    reservation_id = data.get('reservation_id')
    status = data.get('status')

    if(status == "TRAVEL" or status == "COMPLETED" or status == "CANCELED"):
        # Check if username exists
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("update reservation set status = %s WHERE id = %s", (status, reservation_id,))
        
        cursor.execute("select * from reservation where id = %s", (reservation_id,))
        reservation = cursor.fetchone()

        cursor.execute("select * from trips where bus_no = %s", (reservation['bus_no'],))
        trips = cursor.fetchone()
        available_seats = trips['available_seats'] 
        available_seats = int(available_seats) + int(reservation['seat_count'])

        message = ""
        if(status == "TRAVEL"):
            message = "Reservation utilized"
        elif(status == "COMPLETED"):
            cursor.execute("update trips set available_seats = %s WHERE bus_no = %s", (available_seats, trips['bus_no'],))
            message = "Reservation completed"
        elif(status == "CANCELED"):
            cursor.execute("update trips set available_seats = %s WHERE bus_no = %s", (available_seats, trips['bus_no'],))
            message = "Reservation canceled"

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": message}), 201
    else:
        return jsonify({"message": "Invalid data"}), 400


# reservation API
@app.route('/make-reservation', methods=['POST'])
def make_reservation():
    data = request.json
    bus_no = data.get('bus_no')
    user_id = data.get('user_id')
    seat_count = data.get('seat_count')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("select * from trips where bus_no = %s", (bus_no,))
    trips = cursor.fetchone()
    available_seats = trips['available_seats']
    available_seats = available_seats - seat_count
    current_time = datetime.now()

    cursor.execute("update trips set available_seats = %s WHERE bus_no = %s", (available_seats, bus_no,))
    cursor.execute("INSERT INTO reservation (`user_id`, `bus_no`, `seat_count`, `status`, `booktime`) VALUES (%s, %s, %s, %s, %s)", (user_id, bus_no, seat_count, 'RESERVED', current_time,))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Reservation made successfully"}), 201
# Mobile app backend APIs - End
###########################################################################################
###########################################################################################
###########################################################################################


###########################################################################################
###########################################################################################
###########################################################################################
# Bus Web Application - Begin
# Home page
@app.route('/bus/home', methods = ['GET'])
def bus_home():
    session.clear()
    return render_template('homepage.html')


# Login page
@app.route('/bus/login', methods = ['GET'])
def bus_login():
    error_message=""
    if(session.get("unauthorized_access_message")):
        error_message=session.get("unauthorized_access_message")
    session.clear()
    return render_template('login.html', error_message=error_message)


# Register page - action
@app.route('/bus/login', methods = ['POST'])
def bus_login_action():
    password = request.form["password"]
    bus_no = request.form["busNumber"]

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("select * from bus_users where username = %s", (bus_no,))
    bus = cursor.fetchone()

    cursor.close()
    connection.close()
    session.clear()

    if bus != None:
        if check_password(bus['password'], password) == False:
            return render_template('login.html', error_message="Invalid username or password")
        else:
            session["bus"] = bus
            return redirect('/bus/dashboard')
    else:
        return render_template('login.html', error_message="Invalid username or password")


# Register page
@app.route('/bus/register', methods = ['GET'])
def bus_register():
    session.clear()
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("select * from routes")
    routes = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return render_template('register.html', error_message="", routes=routes)


# Register page - action
@app.route('/bus/register', methods = ['POST'])
def bus_register_action():
    session.clear()
    password = request.form["password"]
    bus_no = request.form["busNumber"]
    route_no = request.form["routeNumber"]

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("select * from bus_users where username = %s", (bus_no,))
    bus = cursor.fetchone()
    
    if bus != None:
        cursor.close()
        connection.close()

        return render_template('register.html', error_message="Bus number already exists")
    else:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO bus_users (`username`, `password`) VALUES (%s, %s)", (bus_no, hashed_password,))
        cursor.execute("INSERT INTO buses (`bus_no`, `route_no`) VALUES (%s, %s)", (bus_no, route_no,))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect('/bus/login')


# Dashboard page
@app.route('/bus/dashboard', methods = ['GET'])
def bus_dashboard():
    bus = session.get("bus")

    if(bus == None):
        session["unauthorized_access_message"] = "Please login to continue"
        return redirect('/bus/login')
    else:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("select t.*, h.place from trips t, halts h where t.next_halt_id = h.halt_id and bus_no = %s", (bus['username'],))
        trips = cursor.fetchone()

        cursor.execute("select * from buses where bus_no = %s", (bus['username'],))
        bus_detail = cursor.fetchone()

        sql1 = """ SELECT h1.route_no, 
                        h1.place AS first_halt, 
                        h2.place AS last_halt
                    FROM halts h1
                    JOIN halts h2 ON h1.route_no = h2.route_no
                    WHERE h1.route_no = '"""+bus_detail['route_no']+"""'
                    AND h1.seq_no = (SELECT MIN(seq_no) FROM halts WHERE route_no = '"""+bus_detail['route_no']+"""')
                    AND h2.seq_no = (SELECT MAX(seq_no) FROM halts WHERE route_no = '"""+bus_detail['route_no']+"""');
                    """
        cursor.execute(sql1)
        travel_detail = cursor.fetchone()

        sql2 = """ SELECT 
                    SUM(CASE WHEN status = 'RESERVED' THEN 1 ELSE 0 END) AS reserved_count, 
                    SUM(CASE WHEN status = 'TRAVEL' THEN 1 ELSE 0 END) AS travel_count 
                FROM reservation 
                WHERE bus_no = %s;
                """
        cursor.execute(sql2, (bus['username'],))
        seat_detail = cursor.fetchone()        

        cursor.close()
        connection.close()
    return render_template('dashboard.html', bus=bus, trips=trips, travel_detail=travel_detail, bus_detail=bus_detail, seat_detail=seat_detail)


@app.route('/bus/logout')
def bus_logout():
    session.clear()
    return redirect('/bus/login')


@app.route('/bus/detect-seat-availability', methods = ['POST'])
def bus_detect_seat_availability():
    id = request.args.get('id')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("select * from buses where bus_no = %s", (id,))
    bus = cursor.fetchone()
    
    if bus == None:
         return jsonify({"error": "Bus unavailable!"}), 400
    elif bus['template'] == None or bus['template'] == '':
        return jsonify({"error": "template file unavailable!"}), 400
    else:
        if "image" not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        
        random_str = generate_random_string()
        filename = secure_filename(file.filename)
        new_filename = f"{random_str}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, new_filename)
        
        try:
            file.save(file_path)
            template_image = bus['template']
            templates = [
                template_image,
            ]
            predict_image_file_path = UPLOAD_FOLDER + "\\" + new_filename
            print("predict_image_file_path: " + predict_image_file_path)
            seats = detect_patterns(predict_image_file_path, templates)            
            return jsonify({"seats": seats})
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)


@app.route("/bus/upload-template", methods=["POST"])
def bus_upload_template():
    bus_id = request.args.get("id")
    if not bus_id:
        return jsonify({"error": "Missing id parameter"}), 400
    
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    random_str = generate_random_string()
    filename = secure_filename(file.filename)
    new_filename = f"{random_str}_{filename}"
    file_path = os.path.join(UPLOAD_TEMPLATE_FOLDER, new_filename)
    
    try:
        file.save(file_path)
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("update buses set template = %s WHERE bus_no = %s", (file_path, bus_id,))   
        
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "File uploaded and database updated", "filename": new_filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/bus/update-seat-avilability", methods=["GET"])
def bus_update_seat_availability():
    bus_no = request.args.get('bus_no')
    seats = request.args.get('seats')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
        
    cursor.execute("update trips set available_seats = %s WHERE bus_no = %s", (seats, bus_no,))   
        
    connection.commit()
    cursor.close()
    connection.close()

    return "Seats updated!"


@app.route("/bus/update-location", methods=["GET"])
def bus_update_location():
    bus_no = request.args.get('bus_no')
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
        
    cursor.execute("update trips set longitude = %s, latitude = %s WHERE bus_no = %s", (longitude, latitude, bus_no,))   
        
    connection.commit()
    cursor.close()
    connection.close()

    return "Location updated!"


@app.route("/bus/update-direction", methods=["GET"])
def bus_update_direction():
    bus_no = request.args.get('bus_no')
    direction = request.args.get('direction')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
        
    cursor.execute("update trips set direction = %s WHERE bus_no = %s", (direction, bus_no,))   
        
    connection.commit()
    cursor.close()
    connection.close()

    return "Direction updated!"


@app.route("/bus/update-next-halt", methods=["GET"])
def bus_update_next_halt():
    bus_no = request.args.get('bus_no')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("select * from trips where bus_no = %s", (bus_no,))
    trips = cursor.fetchone()

    cursor.execute("select r.origin_halt_id, r.destination_halt_id from buses b, routes r where b.route_no = r.route_no and b.bus_no = %s", (bus_no,))
    halt_detail = cursor.fetchone()
    halt_id = 0

    if trips['direction'] == 'FORWARD':
        print('forward')
        if trips['next_halt_id'] == halt_detail['destination_halt_id']:
            print('change direction to backward and start to decrease the halt id')
            halt_id = trips['next_halt_id'] - 1
            cursor.execute("update trips set direction = %s WHERE bus_no = %s", ('BACKWARD', bus_no,))   
            connection.commit()          
        else:
            print('increase the halt id')
            halt_id = trips['next_halt_id'] + 1
    else:
        print('backward')
        if trips['next_halt_id'] == halt_detail['origin_halt_id']:
            print('change direction to forward and start to increase the halt id')
            halt_id = trips['next_halt_id'] + 1
            cursor.execute("update trips set direction = %s WHERE bus_no = %s", ('FORWARD', bus_no,))   
            connection.commit()       
        else:
            print('decrease the halt id')
            halt_id = trips['next_halt_id'] - 1

    cursor.execute("update trips set next_halt_id = %s WHERE bus_no = %s", (halt_id, bus_no,))   
        
    connection.commit()
    cursor.close()
    connection.close()

    return "Next halt updated!"
# Bus Web Application - End
###########################################################################################
###########################################################################################
###########################################################################################
# utility functions - Begin
def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_letters, k=length))


def detect_patterns(image_path, template_paths):
    # Read the main image
    image = cv2.imread(image_path)

    # Convert the main image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Initialize a counter for detected patterns
    pattern_count = 0

    for template_path in template_paths:
        # Read and convert each template to grayscale
        template = cv2.imread(template_path)
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Apply template matching
        result = cv2.matchTemplate(gray_image, gray_template, cv2.TM_CCOEFF_NORMED)

        # Set a threshold for detection
        threshold = 0.8  # Adjust this value based on your needs
        yloc, xloc = np.where(result >= threshold)

        # Draw rectangles around detected patterns
        h, w = gray_template.shape
        detected_coordinates = []  # List to store coordinates

        for (x, y) in zip(xloc, yloc):
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            detected_coordinates.append((x, y, w, h))  # Store coordinates for further processing

        # Use non-maximum suppression to filter overlapping boxes
        if detected_coordinates:
            boxes = np.array(detected_coordinates)
            x1 = boxes[:, 0]
            y1 = boxes[:, 1]
            x2 = boxes[:, 0] + boxes[:, 2]
            y2 = boxes[:, 1] + boxes[:, 3]

            areas = (x2 - x1) * (y2 - y1)
            indices = cv2.dnn.NMSBoxes(boxes.tolist(), [1]*len(boxes), score_threshold=0.8, nms_threshold=0.3)

            unique_detections = len(indices) if indices is not None else 0
            pattern_count += unique_detections

    print(f"Number of unique detected patterns in {image_path}: {pattern_count}")
    return pattern_count


def fetch_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.user_id, b.route_no, r.booktime
        FROM reservation r
        JOIN buses b ON r.bus_no = b.bus_no
        WHERE r.status = 'COMPLETED'
    """)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def preprocess_data(data):
    features = []
    target = []
    
    # Get all unique user IDs and route numbers for encoding
    user_ids = list(set(row['user_id'] for row in data))
    route_nos = list(set(row['route_no'] for row in data))

    le_user = LabelEncoder()
    le_user.fit(user_ids)  # Fit on all unique user_ids

    le_route = LabelEncoder()
    le_route.fit(route_nos)  # Fit on all unique route_nos

    for row in data:
        user_id = le_user.transform([row['user_id']])[0]  
        route_no = le_route.transform([row['route_no']])[0]
        
        booktime = row['booktime']
        hour_of_day = booktime.hour
        weekday = booktime.weekday()

        features.append([user_id, hour_of_day, weekday])
        target.append(route_no)
    
    return features, target, le_user, le_route


def train_model():
    data = fetch_data()
    if not data:
        print("No data found for training.")
        return

    features, target, le_user, le_route = preprocess_data(data)

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save model and encoders
    with open('route_predictor.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('user_encoder.pkl', 'wb') as f:
        pickle.dump(le_user, f)
    with open('route_encoder.pkl', 'wb') as f:
        pickle.dump(le_route, f)

    print("Model training complete and saved.")

# Load pre-trained model and encoders
with open('route_predictor.pkl', 'rb') as f:
    model = pickle.load(f)
with open('user_encoder.pkl', 'rb') as f:
    le_user = pickle.load(f)
with open('route_encoder.pkl', 'rb') as f:
    le_route = pickle.load(f)


@app.route('/predict-route', methods=['GET'])
def predict_route():
    print('predict route')
    user_id = request.args.get('user_id')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.user_id, b.route_no, r.booktime
        FROM reservation r
        JOIN buses b ON r.bus_no = b.bus_no
        WHERE r.status = 'COMPLETED' AND r.user_id = %s
    """, (user_id,))
    user_data = cursor.fetchall()
    cursor.close()
    connection.close()

    if not user_data:
        return jsonify({'message': 'No historical data available. Please try again later.'})

    # Handling unseen user IDs
    if user_id not in le_user.classes_:
        user_encoded = -1  # Assign a default value
    else:
        user_encoded = le_user.transform([user_id])[0]

    predictions = []
    today_date = datetime.today().strftime('%Y-%m-%d')
    
    for i in range(4):  # Generate 4 predictions
        booktime = user_data[-1]['booktime']
        if isinstance(booktime, str):
            booktime = datetime.datetime.strptime(booktime, "%Y-%m-%d %H:%M:%S")

        hour_of_day = booktime.hour + i  # Predicting for different times
        weekday = booktime.weekday()

        features = [[user_encoded, hour_of_day % 24, weekday]]

        try:
            predicted_route_encoded = model.predict(features)[0]
            predicted_route = le_route.inverse_transform([predicted_route_encoded])[0]
            predicted_time = f"{today_date}: {hour_of_day % 24}:00"
            predictions.append({
                "predicted_time": predicted_time,
                "predicted_route_number": predicted_route
            })
        except ValueError:
            return jsonify({"error": "Prediction failed due to unseen data"}), 500

    return jsonify(predictions)


@app.route('/train-model', methods=['GET'])
def train_model_api():
    train_model()
    return jsonify({"message": "Model trained"}), 200
# utility functions - End
###########################################################################################
###########################################################################################
###########################################################################################


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    # app.run(debug=True)