from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import pymysql
import bcrypt
import jwt
import datetime

app = FastAPI()

# Database Connection
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="smart_bus_db",
        cursorclass=pymysql.cursors.DictCursor
    )

# Secret key for JWT token
SECRET_KEY = "your_secret_key"

# Pydantic Model for Registration
class DriverRegister(BaseModel):
    full_name: str
    license_number: str
    phone_number: str
    email: str
    password: str
    bus_id: int

@app.post("/register-driver")
async def register_driver(driver: DriverRegister):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Hash password
    hashed_password = bcrypt.hashpw(driver.password.encode('utf-8'), bcrypt.gensalt())

    # Insert driver data
    try:
        cursor.execute(
            "INSERT INTO bus_drivers (full_name, license_number, phone_number, email, password_hash, bus_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (driver.full_name, driver.license_number, driver.phone_number, driver.email, hashed_password, driver.bus_id)
        )
        conn.commit()
    except pymysql.IntegrityError:
        raise HTTPException(status_code=400, detail="Driver with this email or phone number already exists.")
    finally:
        cursor.close()
        conn.close()

    return {"message": "Bus driver registered successfully"}

# Driver Login
class DriverLogin(BaseModel):
    email: str
    password: str

@app.post("/login-driver")
async def login_driver(credentials: DriverLogin):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bus_drivers WHERE email = %s", (credentials.email,))
    driver = cursor.fetchone()

    if not driver or not bcrypt.checkpw(credentials.password.encode('utf-8'), driver["password_hash"].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT Token
    token = jwt.encode({"id": driver["id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)}, SECRET_KEY, algorithm="HS256")

    return {"token": token, "message": "Login successful"}

